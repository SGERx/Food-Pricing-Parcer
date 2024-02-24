from flask_app.config import connection
from loguru import logger


def flask_category_real_price_data():
    logger.info("Запуск функции {func}", func="flask_category_real_price_data")
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
        logger.info("Выполнение SQL-запроса для сбора данных о реальных ценах по категориям")
        cursor.execute(f'''
        WITH ranked_products AS (
          SELECT
            shop,
            category,
            product_name,
            price_real,
            ROW_NUMBER() OVER (PARTITION BY shop, category ORDER BY price_real) as row_num
          FROM
            products
          WHERE
            datetime >= CURRENT_DATE - INTERVAL '3 days'
        )
        SELECT
          shop,
          category,
          product_name,
          price_real
        FROM
          ranked_products
        WHERE
          row_num = 1
        ORDER BY
          shop, category;
        ''')

        logger.info("Сбор данных")
        data = cursor.fetchall()
        logger.info("Закрытие курсора")
        cursor.close()
        logger.info("Завершение функции {func}", func="flask_category_real_price_data")
        return data
