

from sqlalchemy import  Column, Integer, Text, String, \
    DateTime, ForeignKey, Table

from sqlalchemy.orm import relationship



# this is imported from AWS layer, locally it would not be found so will fail on 'chalice package'/'chalice deploy'
try:
    from mysqlalchemy_base import Base
except ImportError:
    import sys

    sys.path.append("../..")  # Adds higher directory to python modules path.
    from mysqlBase import Base

######################
# atomic db models
######################




class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category_name = Column(Text)



class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer,primary_key=True)
    name = Column(String(32))
    description = Column(Text)
    price = Column(Integer)

    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship("Category", foreign_keys=[category_id])
class Sales(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    date = Column(DateTime)

    product_id = Column(Integer, ForeignKey(Product.id))
    product = relationship("Product", foreign_keys=[product_id])


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    Quantity = Column(Integer)
    min_quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey(Product.id))
    product = relationship("Product", foreign_keys=[product_id])


class InventoryLog(Base):
    __tablename__ = 'inventory_log'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    status = Column(String(32))
    update_date = Column(DateTime)
    inventory_id = Column(Integer, ForeignKey(Inventory.id))
    inventory = relationship("Inventory", foreign_keys=[inventory_id])












