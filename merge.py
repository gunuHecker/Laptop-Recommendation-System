import pandas as pd

# Load the two CSV files
details_df = pd.read_csv('rtings-laptops-details.csv')
specs_df = pd.read_csv('rtings-laptop-specs.csv')

# Merge the two DataFrames on the 'Laptop Name' column
merged_df = pd.merge(details_df, specs_df, on='Laptop Name', how='inner')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('rtings-laptops-merge.csv', index=False)

print("Merged CSV file 'rtings-laptops-merge.csv' has been created successfully.")
