# FORSIT Test Project

This repository is responsible for FORSIT Test Project.

## Endpoint

This includes these services, using fastApi:
* ***`getSalesData`***: This Endpoint responsible for retrieve and filter all sales data 
* ***`getperiodicRevenue`***:  This Endpoint responsible for analyze sales data on annually,weekly,daily and monthly basis 
* ***`getCompareData`***: The endpoint give the comparison across different period and categories
* ***`getSale`***: This endpoint filter the sale data for category or product
* ***`getInventoryStatus`***: This endpoint retrieve the inventory status of product e.g. out of stock, available
* ***`getupdate`***: This endpoint track changes over time

## Database

All these endpoint use the msql database and relationship between tables
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
alembic --name dev upgrade head
```

To get the demo data of tables

```sh
mysql -u mac -p forsit < dump.sql
```

## Infrastructure

![high level FastAPI diagram](assets/FastApi.png?raw=true)

## Deployment


*NOTE: not all services are converted to the new method yet*

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

To deploy this App

```bash
$ uvicorn main:app --reload
```


