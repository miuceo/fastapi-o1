from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException

from data_job import get_all_data, write_data
from validate import validate_fullname, validate_name, validate_year, update

app = FastAPI()

@app.get('/')
def main():
    return {
        "message": "Hello from FastAPI!"
    }

@app.get('/products/')
def all_products():
    products = get_all_data().get('products', [])
    return products

@app.get('/products/{id}')
def get_single_product(id :int):
    products = get_all_data().get('products', [])
    for product in products:
        if product['id'] == id:
            return product

    raise HTTPException(status_code=404, detail="Product with this id not found!")

@app.post('/products/')
def post_new_product(data: dict):
    name = data.get('name')
    year = data.get('year')
    category_id = data.get('category_id')

    products = get_all_data().get('products', [])
    categories = get_all_data().get('categories', [])

    if not validate_name(name) or not validate_year(year) or not category_id in [category['id'] for category in categories]:
        raise HTTPException(status_code=400, detail="Please enter right data!")

    all_data = get_all_data()
    all_data['products'].append(
        {
            "id": max([product['id'] for product in products], default=0) + 1,
            "year": year,
            "name": name,
            "category_id": category_id,
        }
    )

    last_status = write_data(all_data)

    if last_status:
        return {
            "message": "Created"
        }
    else:
        raise HTTPException(status_code=502, detail="Bad Gateway")

@app.put('/products/{id}')
def put_product(id: int, data: Dict[str, Any]):
    if not update(id, data=data, model='product'):
        raise HTTPException(status_code=400, detail='Please correct data!')
    return {
        "message": "Updated"
    }

@app.patch('/products/{id}')
def patch_product(id: int, data: Dict[str, Any]):
    if not update(id, data=data, model='product', partial=True):
        raise HTTPException(status_code=400, detail='Please correct data!')
    return {
        "message": "Updated"
    }

@app.delete('/products/{id}')
def delete_product(id: int):
    all_data = get_all_data()
    products = all_data.get('products', [])
    product = next((product for product in products if product['id'] == id), None)

    if not product:
        raise HTTPException(status_code=404, detail='The product with this id not found!')

    products.remove(product)
    status = write_data(all_data)

    if not status:
        raise HTTPException(status_code=400, detail='An eror occured, try again!')

    return {
        "message": "Deleted"
    }

@app.get('/employees/')
def get_all_employees():
    employees = get_all_data().get('employees', [])
    return employees

@app.post('/employees/')
def post_new_product(data: dict):
    fullname = data.get('fullname')
    year = data.get('year')
    company_id = data.get('company_id')

    employees = get_all_data().get('employees', [])
    companies = get_all_data().get('companies', [])

    if not validate_fullname(fullname) or not validate_year(year) or not company_id in [company['id'] for company in companies]:
        raise HTTPException(status_code=400, detail="Please enter right data!")

    all_data = get_all_data()
    all_data['employees'].append(
        {
            "id": max([employee['id'] for employee in employees], default=0) + 1,
            "year": year,
            "fullname": fullname,
            "company_id": company_id,
        }
    )

    if write_data(all_data):
        return {
            "message": "Created"
        }
    else:
        raise HTTPException(status_code=502, detail="Bad Gateway")

@app.get('/employees/{id}')
def get_single_emplyee(id: int):
    employee = next((employee for employee in get_all_data().get('employees', []) if employee['id'] == id), None)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail = 'Employee with this id not found!'
        )

    return employee

@app.put('/employees/{id}')
def put_employee(id: int, data: Dict[str, Any]):
    if not update(id, data=data, model='employee'):
        raise HTTPException(status_code=400, detail='Please enter correct data!')
    return {
        "message": "Updated"
    }

@app.patch('/employees/{id}')
def patch_employee(id: int, data: Dict[str, Any]):
    if not update(id, data=data, model='employee', partial=True):
        raise HTTPException(status_code=400, detail='Please correct data!')
    return {
        "message": "Updated"
    }

@app.delete('/employees/{id}')
def delete_employee(id: int):
    all_data = get_all_data()
    employees = all_data.get('employees', [])
    employee = next((product for product in employees if product['id'] == id), None)

    if not employee:
        raise HTTPException(status_code=404, detail='An employee with this id not found!')

    employees.remove(employee)
    status = write_data(all_data)

    if not status:
        raise HTTPException(status_code=400, detail='An eror occured, try again!')

    return {
        "message": "Deleted"
    }


if __name__ == "__main__":
    uvicorn.run(app)