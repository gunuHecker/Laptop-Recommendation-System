from bs4 import BeautifulSoup

# Load the HTML content from the file
with open('firstlaptop.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize a dictionary to store the extracted data
laptop_data = {
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
    print(f"Failed to extract Refresh Rate: {e}")

# Extract RAM (26th div)
try:
    ram_div = soup.select('.product_page-test_results-content .e-simple_grid .test_group')[25]
    ram = ram_div.find('span', class_='test_result_value').text.strip()
    laptop_data['RAM'] = ram
except Exception as e:
    print(f"Failed to extract RAM: {e}")

# Extract Storage (27th div)
try:
    storage_div = soup.select('.product_page-test_results-content .e-simple_grid .test_group')[26]
    storage = storage_div.find('span', class_='test_result_value').text.strip()
    laptop_data['Storage'] = storage
except Exception as e:
    print(f"Failed to extract Storage: {e}")

# Extract Battery (33rd div)
try:
    battery_div = soup.select('.product_page-test_results-content .e-simple_grid .test_group')[32]
    battery = battery_div.find('span', class_='test_result_value').text.strip()
    laptop_data['Battery'] = battery
except Exception as e:
    print(f"Failed to extract Battery: {e}")

# Extract CPU (24th div)
try:
    cpu_div = soup.select('.product_page-test_results-content .e-simple_grid .test_group')[23]
    brand = cpu_div.select_one('.test_value.is-word .test_result_value').text.strip()
    model = cpu_div.select_one('.test_value.is-freeform .test_result_value').text.strip()
    core_count = cpu_div.select_one('.test_value.is-number .test_result_value').text.strip()
    cpu_info = f"{brand} {model} with Core Count {core_count}"
    laptop_data['CPU'] = cpu_info
except Exception as e:
    print(f"Failed to extract CPU: {e}")

# Print the extracted data
for key, value in laptop_data.items():
    print(f"{key}: {value}")
