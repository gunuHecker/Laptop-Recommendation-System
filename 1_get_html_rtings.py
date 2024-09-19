from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.rtings.com/laptop/reviews")

# Scroll down incrementally to load more content
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for new content to load
    time.sleep(3)
    
    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Break the loop when no new content is loaded
    last_height = new_height

# Find all div elements with class "app-body"
laptop_elems = driver.find_elements(By.CLASS_NAME, 'reviews_page-product')

# Initialize a variable to hold the combined HTML content
html_content = ''

# Loop through each element and extract its HTML
for element in laptop_elems:
    html_content += element.get_attribute('outerHTML') + '\n'

# Save the combined HTML content to a file
with open('rtings laptops.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

time.sleep(20)
# Close the browser
driver.quit()

print("HTML content of all laptops from rtings has been saved to rtings-laptops.html")
