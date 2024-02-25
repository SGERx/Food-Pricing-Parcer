from parsing_logic.parse_all import parse_all
from loguru import logger


url = "https://shop.miratorg.ru/"
searchbar_xpath = "//input[@class='bx-form-control js-search-extend input-field__search']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//a[@class='DOESNTEXIST']"
prodcards_xpath = "//div[@class='col-lg-3 col-md-4 col-sm-6 col-xs-12']/child::div/child::div/child::a"
title_xpath = "//h1[@class='h1']"
price_xpath = '//div[@class="card-price"]/div/ul/li/div/span[2]'
csv_name = "miratorg"
error_text = "FLASK_MIRATORG ERROR"


def flask_miratorg():
    """Запуск парсинга для магазина Miratorg"""
    logger.info("Запуск функции {func}", func="flask_miratorg")
    parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text)
    logger.info("Завершение функции {func}", func="flask_miratorg")


if __name__ == '__main__':
    logger.info("Запуск файла {file} через __main__", file="parsing_miratorg.py")
    flask_miratorg()
    logger.info("Завершение файла {file} через __main__", file="parsing_miratorg.py")
