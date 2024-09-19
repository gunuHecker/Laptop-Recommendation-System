from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Load the CSV file with laptop names and URLs
laptops_links_df = pd.read_csv('rtings laptoplinks.csv')

# Get the first laptop's name and URL
first_laptop_name = laptops_links_df.iloc[0]['Laptop Name']
first_laptop_url = laptops_links_df.iloc[0]['Link']

# Set up WebDriver
driver = webdriver.Chrome()

# Navigate to the first laptop's webpage
driver.get(first_laptop_url)

# Wait for the page to load completely
time.sleep(3)  # Adjust based on your internet speed and website loading time

# Get the HTML content of the entire page
html_content = driver.page_source

# Save the HTML content to a file
with open('firstlaptop.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

# Close the browser
driver.quit()

print(f"HTML content of the first laptop '{first_laptop_name}' has been saved to 'firstlaptop.html'.")
