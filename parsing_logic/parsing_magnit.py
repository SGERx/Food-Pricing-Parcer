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


def flask_magnit():
    logger.info("Запуск функции {func}", func="flask_magnit")
    parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text)
    logger.info("Завершение функции {func}", func="flask_magnit")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="parsing_magnit.py")
    flask_magnit()
    logger.info("Завершение файла {file} через __main__", file="parsing_magnit.py")
