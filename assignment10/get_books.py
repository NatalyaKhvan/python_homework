from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json

# Setup Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open page
driver.get(
    "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
)

# Wait until the search results are visible
wait = WebDriverWait(driver, 10)
items = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "li.row.cp-search-result-item")
    )
)

results = []

for item in items:
    try:
        # Title
        title_el = item.find_element(By.CSS_SELECTOR, "a[title]")
        title = title_el.get_attribute("title").strip()

        # Authors
        author_els = item.find_elements(By.CSS_SELECTOR, "a.author-link")
        authors = (
            "; ".join([a.text.strip() for a in author_els]) if author_els else "Unknown"
        )

        # Format-Year
        try:
            format_year_span = item.find_element(
                By.CSS_SELECTOR,
                "div.manifestation-item-format-info-wrap span.cp-screen-reader-message",
            )
            format_year_text = format_year_span.text.strip()
        except NoSuchElementException:
            format_year_text = "Unknown"

        # Add to results
        results.append(
            {"Title": title, "Author": authors, "Format-Year": format_year_text}
        )

    except Exception as e:
        print("Skipping one result due to error:", e)

# Create DataFrame
df = pd.DataFrame(results)
print(df)

# Write CSV
df.to_csv("assignment10/get_books.csv", index=False)

# Write JSON
with open("assignment10/get_books.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

# Close browser
driver.quit()
