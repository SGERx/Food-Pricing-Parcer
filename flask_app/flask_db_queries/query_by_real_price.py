import datetime
import os
import sqlite3
import csv

import openpyxl
import pandas as pd
import psycopg2

from datetime import timezone, timedelta, datetime


dt = datetime.now(timezone.utc)

# Устанавливаем соединение с базой данных
connection = psycopg2.connect(database="products_postgres", user="postgres", password="root", host="localhost",
                              port=5433)


# Проверяем данные за сегодняшнюю дату
def flask_price_real():
    cursor = connection.cursor()
    cursor.execute(f'''
        SELECT * 
    FROM products 
    WHERE datetime >= CURRENT_DATE - INTERVAL '3 days';
    ''')
    check_data = cursor.fetchall()
    if len(check_data) == 0:
        print("Нет данных за последние три дня - произведите повторный парсинг")
    else:
        # Выбираем данные
        cursor.execute(f'''
        WITH min_prices AS (
        SELECT
        shop,
        category,
        MIN(price_real) as min_real_price
        FROM
        products WHERE datetime >= CURRENT_DATE - INTERVAL '3 days'
        GROUP BY
        shop, category
        )
        SELECT
        shop,
        SUM(min_real_price) as total_price
        FROM
        min_prices
        GROUP BY
        shop
        ORDER BY total_price ASC;
        ''')

        data = cursor.fetchall()
        print(data)
        # cursor.close()
        # connection.close()
        return data


