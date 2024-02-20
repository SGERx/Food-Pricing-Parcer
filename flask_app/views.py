from flask import send_from_directory, render_template, request, redirect, send_file

from flask_app.config import app, db
from flask_app.flask_db_queries.query_by_price_bill import flask_price_bill
from flask_app.flask_db_queries.query_by_real_price import flask_price_real
from flask_app.flask_db_queries.query_category_by_price import flask_category_price_data
from flask_app.flask_db_queries.query_category_by_real_price import flask_category_real_price_data
from flask_app.flask_db_queries.query_cheapest_products_by_category import flask_cheapest
from flask_app.flask_db_queries.query_expensive_products_by_category import flask_expensive
from flask_app.flask_db_queries.query_three_days_data import flask_three_days_data
from flask_app.flask_db_queries.query_today_data import flask_today_data
from flask_app.flask_db_queries.truncate_table import truncate_table_parsing, truncate_table_products
from flask_app.forms import ProductForm
from flask_app.models import Product

import os

from parsing_logic.step_1_parsing.parsing.by_store.parsing_auchan import flask_auchan

from flask_app.models import Parsing
from parsing_logic.step_1_parsing.parsing.by_store.parsing_globus import flask_globus
from parsing_logic.step_1_parsing.parsing.by_store.parsing_magnit import flask_magnit
from parsing_logic.step_1_parsing.parsing.by_store.parsing_metro import flask_metro
from parsing_logic.step_1_parsing.parsing.by_store.parsing_miratorg import flask_miratorg
from parsing_logic.step_1_parsing.parsing.by_store.parsing_perekrestok import flask_perekrestok
from parsing_logic.step_1_parsing.parsing.by_store.parsing_vkusvill import flask_vkusvill
from parsing_logic.step_1_parsing.parsing.by_store.parsing_vprok import flask_vprok
from xlsx_update.query_all_data import update_all_data_xlsx
from xlsx_update.query_by_bill_price import update_bill_price_xlsx
from xlsx_update.query_by_real_price import update_real_price_xlsx
from xlsx_update.query_cheapest_products_by_category import update_cheapest_products_xlsx
from xlsx_update.query_expensive_products_by_category import update_expensive_products

parsing = Parsing.query.all()


def parsing_in_progress():
    return "PARSING IN PROGRESS..."


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# Header

@app.route('/')
@app.route('/home')
def my_index_view():
    return render_template("home.html", active_page='home')


@app.route('/product_list', methods=["POST", "GET"])
def product_list():
    form = ProductForm()
    parsing = Parsing.query.all()
    if request.method == "POST":
        if len(request.form['product_name']) == 0:
            return "Внесите имя продукта, пустая форма не будет сохранена"
        product_name = request.form['product_name']
        parsing = Parsing(product_name=product_name)
        try:
            db.session.add(parsing)
            db.session.commit()
            return redirect('/product_list')
        except:
            return "Ошибка внесения данных в базу"
    else:
        return render_template("product_list.html", form=form, parsing=parsing, active_page='product_list')


@app.route('/delete/<int:id>')
def delete(id):
    parsing_obj = Parsing.query.get_or_404(id)
    try:
        db.session.delete(parsing_obj)
        db.session.commit()
    except:
        return "Не удалось удалить объект"
    return redirect('/product_list')


@app.route('/parsing')
def parsing():
    return render_template("parsing.html", active_page='parsing')


# тестовая страница для запуска скриптов
@app.route('/parsing_all')
def parsing_all():
    flask_auchan()
    print("Flask Auchan parsing complete")
    flask_globus()
    print("Flask Globus parsing complete")
    flask_magnit()
    print("Flask Magnit parsing complete")
    flask_metro()
    print("Flask Metro parsing complete")
    flask_miratorg()
    print("Flask Miratorg parsing complete")
    flask_perekrestok()
    print("Flask Perekrestok parsing complete")
    flask_vkusvill()
    print("Flask Vkusvill parsing complete")
    flask_vprok()

    return redirect('/parsing_complete')


@app.route('/parsing_auchan')
def parsing_auchan():
    flask_auchan()
    return redirect('/parsing_complete')


@app.route('/parsing_globus')
def parsing_globus():
    flask_globus()
    return redirect('/parsing_complete')


@app.route('/parsing_magnit')
def parsing_magnit():
    flask_magnit()
    return redirect('/parsing_complete')


@app.route('/parsing_metro')
def parsing_metro():
    flask_metro()
    return redirect('/parsing_complete')


@app.route('/parsing_miratorg')
def parsing_miratorg():
    flask_miratorg()
    return redirect('/parsing_complete')


@app.route('/parsing_perekrestok')
def parsing_perekrestok():
    flask_perekrestok()
    return redirect('/parsing_complete')


@app.route('/parsing_vkusvill')
def parsing_vkusvill():
    flask_vkusvill()
    return redirect('/parsing_complete')


@app.route('/parsing_vprok')
def parsing_vprok():
    flask_vprok()
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
    products = Product.query.all()
    return render_template("parsing_submenu_all_data.html", products=products, active_page='all_data')


@app.route('/category_price')
def category_price():
    category_price_data = flask_category_price_data()
    return render_template("parsing_submenu_category_price_data.html", products=category_price_data, active_page='category_price')


@app.route('/category_real_price')
def category_real_price():
    category_real_price_data = flask_category_real_price_data()
    return render_template("parsing_submenu_category_real_price_data.html", products=category_real_price_data, active_page='category_real_price')


@app.route('/price_bill')
def price_bill():
    bill_data = flask_price_bill()
    return render_template("parsing_submenu_price_bill.html", products=bill_data, active_page='price_bill')


@app.route('/price_real')
def real_price():
    real_data = flask_price_real()
    return render_template("parsing_submenu_price_real.html", products=real_data, active_page='price_real')


@app.route('/products_cheapest')
def cheapest_products():
    cheap_data = flask_cheapest()
    return render_template("parsing_submenu_products_cheapest.html", products=cheap_data, active_page='products_cheapest')


@app.route('/products_expensive')
def expensive_products():
    expensive_data = flask_expensive()
    return render_template("parsing_submenu_products_expensive.html", products=expensive_data, active_page='products_expensive')




@app.route('/download')
def download():
    products = Product.query.all()
    return render_template("parsing_submenu_download.html", products=products, active_page='download')


@app.route('/download_all_data')
def download_all_data():
    update_all_data_xlsx()
    path = "D:/DEV/Pet Projects/Food Pricing Parcer/data/e_query_results/query_0-all_data.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_price_bill')
def download_all_price_bill():
    update_bill_price_xlsx()
    path = "D:/DEV/Pet Projects/Food Pricing Parcer/data/e_query_results/query_1-by_bill_price.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_price_real')
def download_all_price_real():
    update_real_price_xlsx()
    path = "D:/DEV/Pet Projects/Food Pricing Parcer/data/e_query_results/query_2-by_real_price.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_products_cheapest')
def download_all_cheapest_products():
    update_cheapest_products_xlsx()
    path = "D:/DEV/Pet Projects/Food Pricing Parcer/data/e_query_results/query_3-cheapest_products.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_products_expensive')
def download_all_expensive_products():
    update_expensive_products()
    path = "D:/DEV/Pet Projects/Food Pricing Parcer/data/e_query_results/query_4-expensive_products.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_readme')
def download_readme():
    path = "D:/DEV/Pet Projects/Food Pricing Parcer/README.md"
    return send_file(path, as_attachment=True)


@app.route('/truncate')
def truncate():
    return render_template("truncate.html", active_page='truncate')

@app.route('/truncate_complete')
def truncate_complete():
    print('Вызов страницы удаления')
    truncate_table_parsing()
    truncate_table_products()
    return redirect('/home')


# Footer

@app.route('/info')
def info():
    return render_template("about.html", active_page='info')


@app.route('/readme')
def readme():
    return render_template("readme.html", active_page='readme')


@app.route('/author')
def author():
    return render_template("author.html", active_page='readme')


if __name__ == '__main__':
    app.run()
