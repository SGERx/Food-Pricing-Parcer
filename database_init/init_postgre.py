from datetime import datetime

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

connection = psycopg2.connect("user=postgres password=root host=localhost port=5433")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
cursor.execute(sql.SQL("CREATE DATABASE products_postgres"))

DATABASE_URL = 'postgresql://postgres:root@localhost:5433/products_postgres'

engine = create_engine(DATABASE_URL)

Base = declarative_base()



class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime(timezone=True))
    shop = Column(String(50))
    category = Column(String(50))
    product_name = Column(String(200))
    price = Column(Integer)
    volume = Column(String(20))
    price_real = Column(Integer)

    # def __repr__(self):
    #     return "<Product(datetime='{}', shop='{}', category={}, product_name={}, price={}, volume={}, price_real={})>" \
    #         .format(self.datetime, self.shop, self.category, self.product_name, self.price, self.volume,
    #                 self.price_real)

    def __repr__(self):
        return '<Product %r>' % self.id


class Parsing(Base):
    __tablename__ = 'parsing'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(200))

    # def __repr__(self):
    #     return "<Product(datetime='{}', shop='{}', category={}, product_name={}, price={}, volume={}, price_real={})>" \
    #         .format(self.datetime, self.shop, self.category, self.product_name, self.price, self.volume,
    #                 self.price_real)

    def __repr__(self):
        return '<Product %r>' % self.id


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

current_session = Session()

test_product = Product(
    datetime=datetime.now(),
    shop='test_shop',
    category='test_category',
    product_name='test_product',
    price=777,
    volume='10 л',
    price_real=100
)

current_session.add(test_product)
current_session.commit()

current_session.close()
