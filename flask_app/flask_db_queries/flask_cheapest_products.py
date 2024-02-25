from flask_app.config import connection
from loguru import logger

def flask_cheapest():
    logger.info("Запуск функции {func}", func="flask_cheapest")
    logger.info("Создание курсора")
    cursor = connection.cursor()
    logger.info("Выполнение SQL-запроса для проверки наличия данных")
    cursor.execute(f'''
    SELECT * 
    FROM products 
    WHERE datetime >= CURRENT_DATE - INTERVAL '3 days';
    ''')
    logger.info("Проверка даты")
    check_data = cursor.fetchall()
    logger.info(len(check_data))
    if len(check_data) == 0:
        logger.info("Нет данных за последние три дня - произведите повторный парсинг")
    else:
        logger.info("Выполнение SQL-запроса для сбора данных о наиболее дешевых продуктах по категориям")
        cursor.execute(f'''
        select * from products where price IN
        (select min(price) from products
        group by category) and  datetime >= CURRENT_DATE - INTERVAL '3 days';
        ''')
        logger.info("Сбор данных")
        data = cursor.fetchall()
        logger.info("Закрытие курсора")
        cursor.close()
        logger.info("Завершение функции {func}", func="flask_cheapest")
        return data

