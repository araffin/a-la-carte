from pathlib import Path
from typing import Any

import markdown2
from jinja2 import Environment, FileSystemLoader
from menu_backend import Menu
from PIL import Image

current_dir = Path(__file__).parent
html_dir = current_dir / "html"
recipes_dir = current_dir / "recipes"

environment = Environment(loader=FileSystemLoader(str(html_dir)))
recipe_template = environment.get_template("recipe_template.html")

menus = [
    Menu.load(current_dir / "data/main.yaml", "main", "Main Course"),
    Menu.load(current_dir / "data/side-dish.yaml", "side-dish", "Side Dishes"),
    Menu.load(current_dir / "data/dessert.yaml", "dessert", "Desserts"),
]

metadata: dict[str, list[dict[str, Any]]] = {}
total_recipes = 0

recipes_dir.mkdir(exist_ok=True)

for menu in menus:
    total_recipes += len(menu.dishes)
    processed_info = []

    for dish in menu.dishes:
        dish_info: dict[str, Any] = {}

        if dish.link and not dish.link.startswith("http"):
            recipe_html = markdown2.markdown_path(str(current_dir / "data" / "recipes" / f"{dish.link}.md"))

            content_recipe = recipe_template.render(
                recipe=recipe_html,
                dish=dish,
            )
            recipe_output = recipes_dir / f"{dish.link}.html"
            with recipe_output.open(mode="w", encoding="utf-8") as result:
                result.write(content_recipe)

            dish_info["link"] = f"recipes/{dish.link}.html"
        else:
            dish_info["link"] = dish.link

        if dish.image and not dish.image.startswith("http"):
            with Image.open(current_dir / dish.image) as img:
                dish_info["image_width"], dish_info["image_height"] = img.size
        else:
            dish_info["image_width"], dish_info["image_height"] = 0, 0

        processed_info.append(dish_info)

    metadata[menu.name] = processed_info

template = environment.get_template("template.html")
content = template.render(
    menus=menus,
    metadata=metadata,
    total_recipes=total_recipes,
)

with (current_dir / "index.html").open(mode="w", encoding="utf-8") as result:
    result.write(content)
    print("Done.")
