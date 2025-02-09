import pandas as pd

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


mapping = {
    "https://stockanalysis.com/list/mid-cap-stocks/": "mid_cap.csv",
    "https://stockanalysis.com/list/small-cap-stocks/": "small_cap.csv",
    "https://stockanalysis.com/list/micro-cap-stocks/": "micro_cap.csv",
    "https://stockanalysis.com/list/nano-cap-stocks/": "nano_cap.csv",
}


def get_stock_list():

    links = mapping.keys()

    for link in links:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode

        # Set up the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(link)

        # Wait for the table to be visible
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//table/tbody")))

        data = []

        while True:
            # Wait for the table rows to be present
            wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr"))
            )

            # Get all rows from the table
            rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

            # Collect data from each row
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if columns:  # Ensure the row has data
                    data.append([column.text for column in columns])

            # Try clicking the "Next" button
            try:
                # Wait for the "Next" button to be clickable
                next_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="main"]/div[2]/div/div/nav/button[2]')
                    )
                )

                # Check if the "Next" button is disabled (no more pages)
                if "disabled" in next_button.get_attribute("class"):
                    print("Reached the last page.")
                    break

                # Scroll the "Next" button into view and click it using JavaScript
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                driver.execute_script("arguments[0].click();", next_button)

                # Wait for the next page to load
                time.sleep(2)  # Adjust this delay if necessary
            except Exception as e:
                print(f"Error clicking the 'Next' button: {e}")
                break  # If "Next" button is not found or not clickable, break the loop

        # Close the driver
        driver.quit()

        # Convert to a DataFrame
        if data:
            df = pd.DataFrame(data)
            df = df.drop(0, axis=1)
            df = df.rename(
                columns={
                    1: "Symbol",
                    2: "Company Name",
                    3: "Market Cap",
                    4: "Stock Price",
                    5: "Percent Change",
                    6: "Revenue",
                }
            )
            df.to_csv(
                f"/home/bread/Coding/Finance/src/data/market_cap/{mapping[link]}",
                index=False,
            )
            print(df)
            print(f"Total stocks scraped: {len(df)}")
        else:
            print("No data collected.")
