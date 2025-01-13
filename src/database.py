# src/database.py
import shelve

def create_products_db():
    with shelve.open("data/products") as db:
        if "products" not in db:
            db["products"] = {
                "1": {"name": "Chicken Rice", "price": 5.00, "description": "Delicious chicken rice."},
                "2": {"name": "Satay", "price": 0.80, "description": "Tasty satay sticks."},
                # Add more products here
            }

def get_all_products():
    with shelve.open("data/products") as db:
        return db.get("products", {})

def get_product_by_id(product_id):
    with shelve.open("data/products") as db:
        return db["products"].get(product_id)

def update_product(product_id, details):
    with shelve.open("data/products") as db:
        products = db["products"]
        products[product_id] = details
        db["products"] = products

def delete_product(product_id):
    with shelve.open("data/products") as db:
        products = db["products"]
        if product_id in products:
            del products[product_id]
            db["products"] = products
