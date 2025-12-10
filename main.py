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


if __name__ == "__main__":
    uvicorn.run(app)