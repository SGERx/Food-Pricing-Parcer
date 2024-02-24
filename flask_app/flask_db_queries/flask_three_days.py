from flask_app.config import connection
from loguru import logger


def flask_three_days_data():
    logger.info("Запуск функции {func}", func="flask_three_days_data")
    logger.info("Создание курсора")
    cursor = connection.cursor()
    logger.info("Выполнение SQL-запроса для проверки наличия данных")
    cursor.execute(f'''
    SELECT * 
    FROM products 
    WHERE datetime >= CURRENT_DATE - INTERVAL '3 days'
    ORDER BY shop, category, price, price_real;
    ''')
    logger.info("Сбор данных")
    three_days_data = cursor.fetchall()
    if len(three_days_data) == 0:
        logger.info("Нет данных за последние три дня - произведите повторный парсинг")
    cursor.close()
    logger.info("Завершение функции {func}", func="flask_three_days_data")
    return three_days_data
