import datetime
import os
import sqlite3
import csv

import openpyxl
import pandas as pd
import psycopg2

from datetime import timezone, timedelta, datetime


# Устанавливаем соединение с базой данных
connection = psycopg2.connect(database="products_postgres", user="postgres", password="root", host="localhost",
                              port=5433)


# Проверяем данные за сегодняшнюю дату
def flask_category_price_data():
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
        WITH ranked_products AS (
          SELECT
            shop,
            category,
            product_name,
            price,
            ROW_NUMBER() OVER (PARTITION BY shop, category ORDER BY price) as row_num
          FROM
            products
          WHERE
            datetime >= CURRENT_DATE - INTERVAL '3 days'
        )
        SELECT
          shop,
          category,
          product_name,
          price
        FROM
          ranked_products
        WHERE
          row_num = 1
        ORDER BY
          shop, category;
        ''')

        data = cursor.fetchall()
        print(data)
        # cursor.close()
        # connection.close()
        return data

