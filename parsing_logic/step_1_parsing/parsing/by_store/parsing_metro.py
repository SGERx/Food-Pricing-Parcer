import time

from selenium.common import NoSuchElementException

from parsing_logic.step_1_parsing.parsing.parsing_logic import input_parsing, random_sleep, open_page, product_cards_parcing, write_to_csv, driver

from selenium.webdriver.common.by import By


url = "https://online.metro-cc.ru/"
searchbar_xpath = "//input[@class='search-bar__input reset-input']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//button[@class='search-bar__button search-bar__button--clear']"
prodcards_xpath = "//div[@class='product-card__top']/a"
title_xpath = "//h1[@class='product-page-content__product-name catalog-heading heading__h2']/span"
price_xpath = "//span[@class='product-price__sum-rubles'][1]"
csv_name = "metro"


def change_address():
    time.sleep(10)
    try:
        addressvologda = driver.find_element(By.XPATH, "//button[@class='rectangle-button reset--button-styles action-button apply-button blue lg normal wide']")
        print("Адрес неправильный, предлагают сменить, убираем окно")
        addressvologda.click()
    except NoSuchElementException as exc:
        print(exc)

    time.sleep(10)
    address = driver.find_element(By.XPATH, "//button[@class='header-address__receive-button offline']")
    address.click()
    random_sleep()
    addressbar = driver.find_element(By.XPATH, "//input[@class='reset-input obtainment-delivery__input']")
    addressbar.send_keys("Москва, улица Свободы, 71к2")
    random_sleep()
    savebutton = driver.find_element(By.XPATH, "//button[@class='rectangle-button reset--button-styles obtainment-delivery__apply-btn-desktop blue lg normal wide']")
    print("Нашли кнопку смены адреса")
    savebutton.click()
    print("Кликнули кнопку смены адреса")
    savebutton.click()
    print("Кликнули кнопку смены адреса еще раз")
    print("Адрес сменен")
    time.sleep(10)


def flask_metro():
    try:
        product_list = input_parsing()
        print(product_list)
        open_page(url)
        change_address()
        print('Сейчас будем парсить')
        full_dict = product_cards_parcing(product_list, searchbar_xpath, main_page_button_xpath, clear_button_xpath,
                                          prodcards_xpath, title_xpath, price_xpath)
        write_to_csv(full_dict, csv_name)
        print(f"Конец теста")
    except:
        print("FLASK_METRO ERROR")


with driver:
    if __name__ == '__main__':
        product_list = input_parsing()
        print(product_list)
        open_page(url)
        change_address()
        print('Сейчас будем парсить')
        full_dict = product_cards_parcing(product_list, searchbar_xpath, main_page_button_xpath, clear_button_xpath,
                                          prodcards_xpath, title_xpath, price_xpath)
        write_to_csv(full_dict, csv_name)
        print(f"Конец теста")
        time.sleep(1000)
