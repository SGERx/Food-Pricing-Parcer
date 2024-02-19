import time
from parsing_logic.step_1_parsing.parsing.parsing_logic import input_parsing, open_page, product_cards_parcing, \
    write_to_csv

url = "https://dostavka.magnit.ru"
searchbar_xpath = "//input[@class='m-input__input m-input-search__input m-input-text__input']"
main_page_button_xpath = "//a[@class='m-navigation-link--active m-navigation__link--dostavka m-navigation-link']"
clear_button_xpath = "//button[@class='m-button-close m-input-text__clearable is-rounded m-button-icon']"
prodcards_xpath = "//div[@class='product__container product_border product__container--narrow']/child::a"
title_xpath = "//h1[@class='m-page-header__title text--h1']"
price_xpath = "//div[contains(@class, 'm-price__current')]"
csv_name = "magnit"


def flask_magnit():
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
        print("FLASK_MAGNIT ERROR")


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
