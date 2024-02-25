from parsing_logic.parse_all import parse_all
from loguru import logger

url = "https://www.auchan.ru"
searchbar_xpath = "//input[@class='form__field-input css-1c2y9he digi-instant-search jc-ignore']"
main_page_button_xpath = "//a[@class='css-jodbou']"
clear_button_xpath = "//a[@class='DOESNTEXIST']"
prodcards_xpath = "//div[@class='digi-product']/child::a"
title_xpath = "//h1[@class='css-1dud7uh']"
price_xpath = '//div[@class="fullPricePDP css-5ig8q6"]'
csv_name = "auchan"
error_text = "FLASK_AUCHAN ERROR"
current_adress_xpath = "//button[@id='currentRegionName']"
address_selection_button_xpath = "//select[@id='regions']"
# address_selection_button_xpath="//select[@class='active css-10y9q5l']"
select_address_from_list_xpath = None
address_input_xpath = None
address_input_value = None
address_final_confirmation_button_xpath = "//button[@id='selectShop']"


def flask_auchan():
    """Запуск парсинга для магазина Auchan"""
    logger.info("Запуск функции {func}", func="flask_auchan")
    try:
        parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
                  price_xpath, csv_name, error_text, current_adress_xpath, address_selection_button_xpath,
                  select_address_from_list_xpath,
                  address_input_xpath, address_input_value, address_final_confirmation_button_xpath)
    except Exception as e:
        logger.critical(f"критическая ошибка парсинга магазина Auchan - {e}")
    logger.info("Завершение функции {func}", func="flask_auchan")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="parsing_auchan.py")
    flask_auchan()
    logger.info("Завершение файла {file} через __main__", file="parsing_auchan.py")
