from parsing_logic.parse_all import parse_all

url = "https://www.auchan.ru"
searchbar_xpath = "//input[@class='form__field-input css-1c2y9he digi-instant-search jc-ignore']"
main_page_button_xpath = "//a[@class='css-jodbou']"
clear_button_xpath = "//a[@class='DOESNTEXIST']"
prodcards_xpath = "//div[@class='digi-product']/child::a"
title_xpath = "//h1[@class='css-1dud7uh']"
price_xpath = '//div[@class="fullPricePDP css-5ig8q6"]'
csv_name = "auchan"
error_text = "FLASK_AUCHAN ERROR"


def flask_auchan():
    parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text)


if __name__ == '__main__':
    flask_auchan()