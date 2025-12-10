import datetime
import string
from typing import Dict, Any

from data_job import get_all_data, write_data

chars = string.ascii_letters + "‘'- " + string.digits

def validate_name(name: str) -> bool:
    if not name:
        return False
    name = name.strip().lower()
    if any(char not in chars for char in name):
        return False
    products = get_all_data().get('products', [])
    return all(product['name'].lower().strip() != name for product in products)

def validate_year(year: int) -> bool:
    if year is None:
        return False
    current_year = datetime.datetime.now().year
    return 1980 <= year <= current_year

def validate_fullname(fullname: str) -> bool:
    parts = fullname.strip().split()
    if len(parts) < 2 or len(parts) > 4:
        return False
    return all(char in chars for char in fullname)

def update(id: int, data: Dict[str, Any], model: str, partial: bool = False) -> bool:
    if not id or model != 'product':
        return False

    all_data = get_all_data()
    products = all_data.get('products', [])
    categories = {c['id'] for c in all_data.get('categories', [])}

    product = next((p for p in products if p['id'] == id), None)
    if product is None:
        return False

    if partial:
        if "name" in data:
            if not validate_name(data["name"]):
                return False
            product["name"] = data["name"]
        if "year" in data:
            if not validate_year(data["year"]):
                return False
            product["year"] = data["year"]
        if "category_id" in data:
            if data["category_id"] not in categories:
                return False
            product["category_id"] = data["category_id"]
    else:
        name, year, category_id = data.get("name"), data.get("year"), data.get("category_id")
        if not (validate_name(name) and validate_year(year) and category_id in categories):
            return False
        product.update({"name": name, "year": year, "category_id": category_id})

    return write_data(all_data)
