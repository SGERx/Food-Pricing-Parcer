import os
import openpyxl
import psycopg2


def update_bill_price_xlsx():
    connection = psycopg2.connect(database="products_postgres", user="postgres", password="root", host="localhost",
                                  port=5433)
    cursor = connection.cursor()

    cursor.execute(f'''
    SELECT * 
    FROM products 
    WHERE datetime >= CURRENT_DATE - INTERVAL '3 days';
    ''')
    check_data = cursor.fetchall()
    if len(check_data) == 0:
        print("Нет данных за последние три дня - произведите повторный парсинг")
    else:
        cursor.execute(f'''
        WITH min_prices AS (
        SELECT
        shop,
        category,
        MIN(price) as min_price
        FROM
        products WHERE datetime >= CURRENT_DATE - INTERVAL '3 days'
        GROUP BY
        shop, category
        )
        SELECT
        shop,
        SUM(min_price) as total_price
        FROM
        min_prices
        GROUP BY
        shop
        ORDER BY total_price ASC;
        ''')

        rows = cursor.fetchall()
        print(rows)

        if not os.path.exists(f'../data/e_query_results/query_5-by_bill_price.xlsx'):
            with open(f'../data/e_query_results/query_5-by_bill_price.xlsx', 'w'):
                pass

        filepath = f'../data/e_query_results/query_5-by_bill_price.xlsx'
        workbook_create = openpyxl.Workbook()
        workbook_create.save(filepath)

        wb = openpyxl.load_workbook(f'../data/e_query_results/query_5-by_bill_price.xlsx')

        ws = wb.active

        ws.delete_cols(1, 100)
        ws.delete_rows(1, 3000)

        ws["A1"] = "shop"
        ws["B1"] = "sum_price"

        for row in rows:
            print(row[0], row[1])

        for i in range(0, len(rows)):
            ws[f"A{i + 2}"] = rows[i][0]
            ws[f"B{i + 2}"] = rows[i][1]

        wb.save(f'../data/e_query_results/query_5-by_bill_price.xlsx')

    # cursor.close()
    # connection.close()


if __name__ == '__main__':
    update_bill_price_xlsx()