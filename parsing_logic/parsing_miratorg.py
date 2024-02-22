from parsing_logic.parse_all import parse_all


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
    parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text)

if __name__ == '__main__':
    flask_miratorg()
