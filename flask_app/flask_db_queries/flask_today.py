from flask_app.config import connection
from loguru import logger


def flask_today_data():
    logger.info("Запуск функции {func}", func="flask_today_data")
    logger.info("Создание курсора")
    cursor = connection.cursor()
    logger.info("Выполнение SQL-запроса для проверки наличия данных")
    cursor.execute(f'''
    SELECT * 
    FROM products 
    WHERE datetime >= CURRENT_DATE - INTERVAL '1 day'
    ORDER BY shop, category, price, price_real;
    ''')
    logger.info("Сбор данных")
    today_data = cursor.fetchall()
    if len(today_data) == 0:
        logger.info("Нет данных за сегодня - произведите повторный парсинг")
    logger.info("Закрытие курсора")
    cursor.close()
    logger.info("Завершение функции {func}", func="flask_today_data")
    return today_data
