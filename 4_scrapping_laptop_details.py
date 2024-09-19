from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# Load the CSV file with laptop names and URLs
laptops_df = pd.read_csv('rtings laptoplinks.csv')

# Define the columns for the CSV file
columns = [
    'Laptop Name', 'School Review', 'School Rating', 'Gaming Review', 'Gaming Rating', 
    'Multimedia Review', 'Multimedia Rating', 'Workstation Review', 'Workstation Rating', 
    'Business Review', 'Business Rating', 'Overall Review'
]

# Create a new CSV file with the headers
output_file = 'rtings laptops details.csv'
pd.DataFrame(columns=columns).to_csv(output_file, index=False)

# Function to scrape reviews in batches
def scrape_reviews(start_index, end_index):
    # Set up WebDriver
    driver = webdriver.Chrome()

    # Initialize a list to hold the extracted data
    laptops_data = []

    # Iterate through each laptop in the CSV from start_index to end_index
    for index, row in laptops_df.iloc[start_index:end_index].iterrows():
        laptop_name = row['Laptop Name']
        laptop_url = row['Link']
        
        # Navigate to the laptop's webpage
        driver.get(laptop_url)
        
        # Wait for the page to load completely
        time.sleep(3)  # Adjust based on your internet speed and website loading time
        
        # Get the HTML content of the div with class "product_page"
        try:
            product_page_html = driver.find_element(By.CLASS_NAME, 'product_page').get_attribute('outerHTML')
        except Exception as e:
            print(f"Failed to load product page for {laptop_name}: {e}")
            continue
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(product_page_html, 'html.parser')
        
        # Extract ratings from spans with class "e-score_box-value"
        ratings = soup.find_all('span', class_='e-score_box-value')
        
        if len(ratings) >= 5:  # Ensure there are at least 5 ratings available
            school_rating = ratings[0].text.strip()
            gaming_rating = ratings[1].text.strip()
            multimedia_rating = ratings[2].text.strip()
            workstation_rating = ratings[3].text.strip()
            business_rating = ratings[4].text.strip()
        else:
            school_rating = gaming_rating = multimedia_rating = workstation_rating = business_rating = 'N/A'
        
        # Extract the reviews for each category
        reviews = soup.find_all('div', {'data-node': 'details'})
        if len(reviews) >= 5:
            school_review = reviews[0].find('p').text.strip()
            gaming_review = reviews[1].find('p').text.strip()
            multimedia_review = reviews[2].find('p').text.strip()
            workstation_review = reviews[3].find('p').text.strip()
            business_review = reviews[4].find('p').text.strip()
        else:
            school_review = gaming_review = multimedia_review = workstation_review = business_review = 'N/A'

        # Extract the overall review from the second <p> tag in the "product_page-header"
        try:
            overall_review = soup.find('div', class_='product_page-header').find_all('p')[1].text.strip()
        except Exception as e:
            print(f"Failed to load overall review for {laptop_name}: {e}")
            overall_review = 'N/A'

        # Append the data to the list
        laptops_data.append([
            laptop_name, school_review, school_rating, gaming_review, gaming_rating,
            multimedia_review, multimedia_rating, workstation_review, workstation_rating,
            business_review, business_rating, overall_review
        ])
        
        print(f"Processed: {laptop_name}")
    
    # Close the browser
    driver.quit()
    
    return laptops_data

# Scrape all reviews in batches of 10
all_laptops_data = []
batch_size = 10
total_laptops = len(laptops_df)

for i in range(0, total_laptops, batch_size):
    laptops_data = scrape_reviews(i, min(i + batch_size, total_laptops))
    all_laptops_data.extend(laptops_data)
    time.sleep(5)  # Add a short delay between sessions

# Convert the scraped data into a DataFrame
laptops_ratings_df = pd.DataFrame(all_laptops_data, columns=columns)

# Save the DataFrame to the CSV file 'rtings-laptops-details.csv'
laptops_ratings_df.to_csv(output_file, mode='a', header=False, index=False)

print(f"CSV file '{output_file}' has been created and updated with all laptop names, reviews, and ratings.")
