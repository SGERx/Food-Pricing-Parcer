import time
from parsing_logic.step_1_parsing.parsing.parsing_logic import input_parsing, open_page, product_cards_parcing, \
    write_to_csv

url = "https://online.globus.ru/"
searchbar_xpath = "//input[@class='search']"
main_page_button_xpath = '//a[@href="/"]'
clear_button_xpath = "//div[@id='js-clear-btn']"
prodcards_xpath = "//div[@class='d-col d-col_xs_4 d-col_xtr_3 js-catalog-section__item ']/child::div/child::div/child::a"
title_xpath = "//h1[@class='js-with-nbsp-after-digit']"
price_xpath = '//div[@class="item-card__wrapper--top clearfix"]/div/div[2]/div/span/span/span'
csv_name = "globus"


def flask_globus():
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
        print("FLASK_GLOBUS ERROR")


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
