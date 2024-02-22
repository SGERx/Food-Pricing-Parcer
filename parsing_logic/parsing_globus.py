from parsing_logic.parse_all import parse_all

url = "https://online.globus.ru/"
searchbar_xpath = "//input[@class='search']"
main_page_button_xpath = '//a[@href="/"]'
clear_button_xpath = "//div[@id='js-clear-btn']"
prodcards_xpath = "//div[@class='d-col d-col_xs_4 d-col_xtr_3 js-catalog-section__item ']/child::div/child::div/child::a"
title_xpath = "//h1[@class='js-with-nbsp-after-digit']"
price_xpath = '//div[@class="item-card__wrapper--top clearfix"]/div/div[2]/div/span/span/span'
csv_name = "globus"
error_text = "FLASK_GLOBUS ERROR"


def flask_globus():
    parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text)


if __name__ == '__main__':
    flask_globus()
