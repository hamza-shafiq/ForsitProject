# Inventory & Sales API

## Endpoints

This includes these services, using fastApi:
* ***`/get-all-sales-data`***: This Endpoint responsible for retrieve and filter all sales data 
* ***`/get-periodic-revenue`***:  This Endpoint responsible for analyze sales data on annually,weekly,daily and monthly basis 
* ***`/get-compare-data`***: The endpoint give the comparison across different period and categories
* ***`/get-sales`***: This endpoint filter the sale data for category or product
* ***`/get-inventory-status`***: This endpoint retrieve the inventory status of product e.g. out of stock, available
* ***`/update-inventory`***: This endpoint to update inventory
* ***`/get-updates/{inventory_id}`***: This endpoint track changes over time

## Database

All these endpoints use the msql database and relationship between tables
The client uses sqlalchemy and alembic to manage migrations.
Before you use alembic make sure you have updated DB credentials in your local `.env` file
NOTE: Check IS_OFFLINE=true in your `.env` file

To create a new migration:
```sh
cd migrations
alembic --name dev revision --autogenerate -m "<migration_msg>"
```

To upgrade all migrations:
```sh
cd migrations
alembic upgrade head
```

In order to plug the test data in your database, use the following command to upload the attached dump file.
```sh
mysql -u mac -p <database_name> < dump.sql
```

## Infrastructure

![high level FastAPI diagram](assets/FastApi.png?raw=true)

## Project Setup

Services are deployed using a FastApi configuration. To set up fastApi and required plugins:

You first have to create venv in your project
```bash
$ python -m venv venv_name
```

And to activate this venv For Linux OS or Mac OS:

```bash
$ source venv_name/bin/activate
```

And for window

```bash
$ venv_name\Scripts\activate
```

Install the required packages:

```bash
$ pip install -r requirements.txt
```

To run this App

```bash
$ uvicorn main:app --reload
```


