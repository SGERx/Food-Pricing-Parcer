import time
from parsing_logic.step_1_parsing.parsing.parsing_logic import input_parsing, open_page, product_cards_parcing, write_to_csv

url = "https://vkusvill.ru"
searchbar_xpath = "//input[@type='text']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//button[@class='HeaderSearchBlock__BtnClear js-vv21-search__clear-search _active']"
prodcards_xpath = "//div[@class='ProductCard__content']/child::a"
title_xpath = "//h1[@class='Product__title js-datalayer-catalog-list-name']"
price_xpath = "//span[contains(@class, 'Price Price')]"
csv_name = "vkusvill"


def flask_vkusvill():
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
        print("FLASK_VKUSVILL ERROR")


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
