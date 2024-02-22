import json
import os
import shutil
import time
import csv
from datetime import datetime


def jsonify_data(shop_name):
    data_json = {}
    current_date = datetime.now().strftime("%Y-%m-%d")
    path = f"../data/b_data_output/{current_date}_{shop_name}.csv"
    if not os.path.exists(path):
        print('Файл этого магазина с текущей датой не существует! Требуется повторный парсинг!')
    else:
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
            path = f"../data/c_data_clean/clean_data_json/{current_date}_{shop_name}.json"
            if not os.path.exists(path):
                open(path, "w").close()
            with open(f'../data/c_data_clean/clean_data_json/{current_date}_{shop_name}.json', 'w',
                      encoding='utf-8') as file:
                json.dump(data_json, file, indent=4, ensure_ascii=False)
        time.sleep(1)
        try:
            source_dir = f"../data/b_data_output/"
            target_dir = f"../data/b_data_output/archived_csv/"
            file_name = f"{current_date}_{shop_name}.csv"
            shutil.move(os.path.join(source_dir, file_name), target_dir)
        except Exception as e:
            print(f"Ошибка перемещения файла в архив: {e}")
        return data_json


def write_to_csv(shop_name, json_data):
    if json_data is not None:
        current_date = datetime.now().strftime("%Y-%m-%d")
        path = f"../data/c_data_clean/clean_data_csv/{current_date}_{shop_name}.csv"
        if not os.path.exists(path):
            open(path, "w").close()
        with open(f'../data/c_data_clean/clean_data_csv/{current_date}_{shop_name}.csv', 'w', newline='',
                  encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')

            writer.writerow(['Категория', 'Наименование', 'Цена', 'Вес/Объем', 'Цена за единицу объема'])
            for category, products in json_data.items():
                dummy, category = category.split('_')
                for product in products:
                    writer.writerow([category] + product)
    else:
        print("JSON не возвращен")


if __name__ == '__main__':
    print("Функция CleanDataLogic не имеет своего кода, запуск производится из файла конкретного магазина")
    time.sleep(10)
