"""SQL persistence for Product entities."""

import json

from .connect import DatabaseManager
from models.product import Product


class ProductRepository:
    def __init__(self):
        self.mysql = DatabaseManager()
        self.cursor = self.mysql.cursor()

    def get_all(self):
        self.cursor.execute("SELECT * FROM products ORDER BY name")
        return [Product.from_row(row) for row in self.cursor.fetchall()]

    def get_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        return Product.from_row(self.cursor.fetchone())

    def get_by_name(self, name):
        self.cursor.execute("SELECT * FROM products WHERE name = %s", (name,))
        return Product.from_row(self.cursor.fetchone())

    def add(self, name, ingredients, margin, is_hot=False, description=None):
        query = """
            INSERT INTO products (name, ingredients, profit_margin, is_hot, description)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            query,
            (str(name), json.dumps(ingredients), margin, 1 if is_hot else 0, description),
        )
        self.mysql.connection.commit()
        return self.cursor.lastrowid

    def delete(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        self.mysql.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.cursor.close()
        self.mysql.connection.close()
