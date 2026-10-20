import os

from flask import Flask, render_template, request, redirect, url_for, flash

from models.product import Product
from models.inventory import Inventory

app = Flask(__name__)
# Set FLASK_SECRET_KEY in the environment for sessions outside local development.
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "local-development-key")


@app.route("/")
def homepage():
    return machine_page()




@app.route("/machine")
def machine_page():
    products = Product()
    inventory = Inventory()
    try:
        costs = {material.name: material.cost_per_unit for material in inventory.get_materials()}
        return render_template("machiceView.html", products=products.get_products(costs))
    finally:
        products.close()
        inventory.close()


@app.route("/menu")
def menu_page():
    products = Product()
    inventory = Inventory()
    try:
        costs = {material.name: material.cost_per_unit for material in inventory.get_materials()}
        return render_template("menu.html", products=products.get_products(costs))
    finally:
        products.close()
        inventory.close()


@app.route("/dashboard")
def dashboard_page():
    inventory = Inventory()
    products = Product()
    try:
        costs = {material.name: material.cost_per_unit for material in inventory.get_materials()}
        return render_template("dashboard.html", products=products.get_products(costs),
                               materials=inventory.get_materials())
    finally:
        products.close()
        inventory.close()


@app.route("/materials/add", methods=["POST"])
def add_material_page():
    inventory = Inventory()
    try:
        inventory.add_material(request.form["name"].strip(), request.form["unit"].strip(),
                               float(request.form["quantity"]), float(request.form["cost"]))
        flash("Material saved.", "success")
    finally:
        inventory.close()
    return redirect(url_for("dashboard_page"))


@app.route("/materials/<int:material_id>/update", methods=["POST"])
def update_material_page(material_id):
    inventory = Inventory()
    try:
        inventory.adjust_material(material_id, float(request.form["amount"]))
        flash("Stock updated.", "success")
    finally:
        inventory.close()
    return redirect(url_for("dashboard_page"))


@app.route("/materials/<int:material_id>/delete", methods=["POST"])
def delete_material_page(material_id):
    inventory = Inventory()
    try:
        inventory.delete_material(material_id)
        flash("Material deleted.", "success")
    finally:
        inventory.close()
    return redirect(url_for("dashboard_page"))


@app.route("/products/add", methods=["POST"])
def add_product_page():
    names = request.form.getlist("ingredient_name")
    quantities = request.form.getlist("ingredient_qty")
    ingredients = {name.strip(): float(quantity) for name, quantity in zip(names, quantities)
                   if name.strip()}
    products = Product()
    try:
        products.add_product(request.form["name"].strip(), ingredients,
                             float(request.form["margin"]), request.form.get("is_hot") == "1",
                             request.form.get("description", "").strip())
        flash("Drink saved.", "success")
    finally:
        products.close()
    return redirect(url_for("dashboard_page"))


@app.route("/products/<int:product_id>/delete", methods=["POST"])
def delete_product_page(product_id):
    products = Product()
    try:
        products.delete_product(product_id)
        flash("Drink deleted.", "success")
    finally:
        products.close()
    return redirect(url_for("dashboard_page"))


if __name__ == "__main__":
    app.run(debug=True)
