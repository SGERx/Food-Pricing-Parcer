from loguru import logger

from data_conversion_logic.main_clean_output_data import jsonify_data, write_to_csv


def main_clean_data(name):
    logger.info("Запуск функции {func}", func="main_clean_data")
    json_data = jsonify_data(name)
    write_to_csv(name, json_data)
    logger.info(f"очистка и запись данных по {name} завершена в JSON и CSV")
    logger.info("Завершение функции {func}", func="main_clean_data")
