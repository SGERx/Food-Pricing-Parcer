from loguru import logger

from data_conversion_logic.main_clean_data import main_clean_data

name = "auchan"


def flask_clean_data_auchan():
    """Вызов функции main_clean_data() для очистки и конвертации данных Auchan"""
    logger.info("Запуск функции {func}", func="flask_clean_data_auchan")
    main_clean_data(name)
    logger.info("Завершение функции {func}", func="flask_clean_data_auchan")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="clean_data_auchan.py")
    main_clean_data(name)
    logger.info("Завершение файла {file} через __main__", file="clean_data_auchan.py")
