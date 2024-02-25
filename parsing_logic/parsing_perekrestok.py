from parsing_logic.parse_all import parse_all
from loguru import logger

url = "https://www.perekrestok.ru"
searchbar_xpath = "//input[@class='Input__InputStyled-sc-1kqlv3u-0 caFtVc']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//button[@class='sc-eCstlR jeYPke search-form__button search-form__button-clear']"
prodcards_xpath = "//a[@class='product-card__link']"
title_xpath = "//h1[@class='sc-fubCzh ibFUIH product__title']"
price_xpath = "//div[@class='price-card-unit-value']"
csv_name = "perekrestok"
error_text = "FLASK_PEREKRESTOK ERROR"
current_adress_xpath = "//button[@class='sc-JAcba fhJUVj header-delivery-button__darken']"

address_selection_button_xpath = None
select_address_from_list_xpath = None
address_input_xpath = "//input[@id='react-select-3-input']"

address_input_value = "Москва, улица свободы дом 71к3"

address_final_confirmation_button_xpath = "//button[@class='sc-eCstlR ftZPut delivery-status__submit']"


def flask_perekrestok():
    """Запуск парсинга для магазина Perekrestok"""
    logger.info("Запуск функции {func}", func="flask_perekrestok")
    try:
        parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
                  price_xpath, csv_name, error_text, current_adress_xpath, address_selection_button_xpath,
                  select_address_from_list_xpath,
                  address_input_xpath, address_input_value, address_final_confirmation_button_xpath)
    except Exception as e:
        logger.critical(f"критическая ошибка парсинга магазина Perekrestok - {e}")
    logger.info("Завершение функции {func}", func="flask_perekrestok")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="parsing_perekrestok.py")
    flask_perekrestok()
    logger.info("Завершение файла {file} через __main__", file="parsing_perekrestok.py")
