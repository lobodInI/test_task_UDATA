import json

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def read_file_json() -> dict:
    with open("McDonald_menu.json", "r", encoding="UTF-8") as json_file:
        content = json_file.read()
        return json.loads(content)


@app.get("/all_products/")
def get_all_products():
    return read_file_json()


@app.get("/products/{product_name}/")
def get_product_by_name(
        product_name: str
) -> dict | HTTPException:
    all_products = read_file_json()
    product = all_products.get(product_name)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found!")

    return product


@app.get("/products/{product_name}/{product_field}/")
def get_product_field_by_name(
        product_name: str, product_field: str
) -> dict | HTTPException:
    all_products = read_file_json()
    product = all_products.get(product_name)

    if product is None:
        raise HTTPException(
            status_code=404, detail="Product not found!"
        )

    product_field_data = product.get(product_field)

    if product_field_data is None:
        raise HTTPException(
            status_code=404, detail="Product field not found!"
        )

    return {product_field: product_field_data}
