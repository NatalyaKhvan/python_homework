from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import json

# Setup Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open page
driver.get("https://owasp.org/www-project-top-ten/")

# Let page load
time.sleep(3)

# Find all search result items
vulnerabilities = driver.find_elements(
    By.XPATH,
    "//h2[@id='top-10-web-application-security-risks']/following-sibling::ul[1]/li/a",
)

top_10_list = []

for v in vulnerabilities:
    top_10_list.append({"title": v.text, "link": v.get_attribute("href")})

print(top_10_list)

# Save to CSV
df = pd.DataFrame(top_10_list)
df.to_csv("assignment10/owasp_top_10.csv", index=False)

driver.quit()
