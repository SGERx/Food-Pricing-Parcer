from parsing_logic.parse_all import parse_all
from loguru import logger

url = "https://dostavka.magnit.ru"
searchbar_xpath = "//input[@class='m-input__input m-input-search__input m-input-text__input']"
main_page_button_xpath = "//a[@class='m-navigation-link--active m-navigation__link--dostavka m-navigation-link']"
clear_button_xpath = "//button[@class='m-button-close m-input-text__clearable is-rounded m-button-icon']"
prodcards_xpath = "//div[@class='product__container product_border product__container--narrow']/child::a"
title_xpath = "//h1[@class='m-page-header__title text--h1']"
price_xpath = "//div[contains(@class, 'm-price__current')]"
csv_name = "magnit"
error_text = "FLASK_MAGNIT ERROR"
current_adress_xpath = None
address_selection_button_xpath = "//div[@class='select-address__inner']"
# address_selection_button_xpath="//div[@class='m-tooltip__trigger']"
select_address_from_list_xpath = None
address_input_xpath = "//input[@class='m-input-text__input']"
address_input_value = None
address_final_confirmation_button_xpath = "//span[@class='m-button__label']"


def flask_magnit():
    """Запуск парсинга для магазина Magnit"""
    logger.info("Запуск функции {func}", func="flask_magnit")
    try:
        parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
                  price_xpath, csv_name, error_text, current_adress_xpath, address_selection_button_xpath,
                  select_address_from_list_xpath,
                  address_input_xpath, address_input_value, address_final_confirmation_button_xpath)
    except Exception as e:
        logger.critical(f"критическая ошибка парсинга магазина Magnit - {e}")
    logger.info("Завершение функции {func}", func="flask_magnit")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="parsing_magnit.py")
    flask_magnit()
    logger.info("Завершение файла {file} через __main__", file="parsing_magnit.py")
