from pprint import pprint

import yaml

# TODO: tags vege/vegan/...
with open("data/main.yaml") as f:
    data = yaml.safe_load(f)

pprint(data)
