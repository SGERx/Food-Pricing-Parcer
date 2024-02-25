from loguru import logger

from parsing_logic.main_parsing_logic import input_parsing, open_page, product_cards_parcing, write_to_csv, \
    change_address


def parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text, current_adress_xpath, address_selection_button_xpath,
              select_address_from_list_xpath,
              address_input_xpath, address_input_value, address_final_confirmation_button_xpath):
    """Функция, вызываемая для запуска парсинга - добавлена в рефакторинге"""
    logger.info("Запуск функции {func}", func="parse_all")
    try:
        logger.info("Попытка выполнения функции parse_all")
        product_list = input_parsing()
        open_page(url)
        change_address(current_adress_xpath, address_selection_button_xpath, select_address_from_list_xpath,
                       address_input_xpath, address_input_value, address_final_confirmation_button_xpath)
        full_dict = product_cards_parcing(product_list, searchbar_xpath, main_page_button_xpath, clear_button_xpath,
                                          prodcards_xpath, title_xpath, price_xpath)
        write_to_csv(full_dict, csv_name)
        logger.info(f"Конец теста")
    except Exception as e:
        logger.info(f"Ошибка выполнения, исключение {e}")
        logger.info(error_text)
    logger.info("Завершение функции {func}", func="parse_all")
