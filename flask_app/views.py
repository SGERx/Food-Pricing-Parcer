import os
import sys

from flask import send_from_directory, render_template, request, redirect, send_file
from loguru import logger

from data_conversion_logic.clean_data_auchan import flask_clean_data_auchan
from data_conversion_logic.clean_data_globus import flask_clean_data_globus
from data_conversion_logic.clean_data_magnit import flask_clean_data_magnit
from data_conversion_logic.clean_data_metro import flask_clean_data_metro
from data_conversion_logic.clean_data_miratorg import flask_clean_data_miratorg
from data_conversion_logic.clean_data_perekrestok import flask_clean_data_perekrestok
from data_conversion_logic.clean_data_vkusvill import flask_clean_data_vkusvill
from data_conversion_logic.clean_data_vprok import flask_clean_data_vprok
from data_conversion_logic.main_create_united_csv import create_csv
from data_conversion_logic.main_create_united_json import create_json
from data_conversion_logic.write_to_db_postgre import write_to_db_postgres
from flask_app.config import app, db
from flask_app.flask_db_queries.flask_category_price import flask_category_price_data
from flask_app.flask_db_queries.flask_category_real_price import flask_category_real_price_data
from flask_app.flask_db_queries.flask_cheapest_products import flask_cheapest
from flask_app.flask_db_queries.flask_expensive_products import flask_expensive
from flask_app.flask_db_queries.flask_price_bill import flask_price_bill
from flask_app.flask_db_queries.flask_real_price import flask_price_real
from flask_app.flask_db_queries.flask_three_days import flask_three_days_data
from flask_app.flask_db_queries.flask_today import flask_today_data
from flask_app.forms import ProductForm
from flask_app.models import Parsing
from flask_app.models import Product
from parsing_logic.parsing_auchan import flask_auchan
from parsing_logic.parsing_globus import flask_globus
from parsing_logic.parsing_magnit import flask_magnit
from parsing_logic.parsing_metro import flask_metro
from parsing_logic.parsing_miratorg import flask_miratorg
from parsing_logic.parsing_perekrestok import flask_perekrestok
from parsing_logic.parsing_vkusvill import flask_vkusvill
from parsing_logic.parsing_vprok import flask_vprok
from xlsx_update.xlsx_all_data import update_all_data_xlsx
from xlsx_update.xlsx_bill_price import update_bill_price_xlsx
from xlsx_update.xlsx_category_price import update_category_price_data_xlsx
from xlsx_update.xlsx_category_real_price import update_category__real_price_data_xlsx
from xlsx_update.xlsx_cheapest_products import update_cheapest_products_xlsx
from xlsx_update.xlsx_expensive_products import update_expensive_products
from xlsx_update.xlsx_real_price import update_real_price_xlsx
from xlsx_update.xlsx_three_days import update_three_days_data_xlsx
from xlsx_update.xlsx_today import update_today_data_xlsx

parsing = Parsing.query.all()


def parsing_in_progress():
    logger.info("Запуск функции {func}", func="parsing_in_progress")
    logger.info("Завершение функции {func}, вывод надписи 'PARSING IN PROGRESS...'", func="parsing_in_progress")
    return "PARSING IN PROGRESS..."


@app.route('/favicon.ico')
def favicon():
    logger.info("Запуск функции {func}", func="favicon")
    logger.info("Завершение функции {func}, передача картинки favicon.ico", func="favicon")
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# Header

@app.route('/')
@app.route('/home')
def my_index_view():
    logger.info("Запуск функции {func}", func="my_index_view")
    logger.info("Завершение функции {func}, рендеринг шаблона 'home.html'", func="my_index_view")
    return render_template("home.html", active_page='home')


@app.route('/product_list', methods=["POST", "GET"])
def product_list():
    logger.info("Запуск функции {func}", func="product_list")
    form = ProductForm()
    parsing = Parsing.query.all()
    if request.method == "POST":
        logger.info("/product_list - Метод запроса POST")
        if len(request.form['product_name']) == 0:
            logger.info("Внесите имя продукта, пустая форма не будет сохранена")
            return "Внесите имя продукта, пустая форма не будет сохранена"
        product_name = request.form['product_name']
        logger.info(f"Сохранен продукт для парсинга - {product_name}")
        parsing = Parsing(product_name=product_name)
        try:
            logger.info("Добавляем новый продукт в сессию")
            db.session.add(parsing)
            logger.info("Применяем добавление нового продукта")
            db.session.commit()
            logger.info("Завершение функции {func}, переадресация на '/product_list'", func="product_list")
            return redirect('/product_list')
        except Exception as e:
            logger.error(f"Ошибка внесения данных в базу, исключение {e}")
            return "Ошибка внесения данных в базу"
    else:
        logger.info("/product_list - Метод запроса GET")
        logger.info("Завершение функции {func}, рендеринг шаблона product_list.html", func="product_list")
        return render_template("product_list.html", form=form, parsing=parsing, active_page='product_list')


@app.route('/delete/<int:id>')
def delete(id):
    logger.info("Запуск функции {func}", func="/delete/<int:id>")
    parsing_obj = Parsing.query.get_or_404(id)
    try:
        logger.info("Попытка удаления объекта из базы данных")
        db.session.delete(parsing_obj)
        db.session.commit()
    except Exception as e:
        logger.error(f"Не удалось удалить объект, исключение {e}")
        return "Не удалось удалить объект"
    logger.info("Завершение функции {func}, переадресацию на '/product_list'", func="/delete/<int:id>")
    return redirect('/product_list')


@app.route('/parsing')
def parsing():
    logger.info("Запуск функции {func}", func="parsing")
    logger.info("Завершение функции {func}, рендеринг шаблона 'parsing.html'", func="parsing")
    return render_template("parsing.html", active_page='parsing')


# тестовая страница для запуска скриптов
@app.route('/parsing_all')
def parsing_all():
    logger.info("Запуск функции {func}", func="parsing_all")
    logger.info("Начало парсинга Auchan")
    flask_auchan()
    logger.info("Завершение парсинга Auchan")
    logger.info("Начало парсинга Globus")
    flask_globus()
    logger.info("Завершение парсинга Globus")
    logger.info("Начало парсинга Magnit")
    flask_magnit()
    logger.info("Завершение парсинга Magnit")
    logger.info("Начало парсинга Metro")
    flask_metro()
    logger.info("Завершение парсинга Metro")
    logger.info("Начало парсинга Miratorg")
    flask_miratorg()
    logger.info("Завершение парсинга Miratorg")
    logger.info("Начало парсинга Perekrestok")
    flask_perekrestok()
    logger.info("Завершение парсинга Perekrestok")
    logger.info("Начало парсинга Vkusvill")
    flask_vkusvill()
    logger.info("Завершение парсинга Vkusvill")
    logger.info("Начало парсинга Vprok")
    flask_vprok()
    logger.info("Завершение парсинга Vprok")

    logger.info("Начало очистки данных Auchan")
    flask_clean_data_auchan()
    logger.info("Начало очистки данных Globus")
    flask_clean_data_globus()
    logger.info("Начало очистки данных Magnit")
    flask_clean_data_magnit()
    logger.info("Начало очистки данных Metro")
    flask_clean_data_metro()
    logger.info("Начало очистки данных Miratorg")
    flask_clean_data_miratorg()
    logger.info("Начало очистки данных Perekrestok")
    flask_clean_data_perekrestok()
    logger.info("Начало очистки данных Vkusvill")
    flask_clean_data_vkusvill()
    logger.info("Начало очистки данных Vprok")
    flask_clean_data_vprok()

    logger.info("Начало создания CSV")
    create_csv()
    logger.info("Начало создания JSON")
    create_json()
    logger.info("Начало записи данных в БД")
    write_to_db_postgres()
    logger.info("Завершение функции {func}, переадресация на адрес '/parsing_complete'", func="parsing_all")
    return redirect('/parsing_complete')


@app.route('/parsing_auchan')
def parsing_auchan():
    logger.info("Запуск функции {func}", func="parsing_auchan")

    logger.info("Начало парсинга Auchan")
    flask_auchan()
    logger.info("Завершение парсинга Auchan")
    logger.info("Начало очистки данных Auchan")
    flask_clean_data_auchan()
    logger.info("Начало создания CSV")
    create_csv()
    logger.info("Начало создания JSON")
    create_json()
    logger.info("Начало записи данных в БД")
    write_to_db_postgres()
    logger.info("Завершение функции {func}, переадресация на адрес '/parsing_complete'", func="parsing_auchan")
    return redirect('/parsing_complete')


@app.route('/parsing_globus')
def parsing_globus():
    logger.info("Запуск функции {func}", func="parsing_globus")
    logger.info("Начало парсинга Globus")
    flask_globus()
    logger.info("Завершение парсинга Globus")
    logger.info("Начало очистки данных Globus")
    flask_clean_data_globus()
    logger.info("Начало создания CSV")
    create_csv()
    logger.info("Начало создания JSON")
    create_json()
    logger.info("Начало записи данных в БД")
    write_to_db_postgres()
    logger.info("Завершение функции {func}, переадресация на адрес '/parsing_complete'", func="parsing_globus")
    return redirect('/parsing_complete')


@app.route('/parsing_magnit')
def parsing_magnit():
    logger.info("Запуск функции {func}", func="parsing_magnit")
    logger.info("Начало парсинга Magnit")
    flask_magnit()
    logger.info("Завершение парсинга Magnit")
    logger.info("Начало очистки данных Magnit")
    flask_clean_data_magnit()
    logger.info("Начало создания CSV")
    create_csv()
    logger.info("Начало создания JSON")
    create_json()
    logger.info("Начало записи данных в БД")
    write_to_db_postgres()
    logger.info("Завершение функции {func}, переадресация на адрес '/parsing_complete'", func="parsing_magnit")
    return redirect('/parsing_complete')


@app.route('/parsing_metro')
def parsing_metro():
    logger.info("Запуск функции {func}", func="parsing_metro")
    logger.info("Начало парсинга Metro")
    flask_metro()
    logger.info("Завершение парсинга Metro")
    logger.info("Начало очистки данных Metro")
    flask_clean_data_metro()
    logger.info("Начало создания CSV")
    create_csv()
    logger.info("Начало создания JSON")
    create_json()
    logger.info("Начало записи данных в БД")
    write_to_db_postgres()
    logger.info("Завершение функции {func}, переадресация на адрес '/parsing_complete'", func="parsing_metro")
    return redirect('/parsing_complete')


@app.route('/parsing_miratorg')
def parsing_miratorg():
    logger.info("Запуск функции {func}", func="parsing_miratorg")
    logger.info("Начало парсинга Miratorg")
    flask_miratorg()
    logger.info("Завершение парсинга Miratorg")
    logger.info("Начало очистки данных Miratorg")
    flask_clean_data_miratorg()
    logger.info("Начало создания CSV")
    create_csv()
    logger.info("Начало создания JSON")
    create_json()
    logger.info("Начало записи данных в БД")
    write_to_db_postgres()
    logger.info("Завершение функции {func}, переадресация на адрес '/parsing_complete'", func="parsing_miratorg")
    return redirect('/parsing_complete')


@app.route('/parsing_perekrestok')
def parsing_perekrestok():
    logger.info("Запуск функции {func}", func="parsing_perekrestok")
    logger.info("Начало парсинга Perekrestok")
    flask_perekrestok()
    logger.info("Завершение парсинга Perekrestok")
    logger.info("Начало очистки данных Perekrestok")
    flask_clean_data_perekrestok()
    logger.info("Начало создания CSV")
    create_csv()
    logger.info("Начало создания JSON")
    create_json()
    logger.info("Начало записи данных в БД")
    write_to_db_postgres()
    logger.info("Завершение функции {func}, переадресация на адрес '/parsing_complete'", func="parsing_perekrestok")
    return redirect('/parsing_complete')


@app.route('/parsing_vkusvill')
def parsing_vkusvill():
    logger.info("Запуск функции {func}", func="parsing_vkusvill")
    logger.info("Начало парсинга Vkusvill")
    flask_vkusvill()
    logger.info("Завершение парсинга Vkusvill")
    logger.info("Начало очистки данных Vkusvill")
    flask_clean_data_vkusvill()
    logger.info("Начало создания CSV")
    create_csv()
    logger.info("Начало создания JSON")
    create_json()
    logger.info("Начало записи данных в БД")
    write_to_db_postgres()
    logger.info("Завершение функции {func}, переадресация на адрес '/parsing_complete'", func="parsing_vkusvill")
    return redirect('/parsing_complete')


@app.route('/parsing_vprok')
def parsing_vprok():
    logger.info("Запуск функции {func}", func="parsing_vprok")
    logger.info("Начало парсинга Vprok")
    flask_vprok()
    logger.info("Завершение парсинга Vprok")
    logger.info("Начало очистки данных Vprok")
    flask_clean_data_vprok()
    logger.info("Начало создания CSV")
    create_csv()
    logger.info("Начало создания JSON")
    create_json()
    logger.info("Начало записи данных в БД")
    write_to_db_postgres()
    logger.info("Завершение функции {func}, переадресация на адрес '/parsing_complete'", func="parsing_vprok")
    return redirect('/parsing_complete')


@app.route('/parsing_complete')
def parsing_complete():
    return render_template("parsing_complete.html", active_page='parsing_complete')


@app.route('/parsing_submenu')
def parsing_submenu():
    return render_template("parsing_submenu.html", active_page='parsing_submenu')


@app.route('/today_data')
def today_data():
    today_data = flask_today_data()
    return render_template("parsing_submenu_today_data.html", products=today_data, active_page='today_data')


@app.route('/three_days_data')
def three_days_data():
    three_days_data = flask_three_days_data()
    return render_template("parsing_submenu_today_data.html", products=three_days_data, active_page='three_days_data')


@app.route('/all_data')
def all_data():
    logger.info("Запуск функции {func}", func="all_data")
    products = Product.query.all()
    logger.info("Завершение функции {func}, рендеринг шаблона 'parsing_submenu_all_data.html'", func="all_data")
    return render_template("parsing_submenu_all_data.html", products=products, active_page='all_data')


@app.route('/category_price')
def category_price():
    logger.info("Запуск функции {func}", func="category_price")
    category_price_data = flask_category_price_data()
    logger.info("Завершение функции {func}, рендеринг шаблона 'parsing_submenu_category_price_data.html'", func="category_price")
    return render_template("parsing_submenu_category_price_data.html", products=category_price_data,
                           active_page='category_price')


@app.route('/category_real_price')
def category_real_price():
    logger.info("Запуск функции {func}", func="category_real_price")
    category_real_price_data = flask_category_real_price_data()
    logger.info("Завершение функции {func}, рендеринг шаблона 'parsing_submenu_category_real_price_data.html'", func="category_real_price")
    return render_template("parsing_submenu_category_real_price_data.html", products=category_real_price_data,
                           active_page='category_real_price')


@app.route('/price_bill')
def price_bill():
    logger.info("Запуск функции {func}", func="price_bill")
    bill_data = flask_price_bill()
    logger.info("Завершение функции {func}, рендеринг шаблона 'parsing_submenu_price_bill.html'", func="price_bill")
    return render_template("parsing_submenu_price_bill.html", products=bill_data, active_page='price_bill')


@app.route('/price_real')
def real_price():
    logger.info("Запуск функции {func}", func="real_price")
    real_data = flask_price_real()
    logger.info("Завершение функции {func}, рендеринг шаблона 'parsing_submenu_price_real.html'", func="real_price")
    return render_template("parsing_submenu_price_real.html", products=real_data, active_page='price_real')


@app.route('/products_cheapest')
def cheapest_products():
    logger.info("Запуск функции {func}", func="cheapest_products")
    cheap_data = flask_cheapest()
    logger.info("Завершение функции {func}, рендеринг шаблона 'parsing_submenu_products_cheapest.html'", func="cheapest_products")
    return render_template("parsing_submenu_products_cheapest.html", products=cheap_data,
                           active_page='products_cheapest')


@app.route('/products_expensive')
def expensive_products():
    logger.info("Запуск функции {func}", func="expensive_products")
    expensive_data = flask_expensive()
    logger.info("Завершение функции {func}, рендеринг шаблона 'parsing_submenu_products_expensive.html'", func="expensive_products")
    return render_template("parsing_submenu_products_expensive.html", products=expensive_data,
                           active_page='products_expensive')


@app.route('/download')
def download():
    logger.info("Запуск функции {func}", func="download")
    products = Product.query.all()
    logger.info("Завершение функции {func}, рендеринг шаблона 'parsing_submenu_download.html'", func="download")
    return render_template("parsing_submenu_download.html", products=products, active_page='download')


@app.route('/download_all_data')
def download_all_data():
    logger.info("Запуск функции {func}", func="download_all_data")
    update_all_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_0-all_data.xlsx"
    logger.info("Завершение функции {func}", func="download_all_data")
    return send_file(path, as_attachment=True)


@app.route('/download_three_days')
def download_three_days():
    logger.info("Запуск функции {func}", func="download_three_days")
    update_three_days_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_1-three_days_data.xlsx"
    logger.info("Завершение функции {func}", func="download_three_days")
    return send_file(path, as_attachment=True)


@app.route('/download_today')
def download_today():
    logger.info("Запуск функции {func}", func="download_today")
    update_today_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_2-today_data.xlsx"
    logger.info("Завершение функции {func}", func="download_today")
    return send_file(path, as_attachment=True)


@app.route('/download_category_by_price')
def download_category_by_price():
    logger.info("Запуск функции {func}", func="download_category_by_price")
    update_category_price_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_3-category_by_price.xlsx"
    logger.info("Завершение функции {func}", func="download_category_by_price")
    return send_file(path, as_attachment=True)


@app.route('/download_category_by_real_price')
def download_category_by_real_price():
    logger.info("Запуск функции {func}", func="download_category_by_real_price")
    update_category__real_price_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_4-category_by_real_price.xlsx"
    logger.info("Завершение функции {func}", func="download_category_by_real_price")
    return send_file(path, as_attachment=True)


@app.route('/download_price_bill')
def download_all_price_bill():
    logger.info("Запуск функции {func}", func="download_all_price_bill")
    update_bill_price_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_5-by_bill_price.xlsx"
    logger.info("Завершение функции {func}", func="download_all_price_bill")
    return send_file(path, as_attachment=True)


@app.route('/download_price_real')
def download_all_price_real():
    logger.info("Запуск функции {func}", func="download_all_price_real")
    update_real_price_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_6-by_real_price.xlsx"
    logger.info("Завершение функции {func}", func="download_all_price_real")
    return send_file(path, as_attachment=True)


@app.route('/download_products_cheapest')
def download_all_cheapest_products():
    logger.info("Запуск функции {func}", func="download_all_cheapest_products")
    update_cheapest_products_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_7-cheapest_products.xlsx"
    logger.info("Завершение функции {func}", func="download_all_cheapest_products")
    return send_file(path, as_attachment=True)


@app.route('/download_products_expensive')
def download_all_expensive_products():
    logger.info("Запуск функции {func}", func="download_all_expensive_products")
    update_expensive_products()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_8-expensive_products.xlsx"
    logger.info("Завершение функции {func}", func="download_all_expensive_products")
    return send_file(path, as_attachment=True)


@app.route('/download_readme')
def download_readme():
    logger.info("Запуск функции {func}", func="download_readme")
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/README.md"
    logger.info("Завершение функции {func}", func="download_readme")
    return send_file(path, as_attachment=True)


# Footer

@app.route('/info')
def info():
    logger.info("Запуск функции {func}", func="info")
    logger.info("Завершение функции {func}, рендеринг шаблона 'about.html'", func="info")
    return render_template("about.html", active_page='info')


@app.route('/readme')
def readme():
    logger.info("Запуск функции {func}", func="readme")
    logger.info("Завершение функции {func}, рендеринг шаблона 'readme.html'", func="readme")
    return render_template("readme.html", active_page='readme')


@app.route('/author')
def author():
    logger.info("Запуск функции {func}", func="author")
    logger.info("Завершение функции {func}, рендеринг шаблона 'author.html'", func="author")
    return render_template("author.html", active_page='readme')


if __name__ == '__main__':
    logger.add("logs/app.log", rotation="100 MB", level="CRITICAL")
    logger.info("Запуск файла {file} через __main__", file="views.py")
    app.run(debug=True, use_reloader=False)
    logger.info("Завершение файла {file} через __main__", file="views.py")
    sys.exit()

