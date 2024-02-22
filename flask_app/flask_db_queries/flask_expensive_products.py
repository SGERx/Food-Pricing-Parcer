from flask_app.config import connection


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
        cursor.close()
        return data

