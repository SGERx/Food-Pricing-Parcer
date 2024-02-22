import os

from flask import send_from_directory, render_template, request, redirect, send_file

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
from flask_app.flask_db_queries.flask_price_bill import flask_price_bill
from flask_app.flask_db_queries.flask_real_price import flask_price_real
from flask_app.flask_db_queries.flask_category_price import flask_category_price_data
from flask_app.flask_db_queries.flask_category_real_price import flask_category_real_price_data
from flask_app.flask_db_queries.flask_cheapest_products import flask_cheapest
from flask_app.flask_db_queries.flask_expensive_products import flask_expensive
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
from xlsx_update.xlsx_real_price import update_real_price_xlsx
from xlsx_update.xlsx_category_price import update_category_price_data_xlsx
from xlsx_update.xlsx_category_real_price import update_category__real_price_data_xlsx
from xlsx_update.xlsx_cheapest_products import update_cheapest_products_xlsx
from xlsx_update.xlsx_expensive_products import update_expensive_products
from xlsx_update.xlsx_three_days import update_three_days_data_xlsx
from xlsx_update.xlsx_today import update_today_data_xlsx

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

    flask_clean_data_auchan()
    flask_clean_data_globus()
    flask_clean_data_magnit()
    flask_clean_data_metro()
    flask_clean_data_miratorg()
    flask_clean_data_perekrestok()
    flask_clean_data_vkusvill()
    flask_clean_data_vprok()

    create_csv()
    create_json()
    write_to_db_postgres()
    return redirect('/parsing_complete')


@app.route('/parsing_auchan')
def parsing_auchan():
    flask_auchan()
    flask_clean_data_auchan()
    create_csv()
    create_json()
    write_to_db_postgres()
    return redirect('/parsing_complete')


@app.route('/parsing_globus')
def parsing_globus():
    flask_globus()
    flask_clean_data_globus()
    create_csv()
    create_json()
    write_to_db_postgres()
    return redirect('/parsing_complete')


@app.route('/parsing_magnit')
def parsing_magnit():
    flask_magnit()
    flask_clean_data_magnit()

    create_csv()
    create_json()
    write_to_db_postgres()
    return redirect('/parsing_complete')


@app.route('/parsing_metro')
def parsing_metro():
    flask_metro()
    flask_clean_data_metro()
    create_csv()
    create_json()
    write_to_db_postgres()
    return redirect('/parsing_complete')


@app.route('/parsing_miratorg')
def parsing_miratorg():
    flask_miratorg()
    flask_clean_data_miratorg()
    create_csv()
    create_json()
    write_to_db_postgres()
    return redirect('/parsing_complete')


@app.route('/parsing_perekrestok')
def parsing_perekrestok():
    flask_perekrestok()
    flask_clean_data_perekrestok()
    create_csv()
    create_json()
    write_to_db_postgres()
    return redirect('/parsing_complete')


@app.route('/parsing_vkusvill')
def parsing_vkusvill():
    flask_vkusvill()
    flask_clean_data_vkusvill()
    create_csv()
    create_json()
    write_to_db_postgres()
    return redirect('/parsing_complete')


@app.route('/parsing_vprok')
def parsing_vprok():
    flask_vprok()
    flask_clean_data_vprok()
    create_csv()
    create_json()
    write_to_db_postgres()
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
    return render_template("parsing_submenu_category_price_data.html", products=category_price_data,
                           active_page='category_price')


@app.route('/category_real_price')
def category_real_price():
    category_real_price_data = flask_category_real_price_data()
    return render_template("parsing_submenu_category_real_price_data.html", products=category_real_price_data,
                           active_page='category_real_price')


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
    return render_template("parsing_submenu_products_cheapest.html", products=cheap_data,
                           active_page='products_cheapest')


@app.route('/products_expensive')
def expensive_products():
    expensive_data = flask_expensive()
    return render_template("parsing_submenu_products_expensive.html", products=expensive_data,
                           active_page='products_expensive')


@app.route('/download')
def download():
    products = Product.query.all()
    return render_template("parsing_submenu_download.html", products=products, active_page='download')


@app.route('/download_all_data')
def download_all_data():
    update_all_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_0-all_data.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_three_days')
def download_three_days():
    update_three_days_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_1-three_days_data.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_today')
def download_today():
    update_today_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_2-today_data.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_category_by_price')
def download_category_by_price():
    update_category_price_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_3-category_by_price.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_category_by_real_price')
def download_category_by_real_price():
    update_category__real_price_data_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_4-category_by_real_price.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_price_bill')
def download_all_price_bill():
    update_bill_price_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_5-by_bill_price.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_price_real')
def download_all_price_real():
    update_real_price_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_6-by_real_price.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_products_cheapest')
def download_all_cheapest_products():
    update_cheapest_products_xlsx()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_7-cheapest_products.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_products_expensive')
def download_all_expensive_products():
    update_expensive_products()
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/data/e_query_results/query_8-expensive_products.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_readme')
def download_readme():
    path = "D:/DEV/Pet Projects/Food-Pricing-Parcer/README.md"
    return send_file(path, as_attachment=True)


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
