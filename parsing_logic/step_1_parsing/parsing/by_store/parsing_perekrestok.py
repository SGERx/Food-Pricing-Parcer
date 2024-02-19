import time
from parsing_logic.step_1_parsing.parsing.parsing_logic import input_parsing, open_page, product_cards_parcing, \
    write_to_csv

url = "https://www.perekrestok.ru"
searchbar_xpath = "//input[@class='Input__InputStyled-sc-1kqlv3u-0 caFtVc']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//button[@class='sc-eCstlR jeYPke search-form__button search-form__button-clear']"
prodcards_xpath = "//a[@class='product-card__link']"
title_xpath = "//h1[@class='sc-fubCzh ibFUIH product__title']"
price_xpath = "//div[@class='price-card-unit-value']"
csv_name = "perekrestok"


def flask_perekrestok():
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
        print("FLASK_PEREKRESTOK ERROR")


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
