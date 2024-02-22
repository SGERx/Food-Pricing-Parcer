from datetime import timezone, datetime

import psycopg2

dt = datetime.now(timezone.utc)

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
        cursor.execute(f'''
        select * from products where price IN
        (select max(price) from products
        group by category) and  datetime >= CURRENT_DATE - INTERVAL '3 days';
        ''')

        data = cursor.fetchall()
        print(data)
        return data

