import logging

import pandas as pd
from sqlalchemy import create_engine, extract, func
from sqlalchemy.orm import sessionmaker,joinedload
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from os import environ
from dotenv import load_dotenv

load_dotenv()

from .models import Base, Sales, Product, Category, Inventory, InventoryLog
from .schema import SalesSchema

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASSWORD")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_DATABASE = environ.get("DB_DATABASE")
DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

engine = create_engine(DATABASE_URI, poolclass=NullPool, echo=False)
Session = sessionmaker(bind=engine)

# # Commented because causing Too many connections
# # change the table store_product_review data encoding, to support the inserted data encoding type
# engine.execute('ALTER TABLE `store_product_review` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')


@contextmanager
def session_scope():
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_sale_data(product_id, start_date, end_date):
    sales = []
    with session_scope() as s:
        if product_id:
            sales_data = (
                s.query(Sales, Product)
                .join(Product, Sales.product_id == Product.id)
                .filter(
                    (Sales.product_id == product_id) &
                    (func.date(Sales.date) >= start_date) &
                    (func.date(Sales.date) <= end_date)
                )
                .options(joinedload(Sales.product))
                .all()
            )

            for sale, product in sales_data:
                sales.append({
                    "product_id": product.id,
                    "Product Name": product.name,
                    "Sales": sale.amount,
                    "date": sale.date
                })

        return sales


def db_getAllSalesData():
    sales = []
    with session_scope() as s:
        sales_data = s.query(Sales).all()
        for sale in sales_data:
            product = s.query(Product).filter(Product.id == sale.product_id).first()
            sales.append({
                "product_id": product.id,
                "Product Name": product.name,
                "Sales": sale.amount,
                "date": sale.date
            })
    return sales


def db_getPeriodicSalesData(start_date, end_date, periodicity, product_id):
    sales = []
    if periodicity == "week":
        frequency = "1W"
    elif periodicity == "month":
        frequency = "1M"
    elif periodicity == "annual":
        frequency = "1Y"
    else:
        frequency = "1D"
    with session_scope() as s:
        if product_id:
            sales_data = s.query(Sales).filter(
                Sales.product_id == product_id,
                func.date(Sales.date) >= start_date,
                func.date(Sales.date) <= end_date
            ).all()
        else:
            sales_data = s.query(Sales).filter(
                func.date(Sales.date) >= start_date,
                func.date(Sales.date) <= end_date
            ).all()
        sales_data = SalesSchema().dump(sales_data, many=True)
        print(sales_data)
        df = pd.DataFrame(sales_data)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date']).dt.date
            print(df.to_string())
            df = df.groupby(['date','product_id'])['amount'].sum().reset_index()
            print(df.to_string())
            df.fillna(0, inplace=True)
            df['date'] = pd.to_datetime(df['date'])
            dg = df.groupby([pd.Grouper(key='date', freq=frequency), 'amount']).sum().reset_index()
            response = dg.to_dict(orient="records")
            for each in response:
                product_id_value = int(df['product_id'].iloc[0])  # Extract the value from the pandas Series
                query = s.query(Product).filter(Product.id == product_id_value).first()
                product_name = query.name if query else None
                date = each["date"].strftime("%Y-%m-%d")
                product_id = each["product_id"]
                res = {
                    "date": date,
                    "sales": int(each["amount"]),
                    "product_id ": product_id,
                    "product_name": product_name

                }
                sales.append(res)
    return sales


def fetchCompareData(start_date, end_date, categories):
    with session_scope() as s:
        category = s.query(Category).filter(Category.category_name == categories).first()
        if category:
            data = (
                s.query(Sales, Product)
                .join(Product, Sales.product_id == Product.id)
                .filter(
                    (Product.category_id == category.id) &
                    (func.date(Sales.date) >= start_date) &
                    (func.date(Sales.date) <= end_date)
                )
            )
        sales_data = data.with_entities(func.sum(Sales.amount)).scalar()

    sales_data = int(sales_data) if sales_data else 0
    return sales_data


def fetch_category_sales_data(category, start_date, end_date):
    sales = []
    with session_scope() as s:
        if category:
            sales_data = (
                s.query(Category.category_name, Product.name, Sales.amount, Sales.date)
                .join(Product, Category.id == Product.category_id)
                .join(Sales, Product.id == Sales.product_id)
                .filter(
                    Category.category_name == category,
                    func.date(Sales.date) >= start_date,
                    func.date(Sales.date) <= end_date
                )
                .all()
            )

            for sale_data in sales_data:
                sales.append({
                    "category": sale_data.category_name,
                    "product": sale_data.name,
                    "sales": sale_data.amount,
                    "date": sale_data.date
                })

    return sales


def getInventory(inventory_id, product_id):
    inventory = {}
    with session_scope() as s:
        inventories = s.query(Inventory).filter(Inventory.id == inventory_id).first()
        if inventories:
            product = (
                s.query(Product)
                .filter(Product.id == product_id)
                .first()
            )
            if (inventories.Quantity > inventories.min_quantity) & (inventories.Quantity != 0):
                inventory_status = 'Low Stock'
            elif inventories.Quantity < inventories.min_quantity:
                inventory_status = 'Available'
            else:
                inventory_status = 'Out of stock'
            inventory = {
                "inventory_id": inventories.id,
                "Product_id": product.id,
                "Product": product.name,
                "Product_description": product.description,
                "Quantity": inventories.Quantity,
                "Inventory Status": inventory_status
            }

        return inventory


def db_inventory_logs(inventory):
    with session_scope() as s:
        new_inventory_log = InventoryLog(
            quantity=inventory.quantity,
            status=inventory.status,
            update_date=inventory.update_date,
            inventory_id=inventory.inventory_id
        )
        s.add(new_inventory_log)
        s.commit()
    return {"message": "successfully entered"}


def db_update_inventory(status, new_quantity, inventory_id):
    with session_scope() as session:
        # Assuming you have a model named Inventory

        inventory = session.query(Inventory).filter(Inventory.id == inventory_id).first()
        if inventory:
            if status == "in":
                inventory.Quantity = inventory.Quantity + new_quantity
            elif status == "out" and inventory.Quantity >= new_quantity:
                inventory.Quantity -= new_quantity
            else:
                # Handle the case where the status is not recognized or there's not enough quantity for an "out" operation
                return {"message": "Invalid status or insufficient quantity for 'out' operation"}
            session.commit()

            return {"message": "Inventory quantity updated successfully"}
        else:
            return {"message": "Inventory not found"}


def db_get_update_level(inventory_id):
    with session_scope() as s:
        inventory_logs = s.query(InventoryLog).filter(InventoryLog.inventory_id == inventory_id).all()
    return inventory_logs
