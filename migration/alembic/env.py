from logging.config import fileConfig
from os import environ

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from dotenv import load_dotenv

load_dotenv()


from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

import sys, os
parent_dir = os.path.join(os.path.abspath(os.getcwd()), '..')
print(parent_dir)
sys.path.append(parent_dir)
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
# from mysqlBase import *
from utils.models import *
target_metadata = Base.metadata

DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASSWORD")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_DATABASE = environ.get("DB_DATABASE")


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    section = config.get_section(config.config_ini_section)



    url = section["sqlalchemy.url"].format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DATABASE)
    section["sqlalchemy.url"] = url


    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    section = config.get_section(config.config_ini_section)
    url = section["sqlalchemy.url"].format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DATABASE)
    section["sqlalchemy.url"] = url



    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )


    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
