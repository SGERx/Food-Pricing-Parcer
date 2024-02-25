import csv
import json
import os
import shutil
import time
from datetime import datetime

from loguru import logger


def jsonify_data(shop_name):
    """Проводит очистку и запись данных в JSON"""
    logger.info("Запуск функции {func}", func="jsonify_data")
    data_json = {}
    current_date = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Рассчитанная текущая дата - {current_date}")
    path = f"../data/b_data_output/{current_date}_{shop_name}.csv"
    logger.info(f"Путь к CSV для создания JSON - {path}")
    if not os.path.exists(path):
        logger.info("Файл этого магазина с текущей датой не существует! Требуется повторный парсинг!")
    else:
        logger.info("Файл магазина с текущей датой найден, начинаем считывание")
        with open(f"../data/b_data_output/{current_date}_{shop_name}.csv", newline='', encoding='utf-8-sig') as csvfile:
            data_csv = csv.reader(csvfile, delimiter=',')
            next(data_csv)
            for row in data_csv:
                product_shop, product_name, product_price = f'{shop_name}_' + row[0], row[1], row[2]
                product_price_clean, product_volume = map(
                    lambda x: x.replace('(', '').replace(')', '').replace('\'', '').strip(), product_price.split(','))

                product_price_calculated = ''
                if product_volume == '':
                    product_price_calculated = ''
                elif 'мл' in product_volume:
                    product_price_calculated = round(
                        round(float(product_price_clean) / float(product_volume.replace('мл', '').strip()), 4) * 1000,
                        2)
                elif 'кг' in product_volume:
                    try:
                        product_price_calculated = round(
                            float(product_price_clean) / (float(product_volume.replace('кг', '').strip())), 2)
                    except ValueError as e:
                        product_volume = '1 кг'
                        product_price_calculated = round(
                            float(product_price_clean) / (float(product_volume.replace('кг', '').strip())), 2)
                elif 'г' in product_volume and 'кг' not in product_volume:
                    product_price_calculated = round(
                        round(float(product_price_clean) / float(product_volume.replace('г', '').strip()), 4) * 1000, 2)
                elif 'л' in product_volume and 'мл' not in product_volume:
                    try:
                        product_price_calculated = round(
                            float(product_price_clean) / (float(product_volume.replace('л', '').strip())), 2)
                    except ArithmeticError as e:
                        product_volume.replace('л', '1 л')
                        product_price_calculated = round(
                            float(product_price_clean) / (float(product_volume.replace('л', '').strip())), 2)
                elif 'шт' in product_volume:
                    product_price_calculated = product_price_clean
                if product_shop not in data_json:
                    data_json[product_shop] = []
                data_json[product_shop].append(
                    [product_name, product_price_clean, product_volume, product_price_calculated])
            current_date = datetime.now().strftime("%Y-%m-%d")
            logger.info(f"Повторно рассчитанная текущая дата для записи JSON- {current_date}")
            path = f"../data/c_data_clean/clean_data_json/{current_date}_{shop_name}.json"
            logger.info(f"Путь для записи JSON- {path}")
            if not os.path.exists(path):
                logger.info("Создание JSON")
                open(path, "w").close()
            with open(f'../data/c_data_clean/clean_data_json/{current_date}_{shop_name}.json', 'w',
                      encoding='utf-8') as file:
                json.dump(data_json, file, indent=4, ensure_ascii=False)
                logger.info("Запись JSON завершена")
        time.sleep(1)
        try:
            logger.info("Перемещаем исходный CSV-файл в папку archived_csv")
            source_dir = f"../data/b_data_output/"
            target_dir = f"../data/b_data_output/archived_csv/"
            file_name = f"{current_date}_{shop_name}.csv"
            shutil.move(os.path.join(source_dir, file_name), target_dir)
        except Exception as e:
            logger.info(f"Ошибка перемещения файла в архив: {e}")
        logger.info("Завершение функции {func}", func="jsonify_data")
        return data_json


def write_to_csv(shop_name, json_data):
    """Проводит запись данных в CSV на основе очищенного JSON"""
    logger.info("Запуск функции {func}", func="write_to_csv")
    if json_data is not None:
        logger.info("В функцию write_to_csv был передан входящий JSON-файл")
        current_date = datetime.now().strftime("%Y-%m-%d")
        logger.info(f"Рассчитанная текущая дата для записи CSV- {current_date}")
        path = f"../data/c_data_clean/clean_data_csv/{current_date}_{shop_name}.csv"
        logger.info(f"Путь для записи CSV- {path}")
        if not os.path.exists(path):
            logger.info(f"Создание файла CSV")
            open(path, "w").close()
        with open(f'../data/c_data_clean/clean_data_csv/{current_date}_{shop_name}.csv', 'w', newline='',
                  encoding='utf-8-sig') as file:
            logger.info(f"Начало записи файла CSV")
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Категория', 'Наименование', 'Цена', 'Вес/Объем', 'Цена за единицу объема'])
            for category, products in json_data.items():
                dummy, category = category.split('_')
                for product in products:
                    writer.writerow([category] + product)
    else:
        logger.info(f"JSON не возвращен")
    logger.info("Завершение функции {func}", func="write_to_csv")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="main_clean_output_data.py")
    logger.info("Функция CleanDataLogic не имеет своего кода, запуск производится из файла конкретного магазина")
    logger.info(f"Функция CleanDataLogic не имеет своего кода, запуск производится из файла конкретного магазина")
    time.sleep(10)
