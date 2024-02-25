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
from loguru import logger
from flask_app.models import Parsing

options = uc.ChromeOptions()

options.user_data_dir = "c:\\temp\\profile"

options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
driver = uc.Chrome(options=options)


def input_parsing():
    """Считывание входных данных о продуктах для парсинга"""
    logger.info("Запуск функции {func}", func="input_parsing")
    read_csv_path = "../data/a_data_input/product_list.csv"
    logger.info(f"Файл продуктов для считывания - {read_csv_path}")
    product_list_inner = []
    parsing = Parsing.query.all()
    if len(parsing) > 0:
        logger.info("На сайте присутствуют продукты для парсинга, будут использоваться данные из сайта")
        for parse in parsing:
            product_raw = parse.product_name
            product_list_inner.append(product_raw)
        logger.info(f"Финальный список продуктов для парсинга - {product_list_inner}")
    else:
        logger.info("На сайте отсутствуют продукты для парсинга, будут использоваться данные из файла")
        products_raw = pandas.read_csv(read_csv_path, encoding='ANSI')
        products = products_raw["product"]
        product_list_inner = []
        logger.info(f"Список продуктов для парсинга - {products}")
        for product in products:
            product_list_inner.append(product)
        logger.info(f"Финальный список продуктов для парсинга - {product_list_inner}")
    logger.info("Завершение функции {func}", func="input_parsing")
    return product_list_inner


def random_sleep():
    """Функция для бездействия в целях имитации человека"""
    logger.info("Запуск функции {func}", func="random_sleep")
    t = random.randint(10, 15)
    time.sleep(t)
    logger.info("Завершение функции {func}", func="random_sleep")


def open_page(url):
    """Открытие страницы магазина"""
    logger.info("Запуск функции {func}", func="open_page")
    logger.info(f"open_page - Открытие страницы {url}")
    driver.get(url)
    logger.info(f"open_page - Страница {url} открыта")
    logger.info("Завершение функции {func}", func="open_page")


def change_address():
    """Смена адреса"""
    logger.info("Запуск функции {func}", func="change_address")
    time.sleep(1000)
    logger.info("Завершение функции {func}", func="change_address")


def product_cards_parcing(prod_list, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath,
                          title_xpath, price_xpath):
    """Парсинг сайта"""
    logger.info("Запуск функции {func}", func="product_cards_parcing")
    random_sleep()
    general_dictionary = {}
    logger.info('Начало процесса парсинга')
    for prod in prod_list:
        logger.info(f"Глобальный поиск продукта")
        logger.info(f'Ищем строку поиска - {searchbar_xpath}')
        searchbar = driver.find_element(By.XPATH, searchbar_xpath)
        searchbar.send_keys(" ")
        searchbar.clear()
        searchbar.click()
        time.sleep(3)
        try:
            logger.info(f'Ищем main_page_button - {main_page_button_xpath}')
            main_page_button = driver.find_element(By.XPATH, main_page_button_xpath)
            logger.info("Пытаемся кликнуть main_page_button")
            main_page_button.click()
        except Exception as e:
            logger.info(f'Не нашли или не нажали main_page_button, исключение - {e}')
            time.sleep(5)
            logger.info("Проверяем кнопку очистки на дополнительное проверочное значение (хардкод)")
            if clear_button_xpath == "//button[@class='HeaderSearchBlock__BtnClear js-vv21-search__clear-search _active']":
                searchbar.send_keys("a")
                time.sleep(5)
                searchbar.send_keys("b")
                time.sleep(5)
                searchbar.send_keys("c")
                time.sleep(5)
            time.sleep(5)
            logger.info(f"Ищем кнопку очистки - {clear_button_xpath}")
            clear_button = driver.find_element(By.XPATH, clear_button_xpath)
            time.sleep(3)
            logger.info("Кликаем кнопку очистки")
            clear_button.click()
        time.sleep(3)
        logger.info(f"Ищем строку поиска - {searchbar_xpath}")
        searchbar = driver.find_element(By.XPATH, searchbar_xpath)
        random_sleep()
        logger.info("Вносим продукт в строку поиска")
        searchbar.send_keys(f"{prod}")
        logger.info("Подтверждаем поиск клавишей ENTER")
        searchbar.send_keys(Keys.ENTER)
        random_sleep()
        logger.info(f"Повторно ищем строку поиска - {searchbar_xpath}")
        searchbar = driver.find_element(By.XPATH, searchbar_xpath)
        logger.info("Очищаем строку поиска")
        searchbar.clear()
        random_sleep()
        prod_urls = []
        product_titles = []
        product_prices = []
        product_volumes = []
        logger.info(f"Собираем информацию о карточках продукта - {prodcards_xpath}")
        prodcards = driver.find_elements(By.XPATH, prodcards_xpath)
        for prodcard in prodcards:
            prod_url = prodcard.get_attribute("href")
            logger.info(f"Собираем ссылку с карточки продукта - {prod_url}")
            prod_urls.append(prod_url)

        if len(prod_urls) > 10:
            logger.info("Карточек продуктов больше десяти, берем первые n значений (хардкод)")
            prod_urls_sliced = prod_urls[:2]
        else:
            logger.info("Карточек продуктов меньше десяти, берем все")
            prod_urls_sliced = prod_urls
        for prod_url_slice in prod_urls_sliced:
            logger.info(f"Переходим на карточку продукта {prod_url_slice}")
            i = 0
            random_sleep()
            driver.get(prod_url_slice)
            random_sleep()
            logger.info(f"Ищем заголовок в карточке продукта {title_xpath}")
            title = driver.find_element(By.XPATH, title_xpath)
            title_text = title.text
            logger.info(f"Нашли заголовок в карточке продукта, исходный текст - {title_text}")
            title_text = title_text.replace(',', '.')
            title_text.strip()
            logger.info("Очищаем заголовок в карточке продукта")
            match = re.search(r"(\b\d+(?:[\.,]\d+)?\s?(?:л|мл|г|шт|кг)\b)", title_text)
            if match:
                volume_text = match.group(1)
                title_text = re.sub(r"(\d+(?:[\.,]\d+)?\s?(?:л|мл|г|шт|кг))", "", title_text).strip()
                product_volumes.append(volume_text)
                logger.info(f"Объем из заголовка - {volume_text}")
            else:
                volume_text = ""
                logger.info("Объем в заголовке не указан")
            logger.info(f"Очищенный заголовок в карточке продукта - {title_text}")
            logger.info(f'Ищем цену по элементу - {price_xpath}')
            price = driver.find_element(By.XPATH, price_xpath)
            logger.info('Цена найдена')
            price_text_raw = price.text
            logger.info(f'Неочищенная цена - {price_text_raw}')
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
                    logger.info(f'WEIGHT BEFORE: {weight}')
                    volume_text = f"{volume_text} {weight.strip().replace(',', '').replace('.', '')}"
                    logger.info(f'WEIGHT AFTER: {weight}')
                    logger.info(volume_text)
                else:
                    title_text = title_text
                price_text_clean = price_text_clean.strip()
                price_text_clean = price_text_clean.replace(',', '.')

            if title_text.endswith('.'):
                title_text = title_text[:-1]

            logger.info(f'Очищенная цена - {price_text_clean}')
            logger.info(f'Title: {title_text}')
            logger.info(f'Price: {price_text_clean}')
            logger.info(f'Volume: {volume_text}')
            product_titles.append(title_text)
            product_prices.append(str(round(float(price_text_clean))))
            product_volumes.append(volume_text)

            driver.back()
            random_sleep()
            i = i + 1
            logger.info(f'Цикл поиска - {i}')
        logger.info(f'Итоговый список заголовков - {product_titles}')
        logger.info(f'Итоговый список цен - {product_prices}')
        if len(product_titles) == 0 and len(product_prices) == 0:
            logger.info('Заголовки и цены отсутствуют')
            product_titles.append('NO_RESULTS')
            product_prices.append('NO_RESULTS')

        product_cards_inner_dictionary = dict(zip(product_titles, zip(product_prices, product_volumes)))
        logger.info(f'Словарь с карточками продуктов - {product_cards_inner_dictionary}')
        general_dictionary.update({prod: product_cards_inner_dictionary})
        logger.info(f'Итоговый общий словарь - {general_dictionary}')
    logger.info("Завершение функции {func}", func="product_cards_parcing")
    return general_dictionary


def write_to_csv(data, csv_name):
    """Запись результатов парсинга в CSV-файл"""
    logger.info("Запуск функции {func}", func="write_to_csv")
    current_date = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Рассчитанная текущая дата - {current_date}")
    path = f"../data/b_data_output/{current_date}_{csv_name}.csv"
    logger.info(f"Имя CSV-файла с результатами парсинга - {current_date}")
    logger.info("Создаем файл")
    if not os.path.exists(path):
        open(path, "w").close()
    logger.info("Запись данных в файл")
    with open(path, mode='w', encoding='utf-8-sig',
              newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['Search product', 'Product Title', 'Product Price and unit'])

        for k, v in data.items():
            for k1, v1 in v.items():
                writer.writerow([k, k1, v1])
    logger.info("Завершение функции {func}", func="write_to_csv")


if __name__ == '__main__':
    logger.info("Функция main не имеет своего кода, запуск производится из файла конкретного магазина")
    time.sleep(5)
