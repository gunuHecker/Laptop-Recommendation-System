from bs4 import BeautifulSoup
import pandas as pd

# Load the HTML content from the file
with open('rtings laptops.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all anchor tags with the class "t-link-style reviews_page-product-fullname"
laptop_links = soup.find_all('a', class_='t-link-style reviews_page-product-fullname')

# Extract laptop names and URLs
laptops = []
for link in laptop_links:
    laptop_name = link.text.strip()  # Extract the text (laptop name)
    laptop_url = link['href']  # Extract the href attribute (URL)
    laptops.append([laptop_name, 'https://www.rtings.com' + laptop_url])

# Create a DataFrame using pandas
df = pd.DataFrame(laptops, columns=['Laptop Name', 'Link'])

# Save the DataFrame to a CSV file
df.to_csv('rtings laptoplinks.csv', index=False)

print("CSV file 'rtings laptoplinks.csv' has been created with laptop names and URLs.")