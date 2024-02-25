import glob
import json
import os
import shutil
from datetime import date, datetime
from loguru import logger


def create_json():
    """Проводит дополнительную очистку JSON и записывает в единый JSON"""
    logger.info("Запуск функции {func}", func="create_json")
    json_folder = '../data/c_data_clean/clean_data_json/*.json'
    logger.info(f"Папка с файлами JSON - {json_folder}")
    json_files = glob.glob(json_folder)
    logger.info(f"Файлы JSON - {json_files}")

    final_data = []

    for file in json_files:
        with open(file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            if len(content) > 0:
                try:
                    data = json.loads(content)
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    for key, values in data.items():
                        for value in values:
                            store, category = key.split('_')
                            name = value[0]
                            price = str(value[1])
                            quantity = value[2]
                            real_price = value[3]
                            new_key = current_datetime
                            new_value = [current_datetime, store, category, name, price, quantity, real_price]
                            final_data.append(new_value)
                            logger.info(f"финальный список: {final_data}")
                except json.JSONDecodeError as e:
                    logger.error(f"Ошибка при чтении JSON из файла {file}: {str(e)}")
            else:
                logger.info(f"Файл {file} пустой")

    new_data_json = json.dumps(final_data, ensure_ascii=False)

    output_file = f'../data/d_data_analyse/{date.today()}_united_json_for_db.json'
    logger.info(f"Выходной файл - {output_file}")
    with open(output_file, 'w', encoding='utf-8-sig') as outfile:
        logger.info(f"начинаем запись файла {output_file}")
        outfile.write(new_data_json)

    source_dir = f"../data/c_data_clean/clean_data_json/"
    target_dir = f"../data/c_data_clean/archived_json/"

    file_names = os.listdir(source_dir)
    logger.info(f"Начинаем перемещение исходных файлов из папки {source_dir} в папку {target_dir}")
    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    logger.info("Завершение функции {func}", func="create_json")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="main_create_united_json.py")
    create_json()
    logger.info("Завершение файла {file} через __main__", file="main_create_united_json.py")
