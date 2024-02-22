from flask_app.config import connection


def flask_today_data():
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT * 
    FROM products 
    WHERE datetime >= CURRENT_DATE - INTERVAL '1 day'
    ORDER BY shop, category, price, price_real;
    ''')
    today_data = cursor.fetchall()
    if len(today_data) == 0:
        print("Нет данных за сегодня - произведите повторный парсинг")
    cursor.close()
    return today_data