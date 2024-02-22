import glob
import json
import os
import shutil
from datetime import datetime, timezone

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, Session


def write_to_db_postgres():
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

    json_folder = '../data/d_data_analyse/*.json'
    json_files = glob.glob(json_folder)
    for file_path in json_files:
        with open(file_path, encoding='utf-8-sig') as f:
            content = f.read()
            if len(content) == 0:
                print("Файл пуст")
                exit()
            try:
                print("Пытаемся открыть файл")
                datas = json.loads(content)
                print(datas)
                for data in datas:
                    info = Product(
                        datetime=datetime_now_with_zone,
                        shop=data[1],
                        category=data[2],
                        product_name=data[3],
                        price=round(int(data[4]), 0),
                        volume=data[5],
                        price_real=round(int(data[6]), 0),
                    )
                    session.add(info)
            except json.JSONDecodeError as e:
                print("Ошибка при чтении JSON:", str(e))

    session.commit()
    session.close()

    source_dir = f"../data/d_data_analyse/"
    target_dir = f"../data/d_data_analyse/wrote_to_db/"

    file_names = os.listdir(source_dir)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)


if __name__ == '__main__':
    write_to_db_postgres()
