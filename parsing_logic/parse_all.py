from parsing_logic.main_parsing_logic import input_parsing, open_page, product_cards_parcing, write_to_csv, driver
from loguru import logger


def parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text):
    logger.info("Запуск функции {func}", func="parse_all")
    try:
        logger.info("Попытка выполнения функции parse_all")
        product_list = input_parsing()
        open_page(url)
        full_dict = product_cards_parcing(product_list, searchbar_xpath, main_page_button_xpath, clear_button_xpath,
                                          prodcards_xpath, title_xpath, price_xpath)
        write_to_csv(full_dict, csv_name)
        logger.info(f"Конец теста")
    except Exception as e:
        logger.info(f"Ошибка выполнения, исключение {e}")
        logger.info(error_text)
    logger.info("Завершение функции {func}", func="parse_all")
