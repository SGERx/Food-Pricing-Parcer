from data_conversion_logic.main_clean_data import main_clean_data
from loguru import logger

name = "vkusvill"


def flask_clean_data_vkusvill():
    """Вызов функции main_clean_data() для очистки и конвертации данных Vkusvill"""
    logger.info("Запуск функции {func}", func="flask_clean_data_vkusvill")
    main_clean_data(name)
    logger.info("Завершение функции {func}", func="flask_clean_data_vkusvill")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="clean_data_vkusvill.py")
    main_clean_data(name)
    logger.info("Завершение файла {file} через __main__", file="clean_data_vkusvill.py")
