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


def flask_expensive():
    cursor = connection.cursor()
    cursor.execute(f'''
        SELECT * 
    FROM products 
    WHERE datetime >= CURRENT_DATE - INTERVAL '3 days';
    ''')
    check_data = cursor.fetchall()
    print(len(check_data))
    if len(check_data) == 0:
        print("Нет данных за последние три дня - произведите повторный парсинг")
    else:
        # Выбираем все данные
        cursor.execute(f'''
        select * from products where price IN
        (select max(price) from products
        group by category) and  datetime >= CURRENT_DATE - INTERVAL '3 days';
        ''')

        data = cursor.fetchall()
        print(data)
        # cursor.close()
        # connection.close()
        return data
