import json
import time

from slugify import slugify
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


MENU_URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"


def get_driver() -> Chrome:
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    return Chrome(options=chrome_options)


def click_button_for_view_info(driver) -> None:
    time.sleep(0.7)
    button_detail_info = driver.find_element(
        By.ID, "accordion-29309a7a60-item-9ea8a10642-button"
    )
    button_detail_info.click()


def parse_page(product: webdriver) -> dict:
    driver = get_driver()
    link = product.get_attribute("href")
    driver.get(link)
    click_button_for_view_info(driver)

    name_product = driver.find_element(By.CLASS_NAME, "cmp-product-details-main__heading-title")
    description = driver.find_element(By.CLASS_NAME, "cmp-product-details-main__description")
    # info about calories, fats, carbs, proteins
    nutrition_summary = driver.find_elements(
        By.CSS_SELECTOR, ".cmp-nutrition-summary__heading-primary-item .value"
    )
    # info about sugar, unsaturated fats, salt, portion
    additional_info = driver.find_elements(
        By.CSS_SELECTOR, ".cmp-nutrition-summary__details-column-view-mobile .label-item .value"
    )

    return {
        "name": name_product.text.lower().replace("®", ""),
        "description": description.text,
        "calories": nutrition_summary[0].text.split()[-1],
        "fats": nutrition_summary[1].text.split()[-1],
        "carbs": nutrition_summary[2].text.split()[-1],
        "proteins": nutrition_summary[3].text.split()[-1],
        "unsaturated_fats": additional_info[0].text.split()[0],
        "sugar": additional_info[1].text.split()[0],
        "salt": additional_info[2].text.split()[0],
        "portion": additional_info[3].text.split()[0]
    }


def get_all_webdriver_products() -> list:
    driver = get_driver()
    driver.get(MENU_URL)
    products = driver.find_elements(By.CLASS_NAME, "cmp-category__item-link")

    return products


def get_all_products() -> None:
    products = get_all_webdriver_products()

    product_dict = {}
    for product in products:
        result_parse = parse_page(product)
        product_dict[slugify(result_parse["name"])] = result_parse

    write_to_json("McDonald_menu.json", product_dict)


def write_to_json(file_name: str, products: dict) -> None:
    with open(file_name, "a", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_all_products()
