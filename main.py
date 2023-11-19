from datetime import datetime
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from utils.db import get_sale_data, db_getAllSalesData, db_getPeriodicSalesData, fetchCompareData,\
    fetch_category_sales_data, getInventory, db_inventory_logs, db_update_inventory, db_get_update_level

app = FastAPI(title="Inventory & Sales API", docs_url="/")


class Period(str, Enum):
    daily = "daily"
    week = "week"
    month = "month"
    annual = "annual"


class InventoryLogs(BaseModel):
    quantity: int
    status: str
    update_date: datetime
    inventory_id: int


@app.get('/get-all-sales-data')
def getAllSaleData():
    """
    This URL returns all the sales data
    """
    response = db_getAllSalesData()
    if response:
        return response
    return {'message': "no data found"}


@app.get('/get-periodic-revenue')
def getRevenue(start_date, end_date, periodicity: Period, product_id=None):
    """
    This URL returns all the revenue information
    """
    response = db_getPeriodicSalesData(start_date, end_date, periodicity, product_id)
    return response


@app.get('/get-compare-data')
def getCompareData(start_date, end_date, compare_start_date, compare_end_date, categories):
    """
    This URL returns the comparison between sales of given date ranges
    """
    data = fetchCompareData(start_date, end_date, categories)
    compare_data = fetchCompareData(start_date=compare_start_date, end_date=compare_end_date, categories=categories)
    comparison = round(((data - compare_data) / compare_data) * 100, 2) if compare_data else 0
    res = {
        "category": categories,
        "start_date": start_date,
        "end_date": end_date,
        "sales_data": data,
        "compare_sales_data": compare_data,
        "comparison": comparison
    }

    return res


@app.get('/get-sales')
def getSales(start_date, end_date, category=None, product_id=None):
    """
    This URL returns sales
    """
    if category:
        response = fetch_category_sales_data(category, start_date, end_date)
    elif product_id:
        response = get_sale_data(product_id, start_date, end_date)
    else:
        response = {"message": "please provide any parameter"}
    return response


@app.get('/get-inventory-status')
def getInventoryStatus(inventory_id, product_id):
    """
    This URL returns the current inventory status
    """
    response = getInventory(inventory_id, product_id)
    if not response:
        response = {"message": "no data found"}
    return response


@app.post('/update-inventory')
def updateInventory(inventory: InventoryLogs):
    """
    This URL updates the inventory
    """
    db_inventory_logs(inventory)
    res = db_update_inventory(inventory.status, inventory.quantity, inventory.inventory_id)
    return res


@app.get('/get-updates/{inventory_id}')
def getUpdate(inventory_id):
    """
    This URL returns the inventory logs
    """
    response = db_get_update_level(inventory_id)
    if not response:
        response = {"message": "no data found"}
    return response
