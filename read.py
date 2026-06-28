import re
from pathlib import Path
from typing import Any

import markdown2
from jinja2 import Environment, FileSystemLoader
from menu_backend import Menu
from PIL import Image

NON_ALPHA_NUMERIC = re.compile(r"[^a-zA-Z0-9]")

current_dir = Path(__file__).parent

menus = [
    Menu.load(f"{current_dir}/data/main.yaml", "main", "Main Course"),
    Menu.load(f"{current_dir}/data/side-dish.yaml", "side-dish", "Side Dishes"),
    Menu.load(f"{current_dir}/data/dessert.yaml", "dessert", "Desserts"),
]

metadata: dict[str, list[dict]] = {}

n_columns = 3
column_class = {
    1: "is-full",
    2: "is-half",
    3: "is-one-third",
    4: "is-one-quarter",
}

environment = Environment(loader=FileSystemLoader("html/"))
recipe_template = environment.get_template("recipe_template.html")

total_recipes = 0
for menu in menus:
    menu_columns = min(n_columns, len(menu.dishes))
    n_dish_per_column = len(menu.dishes) // menu_columns
    # Try to have equal repartition of dishes per column
    if len(menu.dishes) % menu_columns != 0:
        n_dish_per_column += 1
    n_dish_per_page = menu_columns * n_dish_per_column
    total_recipes += len(menu.dishes)

    # preprocess flags
    processed_info = []
    for idx, dish in enumerate(menu.dishes):
        dish_info: dict[str, Any] = {}

        if dish.link and "http" not in dish.link:
            recipe_html = markdown2.markdown_path(f"{current_dir}/data/recipes/{dish.link}.md")

            content_recipe = recipe_template.render(
                recipe=recipe_html,
                dish=dish,
            )
            with open(f"recipes/{dish.link}.html", mode="w", encoding="utf-8") as result:
                result.write(content_recipe)

            dish_info["link"] = f"recipes/{dish.link}.html"

        else:
            dish_info["link"] = dish.link

        # Retrieve image dimensions by reading the image
        if dish.image and "https" not in dish.image:
            with Image.open(dish.image) as img:
                dish_info["image_width"], dish_info["image_height"] = img.size
        else:
            dish_info["image_width"], dish_info["image_height"] = 0, 0

        last_dish = idx == len(menu.dishes) - 1
        dish_info["new_page"] = (idx % n_dish_per_page) == 0
        dish_info["close_page"] = (idx > 0 and ((idx + 1) % n_dish_per_page) == 0) or last_dish
        dish_info["new_column"] = (idx % n_dish_per_column) == 0
        dish_info["close_column"] = (idx >= 0 and ((idx + 1) % n_dish_per_column) == 0) or last_dish
        processed_info.append(dish_info)

    metadata[menu.name] = processed_info


# pprint(data)


environment = Environment(loader=FileSystemLoader("html/"))
template = environment.get_template("template.html")

content = template.render(
    menus=menus,
    metadata=metadata,
    column_class=column_class[n_columns],
    total_recipes=total_recipes,
)

with open("index.html", mode="w", encoding="utf-8") as result:
    result.write(content)
    print("Done.")
