from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

driver = webdriver.Chrome() 
driver.get("https://arcprize.org/play?task=6aa20dc0")
time.sleep(5)  

containers = ["input_preview"] + [f"pair_preview_{i}" for i in range(2)]

for container_class in containers:
    try:
        container = driver.find_element(By.CSS_SELECTOR, f"div.{container_class}.puzzle.selectable_grid")
    except:
        print(f"Container {container_class} not found, skipping.")
        continue

    rows = container.find_elements(By.CSS_SELECTOR, "div.grid-row")
    flat_grid = []

    for row in rows:
        flat_row = []
        cells = row.find_elements(By.CSS_SELECTOR, "div.cell")
        for cell in cells:
            flat_row.append(cell.get_attribute("symbol"))
        flat_grid.append(flat_row)

    filename = f"{container_class}.json"
    with open(filename, "w") as f:
        json.dump(flat_grid, f, indent=4)
    print(f"{filename} saved.")

driver.quit()
