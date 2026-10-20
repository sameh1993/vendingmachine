"""SQL persistence for Inventory entities."""

from .connect import DatabaseManager
from models.inventory import Inventory


class InventoryRepository:
    def __init__(self):
        self.mysql = DatabaseManager()
        self.cursor = self.mysql.cursor()

    def insert_new_material(self, material):
        self.cursor.execute(
            "INSERT INTO inventory (name, unit, quantity, cost_per_unit) "
            "VALUES (%s, %s, %s, %s)",
            (material.name, material.unit, material.quantity, material.cost_per_unit),
        )
        self.mysql.connection.commit()
        return self.cursor.lastrowid

    def get_all(self):
        self.cursor.execute("SELECT * FROM inventory ORDER BY name")
        return [self._to_inventory(row) for row in self.cursor.fetchall()]

    def get_by_name(self, name):
        self.cursor.execute("SELECT * FROM inventory WHERE name = %s", (name,))
        row = self.cursor.fetchone()
        return self._to_inventory(row) if row else None

    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM inventory WHERE id = %s", (id,))
        row = self.cursor.fetchone()
        return self._to_inventory(row) if row else None

    @staticmethod
    def _to_inventory(row):
        return Inventory(
            name=row.get("name", ""),
            unit=row.get("unit", ""),
            cost_per_unit=row.get("cost_per_unit", 0),
            quantity=row.get("quantity", 0),
            id=row.get("id"),
        )

    def add_or_update(self, name, unit, quantity, cost):
        query = """
            INSERT INTO inventory (name, unit, quantity, cost_per_unit)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                unit = VALUES(unit),
                quantity = quantity + VALUES(quantity),
                cost_per_unit = VALUES(cost_per_unit)
        """
        self.cursor.execute(query, (name, unit, quantity, cost))
        self.mysql.connection.commit()

    def adjust_quantity(self, name, amount):
        self.cursor.execute(
            "UPDATE inventory SET quantity = quantity + %s WHERE name = %s",
            (amount, name),
        )
        self.mysql.connection.commit()
        return self.cursor.rowcount > 0

    def adjust_quantity_by_id(self, id, amount):
        self.cursor.execute(
            "UPDATE inventory SET quantity = quantity + %s WHERE id = %s",
            (amount, id),
        )
        self.mysql.connection.commit()
        return self.cursor.rowcount > 0

    def delete(self, id):
        self.cursor.execute("DELETE FROM inventory WHERE id = %s", (id,))
        self.mysql.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.cursor.close()
        self.mysql.connection.close()
