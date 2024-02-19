import datetime
import os
import sqlite3
import csv

import openpyxl
import pandas as pd
import psycopg2

from datetime import timezone, timedelta, datetime

current_date = datetime.today().strftime('%Y-%m-%d')
current_date_timezoned = current_date + '+03'
dt = datetime.now(timezone.utc)

# Устанавливаем соединение с базой данных
connection = psycopg2.connect(database="products_postgres", user="postgres", password="root", host="localhost",
                              port=5433)


# Проверяем данные за сегодняшнюю дату
def flask_price_bill():
    cursor = connection.cursor()
    cursor.execute(f'''
    select * from products where datetime - '{dt}' < '1 day';
    ''')
    check_data = cursor.fetchall()
    if len(check_data) == 0:
        print("Нет данных за текущую дату", "Произведите повторный парсинг", "")
    else:
        # Выбираем данные
        cursor.execute(f'''
        SELECT SUM(price) AS total_price, SUM(price_real) AS total_price_real, shop
        FROM products
        WHERE id || ' ' || price_real IN (
            SELECT id || ' ' || MIN(price_real) 
            FROM products 
            WHERE shop = 'auchan' AND datetime - '{dt}' < INTERVAL '1 day'
            GROUP BY id
        )
        GROUP BY shop
        UNION
        SELECT SUM(price) AS total_price, SUM(price_real) AS total_price_real, shop
        FROM products
        WHERE id || ' ' || price_real IN (
            SELECT id || ' ' || MIN(price_real) 
            FROM products 
            WHERE shop = 'globus' AND datetime - '{dt}' < INTERVAL '1 day'
            GROUP BY id
        )
        GROUP BY shop
        UNION
        SELECT SUM(price) AS total_price, SUM(price_real) AS total_price_real, shop
        FROM products
        WHERE id || ' ' || price_real IN (
            SELECT id || ' ' || MIN(price_real) 
            FROM products 
            WHERE shop = 'magnit' AND datetime - '{dt}' < INTERVAL '1 day'
            GROUP BY id
        )
        GROUP BY shop
        UNION
        SELECT SUM(price) AS total_price, SUM(price_real) AS total_price_real, shop
        FROM products
        WHERE id || ' ' || price_real IN (
            SELECT id || ' ' || MIN(price_real) 
            FROM products 
            WHERE shop = 'metro' AND datetime - '{dt}' < INTERVAL '1 day'
            GROUP BY id
        )
        GROUP BY shop
        UNION
        SELECT SUM(price) AS total_price, SUM(price_real) AS total_price_real, shop
        FROM products
        WHERE id || ' ' || price_real IN (
            SELECT id || ' ' || MIN(price_real) 
            FROM products 
            WHERE shop = 'miratorg' AND datetime - '{dt}' < INTERVAL '1 day'
            GROUP BY id
        )
        GROUP BY shop
        UNION
        SELECT SUM(price) AS total_price, SUM(price_real) AS total_price_real, shop
        FROM products
        WHERE id || ' ' || price_real IN (
            SELECT id || ' ' || MIN(price_real) 
            FROM products 
            WHERE shop = 'perekrestok' AND datetime - '{dt}' < INTERVAL '1 day'
            GROUP BY id
        )
        GROUP BY shop
        UNION
        SELECT SUM(price) AS total_price, SUM(price_real) AS total_price_real, shop
        FROM products
        WHERE id || ' ' || price_real IN (
            SELECT id || ' ' || MIN(price_real) 
            FROM products 
            WHERE shop = 'vkusvill' AND datetime - '{dt}' < INTERVAL '1 day'
            GROUP BY id
        )
        GROUP BY shop
        UNION
        SELECT SUM(price) AS total_price, SUM(price_real) AS total_price_real, shop
        FROM products
        WHERE id || ' ' || price_real IN (
            SELECT id || ' ' || MIN(price_real) 
            FROM products 
            WHERE shop = 'vprok' AND datetime - '{dt}' < INTERVAL '1 day'
            GROUP BY id
        )
        GROUP BY shop
        ORDER BY total_price ASC;
        ''')

        data = cursor.fetchall()
        print(data)
        return data

    # Закрываем соединение
    #     cursor.close()
    #     connection.close()
