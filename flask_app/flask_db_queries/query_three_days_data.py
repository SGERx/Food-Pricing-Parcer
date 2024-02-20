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
def flask_three_days_data():
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT * 
    FROM products 
    WHERE datetime >= CURRENT_DATE - INTERVAL '3 days'
    ORDER BY shop, category, price, price_real;
    ''')
    today_data = cursor.fetchall()
    if len(today_data) == 0:
        print("Нет данных за последние три дня - произведите повторный парсинг")
    return today_data