import atexit
import random
import re
import pandas
import undetected_chromedriver as uc
import time
import csv
import os
from datetime import datetime
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from flask_app.models import Parsing

options = uc.ChromeOptions()

options.user_data_dir = "c:\\temp\\profile"

options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
driver = uc.Chrome(options=options)

# TODO
atexit.register(driver.quit)


def input_parsing():
    read_csv_path = "../data/a_data_input/product_list.csv"
    product_list_inner = []
    parsing = Parsing.query.all()
    if len(parsing) > 0:
        for parse in parsing:
            product_raw = parse.product_name
            product_list_inner.append(product_raw)
    else:
        products_raw = pandas.read_csv(read_csv_path, encoding='ANSI')
        products = products_raw["product"]
        product_list_inner = []
        for product in products:
            product_list_inner.append(product)
    return product_list_inner


def random_sleep():
    t = random.randint(10, 15)
    time.sleep(t)


def open_page(url):
    print(f'Сейчас будет открытие в старом файле')
    print(f"open_page - Открытие страницы {url}")
    driver.get(url)
    print(f"open_page - Страница {url} открыта")


def change_address():
    time.sleep(1000)


def product_cards_parcing(prod_list, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath,
                          title_xpath, price_xpath):
    print('Начали парсить')
    random_sleep()
    general_dictionary = {}
    print('Начали парсить уже совсем')
    for prod in prod_list:
        print(f"Глобальный поиск продукта")
        print('Ищем строку поиска')
        searchbar = driver.find_element(By.XPATH, searchbar_xpath)
        searchbar.send_keys(" ")
        searchbar.clear()
        searchbar.click()
        time.sleep(3)
        try:
            main_page_button = driver.find_element(By.XPATH, main_page_button_xpath)
            main_page_button.click()
        except Exception as e:
            time.sleep(5)
            if clear_button_xpath == "//button[@class='HeaderSearchBlock__BtnClear js-vv21-search__clear-search _active']":
                searchbar.send_keys("a")
                time.sleep(5)
                searchbar.send_keys("b")
                time.sleep(5)
                searchbar.send_keys("c")
                time.sleep(5)
            time.sleep(5)
            clear_button = driver.find_element(By.XPATH, clear_button_xpath)
            time.sleep(3)
            clear_button.click()
        time.sleep(3)
        searchbar = driver.find_element(By.XPATH, searchbar_xpath)
        random_sleep()
        searchbar.send_keys(f"{prod}")
        searchbar.send_keys(Keys.ENTER)
        random_sleep()
        searchbar = driver.find_element(By.XPATH, searchbar_xpath)
        searchbar.clear()
        random_sleep()
        prod_urls = []
        product_titles = []
        product_prices = []
        product_volumes = []
        prodcards = driver.find_elements(By.XPATH, prodcards_xpath)
        for prodcard in prodcards:
            prod_url = prodcard.get_attribute("href")
            prod_urls.append(prod_url)

        if len(prod_urls) > 10:
            prod_urls_sliced = prod_urls[:2]
        else:
            prod_urls_sliced = prod_urls
        for prod_url_slice in prod_urls_sliced:
            i = 0
            random_sleep()
            driver.get(prod_url_slice)
            random_sleep()

            title = driver.find_element(By.XPATH, title_xpath)
            title_text = title.text
            title_text = title_text.replace(',', '.')
            title_text.strip()

            match = re.search(r"(\b\d+(?:[\.,]\d+)?\s?(?:л|мл|г|шт|кг)\b)", title_text)
            if match:
                volume_text = match.group(1)
                title_text = re.sub(r"(\d+(?:[\.,]\d+)?\s?(?:л|мл|г|шт|кг))", "", title_text).strip()
                product_volumes.append(volume_text)
            else:
                volume_text = ""
            print('price parsing start')
            price = driver.find_element(By.XPATH, price_xpath)
            print('price parsing end')
            price_text_raw = price.text
            print(f'raw price - {price_text_raw}')
            if '/' not in price_text_raw:
                price_text_clean = re.sub(r'[^0-9.,]', '', price_text_raw)
                price_text_clean = price_text_clean.replace(',', '.')
            else:
                price_text_clean, weight = price_text_raw.split('/')
                price_text_clean = price_text_clean.replace('₽', '')
                price_text_clean = price_text_clean.replace('руб', '')
                price_text_clean = price_text_clean.replace('р', '')
                price_text_clean = price_text_clean.replace('\n', '')

                if 'шт' not in weight:
                    print(f'WEIGHT BEFORE: {weight}')
                    volume_text = f"{volume_text} {weight.strip().replace(',', '').replace('.', '')}"
                    print(f'WEIGHT AFTER: {weight}')
                    print(volume_text)
                else:
                    title_text = title_text
                price_text_clean = price_text_clean.strip()
                price_text_clean = price_text_clean.replace(',', '.')

            if title_text.endswith('.'):
                title_text = title_text[:-1]

            print(f'clean price - {price_text_clean}')

            print(f'Title: {title_text}')
            print(f'Price: {price_text_clean}')
            print(f'Volume: {volume_text}')
            product_titles.append(title_text)
            product_prices.append(str(round(float(price_text_clean))))
            product_volumes.append(volume_text)

            driver.back()
            random_sleep()
            i = i + 1
            print(i)
        print(product_titles)
        print(product_prices)
        if len(product_titles) == 0 and len(product_prices) == 0:
            product_titles.append('NO_RESULTS')
            product_prices.append('NO_RESULTS')

        product_cards_inner_dictionary = dict(zip(product_titles, zip(product_prices, product_volumes)))
        print(product_cards_inner_dictionary)
        general_dictionary.update({prod: product_cards_inner_dictionary})
        print(general_dictionary)

    return general_dictionary


def write_to_csv(data, csv_name):

    current_date = datetime.now().strftime("%Y-%m-%d")
    path = f"../data/b_data_output/{current_date}_{csv_name}.csv"
    if not os.path.exists(path):
        open(path, "w").close()

    with open(path, mode='w', encoding='utf-8-sig',
              newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['Search product', 'Product Title', 'Product Price and unit'])

        for k, v in data.items():
            for k1, v1 in v.items():
                writer.writerow([k, k1, v1])




if __name__ == '__main__':
    print("Функция main не имеет своего кода, запуск производится из файла конкретного магазина")
    time.sleep(5)
