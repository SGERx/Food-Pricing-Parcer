import time
from parsing_logic.step_1_parsing.parsing.parsing_logic import input_parsing, open_page, product_cards_parcing, write_to_csv

url = "https://shop.miratorg.ru/"
searchbar_xpath = "//input[@class='bx-form-control js-search-extend input-field__search']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//a[@class='DOESNTEXIST']"
prodcards_xpath = "//div[@class='col-lg-3 col-md-4 col-sm-6 col-xs-12']/child::div/child::div/child::a"
title_xpath = "//h1[@class='h1']"
price_xpath = '//div[@class="card-price"]/div/ul/li/div/span[2]'
csv_name = "miratorg"


def flask_miratorg():
    try:
        product_list = input_parsing()
        print(product_list)
        open_page(url)
        print('Сейчас будем парсить')
        full_dict = product_cards_parcing(product_list, searchbar_xpath, main_page_button_xpath, clear_button_xpath,
                                          prodcards_xpath, title_xpath, price_xpath)
        write_to_csv(full_dict, csv_name)
        print(f"Конец теста")
    except:
        print("FLASK_MIRATORG ERROR")

if __name__ == '__main__':
    product_list = input_parsing()
    print(product_list)
    open_page(url)
    print('Сейчас будем парсить')
    full_dict = product_cards_parcing(product_list, searchbar_xpath, main_page_button_xpath, clear_button_xpath,
                                      prodcards_xpath, title_xpath, price_xpath)
    write_to_csv(full_dict, csv_name)
    print(f"Конец теста")
    time.sleep(1000)
