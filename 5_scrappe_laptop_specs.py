from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# Load the CSV file with laptop names and URLs
laptops_df = pd.read_csv('rtings laptoplinks.csv')

# Define the columns for the new CSV file
columns = ['Laptop Name', 'Refresh Rate', 'RAM', 'Storage', 'Battery', 'CPU']

# Create a new CSV file with the headers
output_file = 'rtings laptop specs.csv'
pd.DataFrame(columns=columns).to_csv(output_file, index=False)

# Function to scrape specifications of a single laptop
def scrape_laptop_specs(laptop_name, laptop_url):
    # Set up WebDriver
    driver = webdriver.Chrome()

    # Navigate to the laptop's webpage
    driver.get(laptop_url)

    # Wait for the page to load completely
    time.sleep(3)  # Adjust based on your internet speed and website loading time

    # Get the HTML content of the page
    page_html = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_html, 'html.parser')

    # Initialize a dictionary to store the extracted data
    laptop_data = {
        'Laptop Name': laptop_name,
        'Refresh Rate': 'NA',
        'RAM': 'NA',
        'Storage': 'NA',
        'Battery': 'NA',
        'CPU': 'NA'
    }

    # Extract Refresh Rate (8th div under product_page-test_results-content)
    try:
        refresh_rate_div = soup.select('.product_page-test_results-content .e-simple_grid .test_group')[7]
        refresh_rate = refresh_rate_div.find('span', class_='test_result_value').text.strip()
        laptop_data['Refresh Rate'] = refresh_rate
    except Exception as e:
        print(f"Failed to extract Refresh Rate for {laptop_name}: {e}")

    # Extract RAM (26th div)
    try:
        ram_div = soup.select('.product_page-test_results-content .e-simple_grid .test_group')[25]
        ram = ram_div.find('span', class_='test_result_value').text.strip()
        laptop_data['RAM'] = ram
    except Exception as e:
        print(f"Failed to extract RAM for {laptop_name}: {e}")

    # Extract Storage (27th div)
    try:
        storage_div = soup.select('.product_page-test_results-content .e-simple_grid .test_group')[26]
        storage = storage_div.find('span', class_='test_result_value').text.strip()
        laptop_data['Storage'] = storage
    except Exception as e:
        print(f"Failed to extract Storage for {laptop_name}: {e}")

    # Extract Battery (33rd div)
    try:
        battery_div = soup.select('.product_page-test_results-content .e-simple_grid .test_group')[32]
        battery = battery_div.find('span', class_='test_result_value').text.strip()
        laptop_data['Battery'] = battery
    except Exception as e:
        print(f"Failed to extract Battery for {laptop_name}: {e}")

    # Extract CPU (24th div)
    try:
        cpu_div = soup.select('.product_page-test_results-content .e-simple_grid .test_group')[23]
        brand = cpu_div.select_one('.test_value.is-word .test_result_value').text.strip()
        model = cpu_div.select_one('.test_value.is-freeform .test_result_value').text.strip()
        core_count = cpu_div.select_one('.test_value.is-number .test_result_value').text.strip()
        cpu_info = f"{brand} {model} with Core Count {core_count}"
        laptop_data['CPU'] = cpu_info
    except Exception as e:
        print(f"Failed to extract CPU for {laptop_name}: {e}")

    return laptop_data

# Scrape all laptops and save their specs to the CSV file
laptops_data = []

for index, row in laptops_df.iterrows():
    laptop_name = row['Laptop Name']
    laptop_url = row['Link']
    
    laptop_specs = scrape_laptop_specs(laptop_name, laptop_url)
    laptops_data.append(laptop_specs)
    
    # Save the data to the CSV file after each iteration to avoid data loss in case of errors
    pd.DataFrame([laptop_specs]).to_csv(output_file, mode='a', header=False, index=False)
    
    print(f"Processed: {laptop_name}")
    time.sleep(2)  # Optional: Add a delay between requests to avoid overloading the server

print(f"CSV file '{output_file}' has been created and filled with all laptop specs.")
