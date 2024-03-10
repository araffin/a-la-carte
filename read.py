import re

import yaml
from jinja2 import Environment, FileSystemLoader
from PIL import Image

NON_ALPHA_NUMERIC = re.compile(r"[^a-zA-Z0-9]")

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

    # preprocess flags
    processed_data = []
    raw_data = sorted(raw_data, key=lambda item: item["name"])
    for dish in raw_data:
        processed_dish = dish.copy()
        flag_str = ""
        for tag in processed_dish.get("tags", []):
            if tag in name_to_flags:
                flag_str += " " + name_to_flags[tag]

        # convert name to an id by removing spaces and lowercasing
        # and remove non-alphanumeric characters
        dish_id = NON_ALPHA_NUMERIC.sub("", dish["name"].lower())

        processed_dish["id"] = dish_id
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
        processed_data.append(processed_dish)

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
