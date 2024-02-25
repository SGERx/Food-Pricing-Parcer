import csv
import os
import shutil
from datetime import date
from loguru import logger


def create_csv():
    """Объединяет CSV с данными разных магазинов в единый CSV. Исходники перемещаются в папку архива"""
    logger.info("Запуск функции {func}", func="create_csv")
    folder = f"../data/c_data_clean/clean_data_csv/"
    logger.info(f"Папка с исходными файлами - {folder}")
    today = date.today()
    logger.info(f"Сегодняшняя дата - {today}")
    files = os.listdir(folder)
    logger.info(f"Перечень файлов для объединения в единый CSV - {files}")
    csv_files = [file for file in files]
    logger.info(f"Список файлов для объединения в единый CSV - {csv_files}")
    output_file = f'../data/d_data_analyse/{today}_united_csv.csv'
    logger.info(f"Выходной единый CSV-файл - {output_file}")
    if not os.path.exists(output_file):
        open(output_file, "w").close()
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as outfile:
        logger.info("Начинаем запись CSV-файла")
        writer = csv.writer(outfile)
        for file in csv_files:
            file_path = os.path.join(folder, file)
            with open(file_path, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)

                writer.writerow(['Лист ' + file])
                writer.writerow([])

                for row in reader:
                    writer.writerow(row)
                    writer.writerow([])

    source_dir = f"../data/c_data_clean/clean_data_csv/"
    target_dir = f"../data/c_data_clean/archived_csv/"

    file_names = os.listdir(source_dir)
    logger.info(f"Начинаем перемещение исходных CSV-файлов из {source_dir} в {target_dir}")
    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    logger.info("Завершение функции {func}", func="create_csv")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="main_create_united_csv.py")
    create_csv()
    logger.info("Завершение файла {file} через __main__", file="main_create_united_csv.py")
