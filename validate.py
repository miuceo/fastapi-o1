import datetime
import string
from typing import Dict, Any

from data_job import get_all_data, write_data

chars = string.ascii_letters + "'- " + string.digits

def validate_name(name: str) -> bool:
    if not name:
        return False
    name = name.strip().lower()
    if any(char not in chars for char in name):
        return False
    return True

def validate_year(year: int) -> bool:
    if year is None:
        return False
    current_year = datetime.datetime.now().year
    return 1980 <= year <= current_year

def validate_fullname(fullname: str) -> bool:
    parts = fullname.strip().split()
    if len(parts) < 2 or len(parts) > 4:
        return False
    return all(char in (string.ascii_letters + " '-") for char in fullname)

def update(id: int, data: Dict[str, Any], model: str, partial: bool = False) -> bool:
    if not id or model not in ['product', 'employee']:
        return False

    all_data = get_all_data()

    if model == 'product':
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

    if model == 'employee':
        employees = all_data.get('employees', [])
        companies = all_data.get('companies', [])
        company_ids = {c["id"] for c in companies}

        employee = next((employee for employee in employees if employee['id'] == id), None)
        if employee is None:
            return False

        if partial:
            if "fullname" in data:
                if not validate_fullname(data['fullname']):
                    return False
                employee['fullname'] = data['fullname']
            if "year" in data:
                if not validate_year(data['year']):
                    return False
                employee['year'] = data['year']
            if "company_id" in data:
                if data["company_id"] not in company_ids:
                    return False
                employee['company_id'] = data['company_id']

        else:
            fullname, year, company_id = data.get('fullname'), data.get('year'), data.get('company_id')
            if not (validate_fullname(fullname) and validate_year(year) and company_id in company_ids):
                return False
            employee.update({'fullname': fullname, 'year': year, 'company_id': company_id})

    return write_data(all_data)
