from flask_app.config import db


class Product(db.Model):
    """Класс для записи результатов парсинга в БД"""
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    shop = db.Column(db.String(50))
    category = db.Column(db.String(50))
    product_name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    volume = db.Column(db.String(20))
    price_real = db.Column(db.Float)

    def __repr__(self):
        return "datetime='{}', shop='{}', category={}, product_name={}, price={}, volume={}, price_real={}" \
            .format(self.datetime, self.shop, self.category, self.product_name, self.price, self.volume,
                    self.price_real)


class Parsing(db.Model):
    """Класс для записи продуктов для парсинга в БД"""
    __tablename__ = 'parsing'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
