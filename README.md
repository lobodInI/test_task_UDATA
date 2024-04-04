# Scraping McDonald menu

#### How to use:

```bash
cd project
git clone https://github.com/lobodInI/test_task_UDATA/tree/develop

python3 -m venv venv
pip install -r requirements.txt

uvicorn main:app --reload

```

Implemented endpoints :

* a) get: /all_products/  - return all information about all products
* b) get: /products/{product_name}  - return information about exact product
* c) get: //products/{product_name}/{product_field}  - return information about exact field    
