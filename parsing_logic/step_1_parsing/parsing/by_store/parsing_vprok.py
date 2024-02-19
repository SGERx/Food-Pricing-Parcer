import time
from parsing_logic.step_1_parsing.parsing.parsing_logic import input_parsing, open_page, product_cards_parcing, \
    write_to_csv

url = "https://www.vprok.ru"
searchbar_xpath = "//input[@class='Input_input__couZC']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//svg[@class='Input_clear__iom_A']"
prodcards_xpath = "//article[contains(@class, MainProductTile_root)]/child::a"
title_xpath = "//h1[contains(@class, Title_title__)]"
price_xpath = "//span[contains(@class, 'Price_price__')]"
csv_name = "vprok"


def flask_vprok():
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
        print("FLASK_VPROK ERROR")


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
