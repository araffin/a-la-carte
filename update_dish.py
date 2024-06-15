from pathlib import Path

from omg import Menu

current_dir = Path(__file__).parent
menu = Menu.load(f"{current_dir}/data/main.yaml")

dish = menu.search("aglio")

dish[0].update_image("/home/antonin/Téléchargements/Photos-001/aglio.jpg",current_dir / "images")

# Save the updated menu
menu.save(f"{current_dir}/data/main.yaml")
