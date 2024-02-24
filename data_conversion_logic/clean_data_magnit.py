from loguru import logger

from data_conversion_logic.main_clean_data import main_clean_data

name = "magnit"


def flask_clean_data_magnit():
    logger.info("Запуск функции {func}", func="flask_clean_data_magnit")
    main_clean_data(name)
    logger.info("Завершение функции {func}", func="flask_clean_data_magnit")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="clean_data_magnit.py")
    main_clean_data(name)
    logger.info("Завершение файла {file} через __main__", file="clean_data_magnit.py")

