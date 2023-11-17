from datetime import datetime, timedelta

from fastapi import FastAPI
from pydantic import BaseModel
from utils.db import db_getSaleData, db_getAllSalesData, db_getPeriodicSalesData, fetchCompareData \
    , fetch_category_sales_data, getInventory, db_inventory_logs,db_update_inventory,db_get_update_level

app = FastAPI()

class Inventory_logs(BaseModel):
    quantity: int
    status: str
    update_date: datetime
    inventory_id: int


@app.get('/getallsalesData')
def getAllSaleData():
    response = db_getAllSalesData()
    if response:
        return response
    return {'message': "no data found"}


@app.get('/getperiodicRevenue')
def getRevenue(start_date, end_date, periodicity, product_id=None):
    response = db_getPeriodicSalesData(start_date, end_date, periodicity, product_id)
    return response


@app.get('/getCompareData')
def getCompareData(start_date, end_date, compare_start_date, compare_end_date, categories):
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


@app.get('/getSale')
def getSale(start_date, end_date, category=None, product_id=None):
    if (category):
        response = fetch_category_sales_data(category, start_date, end_date)
    elif product_id:
        response = db_getSaleData(product_id, start_date, end_date)
    else:
        response = {"message": "please provide any parameter"}
    return response


@app.get('/getInventoryStatus')
def getInventoryStatus(inventory_id, product_id):
    response = getInventory(inventory_id, product_id)
    if not response:
        response = {"message": "no data found"}
    return response


@app.post('/inventory_update')
def UpadateInventory(inventory: Inventory_logs):
    response = db_inventory_logs(inventory)
    res = db_update_inventory(inventory.status,inventory.quantity,inventory.inventory_id)
    return res

@app.get('/getupdate/{inventory_id}')
def getUpdate(inventory_id):
    response = db_get_update_level(inventory_id)
    if not response:
        response = {"message": "no data found"}
    return response
