import time
from parsing_logic.step_1_parsing.parsing.parsing_logic import input_parsing, open_page, product_cards_parcing, \
    write_to_csv

url = "https://www.auchan.ru"
searchbar_xpath = "//input[@class='form__field-input css-1c2y9he digi-instant-search jc-ignore']"
main_page_button_xpath = "//a[@class='css-jodbou']"
clear_button_xpath = "//a[@class='DOESNTEXIST']"
prodcards_xpath = "//div[@class='digi-product']/child::a"
title_xpath = "//h1[@class='css-1dud7uh']"
price_xpath = '//div[@class="fullPricePDP css-5ig8q6"]'
csv_name = "auchan"


def flask_auchan():
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
        print("FLASK_AUCHAN ERROR")


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
