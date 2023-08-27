from pprint import pprint

import yaml
from jinja2 import Environment, FileSystemLoader

# TODO: tags vege/vegan/...
data = {
    "main": [],
    "dessert": [],
}
name_to_flags = {
    "argentina": "🇦🇷",
    "india": "🇮🇳",
    "france": "🇫🇷",
    "spicy": "🌶️",
}
for key in data.keys():
    with open(f"data/{key}.yaml") as f:
        raw_data = yaml.safe_load(f)
    # preprocess flags
    processed_data = []
    for dish in raw_data:
        processed_dish = dish.copy()
        flag_str = ""
        for tag in processed_dish.get("tags", []):
            if tag in name_to_flags:
                flag_str += " " + name_to_flags[tag]

        processed_dish["flags"] = flag_str
        processed_dish["options"] = dish.get("options", "TODO")
        processed_data.append(processed_dish)

    data[key] = processed_data


# pprint(data)


environment = Environment(loader=FileSystemLoader("html/"))
template = environment.get_template("template.html")

content = template.render(
    dishes=data["main"],
    desserts=data["dessert"],
)

with open("result.html", mode="w", encoding="utf-8") as result:
    result.write(content)
    print("Done.")
