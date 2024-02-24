import glob
import json
import os
import shutil
from datetime import datetime, timezone
from loguru import logger
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, Session


def write_to_db_postgres():
    logger.info("Запуск функции {func}", func="write_to_db_postgres")
    Base = declarative_base()

    DATABASE_URI = 'postgresql://postgres:root@localhost:5433/products_postgres'
    logger.info(f"Адрес БД - {DATABASE_URI}")

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

    datetime_now_with_zone = datetime.now(timezone.utc)
    logger.info(f"Рассчет текущего времени - {datetime_now_with_zone}")
    json_folder = '../data/d_data_analyse/*.json'
    logger.info(f"Папка JSON - {json_folder}")
    logger.info("Начинаем сбор файлов JSON для записи в БД")
    json_files = glob.glob(json_folder)
    logger.info("Сбор файлов JSON для записи в БД завершен")
    logger.info("Начинаем считывание файлов JSON для записи в БД")
    for file_path in json_files:
        with open(file_path, encoding='utf-8-sig') as f:
            content = f.read()
            if len(content) == 0:
                logger.info("Файл пуст")
                exit()
            try:
                logger.info("Пытаемся открыть файл")
                datas = json.loads(content)
                logger.info(f"Считанные из JSON данные - {datas}")
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
                    logger.info("Добавляем данные в сессию")
                    session.add(info)
            except json.JSONDecodeError as e:
                logger.error("Ошибка при чтении JSON:", str(e))

    logger.info("Применяем внесенные изменения")
    session.commit()
    logger.info("Закрываем сессию")
    session.close()
    source_dir = f"../data/d_data_analyse/"
    target_dir = f"../data/d_data_analyse/wrote_to_db/"
    logger.info(f"Производим перемещение записанных данных из папки {source_dir} в папку {target_dir}")
    file_names = os.listdir(source_dir)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    logger.info("Перемещение записанных файлов JSON завершено")
    logger.info("Завершение функции {func}", func="write_to_db_postgres")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="write_to_db_postgre.py")
    write_to_db_postgres()
    logger.info("Завершение файла {file} через __main__", file="write_to_db_postgre.py")
