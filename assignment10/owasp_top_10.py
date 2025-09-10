from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# Setup Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open page
driver.get("https://owasp.org/www-project-top-ten/")

# Wait until the vulnerabilities list is visible
wait = WebDriverWait(driver, 10)
vulnerabilities = wait.until(
    EC.presence_of_all_elements_located(
        (
            By.XPATH,
            "//h2[@id='top-10-web-application-security-risks']/following-sibling::ul[1]/li/a",
        )
    )
)

top_10_list = []

for v in vulnerabilities:
    top_10_list.append({"title": v.text, "link": v.get_attribute("href")})

print(top_10_list)

# Save to CSV
df = pd.DataFrame(top_10_list)
df.to_csv("assignment10/owasp_top_10.csv", index=False)

driver.quit()
