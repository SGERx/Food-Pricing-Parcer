import os

import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

SECRET_KEY = os.urandom(32)

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5433/products_postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
connection = psycopg2.connect(database="products_postgres", user="postgres", password="root", host="localhost",
                              port=5433)
