from parsing_logic.parse_all import parse_all
from loguru import logger

url = "https://vkusvill.ru"
searchbar_xpath = "//input[@type='text']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//button[@class='HeaderSearchBlock__BtnClear js-vv21-search__clear-search _active']"
prodcards_xpath = "//div[@class='ProductCard__content']/child::a"
title_xpath = "//h1[@class='Product__title js-datalayer-catalog-list-name']"
price_xpath = "//span[contains(@class, 'Price Price')]"
csv_name = "vkusvill"
error_text = "FLASK_VKUSVILL ERROR"
current_adress_xpath = "//span[@class='HeaderATDToggler__Text rtext _desktop-md _tablet-sm _mobile-sm']"
address_selection_button_xpath = None
select_address_from_list_xpath = None
address_input_xpath = "//textarea[@class='VV_Input__Input js-vv-control__input']"

address_input_value = "Москва, улица Свободы, 71к3"

address_final_confirmation_button_xpath = "//a[@class='VV_Button _desktop-lg _tablet-md _mobile-md _block']"


def flask_vkusvill():
    """Запуск парсинга для магазина Vkusvill"""
    logger.info("Запуск функции {func}", func="flask_vkusvill")
    try:
        parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
                  price_xpath, csv_name, error_text, current_adress_xpath, address_selection_button_xpath,
                  select_address_from_list_xpath,
                  address_input_xpath, address_input_value, address_final_confirmation_button_xpath)
    except Exception as e:
        logger.critical(f"критическая ошибка парсинга магазина Vkusvill - {e}")
    logger.info("Завершение функции {func}", func="flask_vkusvill")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="parsing_vkusvill.py")
    flask_vkusvill()
    logger.info("Завершение файла {file} через __main__", file="parsing_vkusvill.py")
