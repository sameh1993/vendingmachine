"""Product model and operations delegated to its repository."""

import json


class Product:
    def __init__(self, name=None, ingredients=None, profit_margin=0, is_hot=False,
                 description=None, product_id=None):
        self.id = product_id
        self.name = name
        self.ingredients = ingredients
        self.profit_margin = float(profit_margin or 0)
        self.is_hot = bool(is_hot)
        self.description = description
        self.price = 0.0
        self._repository = None

    def _repo(self):
        if self._repository is None:
            from db.productRepo import ProductRepository
            self._repository = ProductRepository()
        return self._repository

    def get_products(self, material_costs=None):
        products = self._repo().get_all()
        if material_costs is not None:
            for product in products:
                product.price = product.selling_price(material_costs)
        return products

    def add_product(self, name, ingredients, margin, is_hot=False, description=None):
        return self._repo().add(name, ingredients, margin, is_hot, description)

    def delete_product(self, product_id):
        return self._repo().delete(product_id)

    def close(self):
        if self._repository is not None:
            self._repository.close()
            self._repository = None

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        ingredients = row.get("ingredients") or {}
        if isinstance(ingredients, str):
            try:
                ingredients = json.loads(ingredients)
            except (TypeError, ValueError):
                ingredients = {}
        return cls(
            name=row.get("name", ""),
            ingredients=ingredients,
            profit_margin=row.get("profit_margin", 0),
            is_hot=row.get("is_hot", False),
            description=row.get("description"),
            product_id=row.get("id"),
        )

    @property
    def ingredients_text(self):
        if not isinstance(self.ingredients, dict):
            return str(self.ingredients)
        return ", ".join(f"{name}: {amount}" for name, amount in self.ingredients.items())

    def selling_price(self, material_costs):
        ingredient_cost = sum(
            float(material_costs.get(name, 0)) * float(quantity)
            for name, quantity in self.ingredients.items()
        ) if isinstance(self.ingredients, dict) else 0
        return round(ingredient_cost * (1 + self.profit_margin), 2)


class ColdDrink(Product):
    def __init__(self, *args, **kwargs):
        kwargs["is_hot"] = False
        super().__init__(*args, **kwargs)


class HotDrink(Product):
    def __init__(self, *args, **kwargs):
        kwargs["is_hot"] = True
        super().__init__(*args, **kwargs)
