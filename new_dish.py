from pathlib import Path

from omg import Dish, Menu
from rich.prompt import Prompt

current_dir = Path(__file__).parent

# List all the filenames in the images-tmp directory
images = [item.name for item in (current_dir / "images-tmp").iterdir() if item.is_file()]

default_image = images[0] if len(images) == 1 else ""

menu_name = Prompt.ask("Menu?", choices=["main", "dessert"], default="main")

menu = Menu.load(f"{current_dir}/data/{menu_name}.yaml")

try:
    name = Prompt.ask("Name?")
    image = Prompt.ask("Image?", choices=images, default=default_image)
    options = Prompt.ask("Options?", default="")
    ingredients = Prompt.ask("Ingredients?", default="").split(",")
    tags = Prompt.ask("Tags?", default="").split(",")
    link = Prompt.ask("Link?", default="")

    # Convert [""] to empty list for ingredients and tags
    if ingredients == [""]:
        ingredients = []
    if tags == [""]:
        tags = []

    # Remove extra spaces from ingredients and tags
    ingredients = [ingredient.strip() for ingredient in ingredients]
    tags = [tag.strip() for tag in tags]

    new_dish = Dish(name, ingredients=ingredients, tags=tags, options=options, link=link)
    if image:
        # Preprocess the image and save it to the images directory
        new_dish.update_image(current_dir / "images-tmp" / image, current_dir / "images")
        # Move original image to processed folder
        (current_dir / "images-tmp" / image).replace(current_dir / "images-tmp/processed" / image)

    menu.add(new_dish)

    # sort menu
    # TODO: add to omg package
    menu._dishes.sort(key=lambda item: item.name)

except KeyboardInterrupt:
    print("Exiting...")
    pass

# Save the updated menu
menu.save(f"{current_dir}/data/{menu_name}.yaml")
