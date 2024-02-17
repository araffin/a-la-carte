import yaml
from jinja2 import Environment, FileSystemLoader
from PIL import Image

data: dict[str, list[dict]] = {
    "main": [],
    "dessert": [],
}
name_to_flags = {
    "argentina": "🇦🇷",
    "india": "🇮🇳",
    "france": "🇫🇷",
    "italy": "🇮🇹",
    "afghanistan": "🇦🇫",
    "spicy": "🌶️",
}
n_columns = 3
n_pages = {}
column_class = {
    1: "is-full",
    2: "is-half",
    3: "is-one-third",
    4: "is-one-quarter",
}
total_recipes = 0
for key in data.keys():
    with open(f"data/{key}.yaml") as f:
        raw_data = yaml.safe_load(f)

    n_dish_per_column = len(raw_data) // n_columns + 1
    n_dish_per_page = n_columns * n_dish_per_column
    total_recipes += len(raw_data)

    n_pages[key] = 0
    # preprocess flags
    processed_data = []
    raw_data = sorted(raw_data, key=lambda item: item["name"])
    for idx, dish in enumerate(raw_data):
        processed_dish = dish.copy()
        flag_str = ""
        for tag in processed_dish.get("tags", []):
            if tag in name_to_flags:
                flag_str += " " + name_to_flags[tag]

        processed_dish["tags"] = ",".join(processed_dish.get("tags", []))
        processed_dish["ingredients"] = ",".join(processed_dish.get("ingredients", []))
        processed_dish["flags"] = flag_str
        processed_dish["link"] = dish.get("link")
        processed_dish["image"] = dish.get("image")

        if processed_dish["link"] and "http" not in processed_dish["link"]:
            processed_dish["link"] = f"recipe.html?id={processed_dish['link']}"

        # Retrieve image dimensions by reading the image
        if processed_dish["image"] and "https" not in processed_dish["image"]:
            with Image.open(processed_dish["image"]) as img:
                processed_dish["image_width"], processed_dish["image_height"] = img.size
        else:
            processed_dish["image_width"], processed_dish["image_height"] = 0, 0

        processed_dish["options"] = dish.get("options", "")
        processed_dish["new_page"] = (idx % n_dish_per_page) == 0
        processed_dish["close_page"] = idx > 0 and ((idx + 1) % n_dish_per_page) == 0 or idx == len(raw_data) - 1
        processed_dish["new_column"] = (idx % n_dish_per_column) == 0
        processed_dish["close_column"] = idx > 0 and ((idx + 1) % n_dish_per_column) == 0 or idx == len(raw_data) - 1
        processed_data.append(processed_dish)
        if processed_dish["new_page"]:
            n_pages[key] += 1

    data[key] = processed_data


# pprint(data)


environment = Environment(loader=FileSystemLoader("html/"))
template = environment.get_template("template.html")

content = template.render(
    meals=[
        {"name": "Main Course", "dishes": data["main"]},
        {"name": "Desserts", "dishes": data["dessert"]},
    ],
    column_class=column_class[n_columns],
    total_recipes=total_recipes,
)

with open("index.html", mode="w", encoding="utf-8") as result:
    result.write(content)
    print("Done.")
