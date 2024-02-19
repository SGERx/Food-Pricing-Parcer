import glob
import json
import random
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

DATABASE_URI = 'postgresql://postgres:root@localhost:5433/products_postgres'


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    shop = Column(String(50))
    category = Column(String(50))
    product_name = Column(String(200))
    price = Column(Integer)
    volume = Column(String(20))
    price_real = Column(Float)

    def __repr__(self):
        return "<Product(datetime='{}', shop='{}', category={}, product_name={}, price={}, volume={}, price_real={})>" \
            .format(self.datetime, self.shop, self.category, self.product_name, self.price, self.volume,
                    self.price_real)


engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
session = Session(engine)

current_session = Session()
datetime_now_with_zone = datetime.now(timezone.utc)

test_category_data = ['Моколо', 'Яйца', 'Хлеб', 'Гречка', 'Рис', 'Курица', 'Индейка', 'Чай']
test_shop_data = ['auchan', 'globus', 'magnit', 'metro', 'miratorg', 'perekrestok', 'vkusvill', 'vprok']

for i in range(0, 1000):
    info = Product(
        datetime=datetime_now_with_zone,
        shop=test_shop_data[random.randint(0, 7)],
        category=test_category_data[random.randint(0, 7)],
        product_name=f"test_product_name_{i}",
        price=round(int(i), 0),
        volume=f"{i} л",
        price_real=round((int(i)+random.randint(0, 7)), 0),
    )
    session.add(info)

session.commit()
session.close()
