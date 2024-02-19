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


def flask_cheapest():
    cursor = connection.cursor()
    cursor.execute(f'''
    select * from products where datetime - '{dt}' < '1 day';
    ''')
    check_data = cursor.fetchall()
    print(len(check_data))
    if len(check_data) == 0:
        print('Нет данных за сегодняшнюю дату, используйте скрипт query_all_data.py для выгрузки всех данных и ручного '
              'просмотра')
    else:
        # Выбираем все данные
        cursor.execute(f'''
        select * from products where price IN
        (select min(price) from products
        group by category) and  datetime - '{dt}' < '1 day';
        ''')

        data = cursor.fetchall()
        print(data)
        return data

    # Закрываем соединение
    # cursor.close()
    # connection.close()
