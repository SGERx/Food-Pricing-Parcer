from data_conversion_logic.main_clean_data import main_clean_data
from loguru import logger

name = "vprok"


def flask_clean_data_vprok():
    logger.info("Запуск функции {func}", func="flask_clean_data_vprok")
    main_clean_data(name)
    logger.info("Завершение функции {func}", func="flask_clean_data_vprok")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="clean_data_vprok.py")
    main_clean_data(name)
    logger.info("Завершение файла {file} через __main__", file="clean_data_vprok.py")
