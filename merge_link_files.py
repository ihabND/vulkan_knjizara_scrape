all_links_set = set()

for i in range(1, 50):
    try:
        with open(f"data/article_links_{i}.txt", "r", encoding="utf-8") as file:
            links = file.readlines()
            links_f = [link.strip() for link in links]
        for link in links_f:
            all_links_set.add(link)
    except Exception as e:
        print("Finished")

with open(f"data/ALL_LINKS.txt", "w", encoding="utf-8") as file:
    for link in all_links_set:
        file.write(link + "\n")
