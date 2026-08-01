import requests
from bs4 import BeautifulSoup

user_agent = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
}

CHUNK_SIZE = 1000
page_num = 1160

seen = set()
buffer = []
chunk_index = 9


def flush(links, index):
    with open(f"data/article_links_{index}.txt", "w", encoding="utf-8") as file:
        for link in links:
            file.write(link + "\n")
    print(f"wrote article_links_{index}.txt ({len(links)} links)")

counter = 268
for i in range(1, page_num + 1):
    url = f"https://www.knjizare-vulkan.rs/proizvodi/page-{counter}"
    print("SCRAPING...", counter, url)
    counter += 1

    try:
        response = requests.get(url, headers=user_agent, timeout=30)
        content = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error, skipping page: {e}")

    for div in content.find_all("div", {"class": "nb-product-name"}):
        link = div.find("a", {"class": "nb-link"})
        if link is None or not link.get("href"):
            continue
        href = link["href"]
        if href in seen:
            continue
        seen.add(href)
        buffer.append(href)

    while len(buffer) >= CHUNK_SIZE:
        flush(buffer[:CHUNK_SIZE], chunk_index)
        buffer = buffer[CHUNK_SIZE:]
        chunk_index += 1

if buffer:
    flush(buffer, chunk_index)