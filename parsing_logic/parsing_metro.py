from parsing_logic.parse_all import parse_all

url = "https://online.metro-cc.ru/"
searchbar_xpath = "//input[@class='search-bar__input reset-input']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//button[@class='search-bar__button search-bar__button--clear']"
prodcards_xpath = "//div[@class='product-card__top']/a"
title_xpath = "//h1[@class='product-page-content__product-name catalog-heading heading__h2']/span"
price_xpath = "//span[@class='product-price__sum-rubles'][1]"
csv_name = "metro"
error_text = "FLASK_METRO ERROR"


def flask_metro():
    parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text)


if __name__ == '__main__':
    flask_metro()
