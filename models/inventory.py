"""Inventory material model and its repository operations."""


class Inventory:
    def __init__(self, name=None, unit="", cost_per_unit=0, quantity=0, id=None):
        self.id = id
        self.name = name
        self.unit = unit or ""
        self.cost_per_unit = float(cost_per_unit or 0)
        self.quantity = float(quantity or 0)
        self._repository = None

    def _repo(self):
        if self._repository is None:
            from db.inventoryRepo import InventoryRepository
            self._repository = InventoryRepository()
        return self._repository

    def get_materials(self):
        return self._repo().get_all()

    def add_material(self, name, unit, quantity, cost_per_unit):
        return self._repo().add_or_update(name, unit, quantity, cost_per_unit)

    def adjust_material(self, material_id, amount):
        return self._repo().adjust_quantity_by_id(material_id, amount)

    def delete_material(self, material_id):
        return self._repo().delete(material_id)

    def close(self):
        if self._repository is not None:
            self._repository.close()
            self._repository = None
