from flask_app.config import connection
from loguru import logger


def flask_price_real():
    logger.info("Запуск функции {func}", func="flask_price_real")
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
    if len(check_data) == 0:
        logger.info("Нет данных за последние три дня - произведите повторный парсинг")
    else:
        logger.info("Выполнение SQL-запроса для сбора данных о реальной цене")
        cursor.execute(f'''
        WITH min_prices AS (
        SELECT
        shop,
        category,
        MIN(price_real) as min_real_price
        FROM
        products WHERE datetime >= CURRENT_DATE - INTERVAL '3 days'
        GROUP BY
        shop, category
        )
        SELECT
        shop,
        SUM(min_real_price) as total_price
        FROM
        min_prices
        GROUP BY
        shop
        ORDER BY total_price ASC;
        ''')

        logger.info("Сбор данных")
        data = cursor.fetchall()
        logger.info("Закрытие курсора")
        cursor.close()
        logger.info("Завершение функции {func}", func="flask_price_real")
        return data


