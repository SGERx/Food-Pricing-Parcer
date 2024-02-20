from flask import Flask, g
import psycopg2

connection = psycopg2.connect(database="products_postgres", user="postgres", password="root", host="localhost",
                              port=5433)


def truncate_table_parsing():
    print('Вызов функции удаления таблицы parsing')
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT
    pg_terminate_backend(pg_stat_activity.pid)
    FROM
    pg_stat_activity
    WHERE
    pg_stat_activity.datname = 'products_postgres'
    AND
    pg_stat_activity.pid <> pg_backend_pid();
    ''')
    cursor.execute(f'''
    TRUNCATE TABLE parsing;
    ''')
    if 'products_postgres' not in g:
        g.db = psycopg2.connect(database='products_postgres', user='postgres', password='root', host='localhost',
                                port='5433')
    return g.db


def truncate_table_products():
    print('Вызов функции удаления таблицы products')

    new_connection = psycopg2.connect(database='products_postgres', user='postgres', password='root', host='localhost',
                                      port='5433')

    cursor = new_connection.cursor()
    cursor.execute('TRUNCATE TABLE products;')
    new_connection.commit()
    cursor.close()
    new_connection.close()

    return new_connection

