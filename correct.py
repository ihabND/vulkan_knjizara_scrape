import json

import requests
from bs4 import BeautifulSoup

with open("data/ALL_LINKS.txt", "r", encoding="utf-8") as file:
    individual_product_links = file.readlines()
individual_product_links = [link.strip() for link in individual_product_links]

user_agent = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
}


def find_product_ld(soup):
    """Return the JSON-LD block whose @type is Product, or None."""
    for tag in soup.find_all("script", type="application/ld+json"):
        raw = tag.string or tag.get_text()
        if not raw or not raw.strip():
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue

        # a block can be a dict, a list of dicts, or use @graph
        candidates = data if isinstance(data, list) else data.get("@graph", [data])
        if isinstance(candidates, dict):
            candidates = [candidates]

        for item in candidates:
            if isinstance(item, dict) and item.get("@type") == "Product":
                return item
    return None


for link in individual_product_links:
    try:
        individual_page = requests.get(link, headers=user_agent, timeout=60)
    except Exception as e:
        print(f"Page fetch failed: {e}")
        continue

    content = BeautifulSoup(individual_page.text, "html.parser")
    product = find_product_ld(content)

    if product is None:
        print(f"No Product JSON-LD: {link}")
        continue

    offers = product.get("offers") or {}
    brand = product.get("brand") or {}

    row = {
        "name": product.get("name"),
        "isbn": product.get("isbn"),
        "sku": product.get("sku"),
        "brand": brand.get("name"),
        "price": offers.get("price"),
        "currency": offers.get("priceCurrency"),
        "availability": offers.get("availability", "").rsplit("/", 1)[-1],
        "url": offers.get("url") or link,
    }

    print(row)
    print("=" * 100)
