import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Step 1: Load the Data
df = pd.read_csv('rtings laptops merge.csv')

# Step 2: Extract Relevant Columns
# Assuming the columns are named accordingly in the dataset
df_relevant = df[['Laptop Name', 'Gaming Rating', 'Multimedia Rating', 'Business Rating']]

# Step 3: Normalize the Ratings
scaler = MinMaxScaler()
df_relevant[['Gaming Rating', 'Multimedia Rating', 'Business Rating']] = scaler.fit_transform(df_relevant[['Gaming Rating', 'Multimedia Rating', 'Business Rating']])

# Calculate Combined Score
df_relevant['Combined_Score'] = df_relevant[['Gaming Rating', 'Multimedia Rating', 'Business Rating']].mean(axis=1)

# Step 4: Sort and Select Top 5
df_top5 = df_relevant.sort_values(by='Combined_Score', ascending=False).head(5)

# Display Results
print(df_top5[['Laptop Name', 'Gaming Rating', 'Multimedia Rating', 'Business Rating', 'Combined_Score']])
