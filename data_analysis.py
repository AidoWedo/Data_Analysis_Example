import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('stocks_data.csv')

# Initial conversion and handling of 'Rec Date'
# Rec date was in format dd/mm/yy
df['Rec Date'] = df['Rec Date'].apply(lambda x: x[:-2] + "20" + x[-2:])
df['Rec Date'] = pd.to_datetime(df['Rec Date'], format='%d/%m/%Y', errors='coerce')
df['Rec Date'] = df['Rec Date'].fillna(pd.Timestamp('2020-01-01'))

# Print Data Frames types as part of testing and troubleshooting ensure correct
# print(df.dtypes)

# Basic statistics for numeric columns
print(df.describe())

# Count of 'Rec Status' to see distribution of Buy, Hold, and Sold recommendations
print(df['Rec Status'].value_counts())

# Ensure there are no issues with 'Rec Status' before proceeding
print(df['Rec Status'].value_counts())

# Plot count of 'Rec Status' over time
df.set_index('Rec Date').groupby('Rec Status').resample('ME').size().unstack(level=0).plot(kind='line', figsize=(10, 6))
plt.title('Recommendation Status Over Time')
plt.ylabel('Count')
plt.xlabel('Rec Date')

# Show plot
plt.show()

# Correlation matrix
print(df[['Return', 'S&P UK']].corr())

# Simple outlier detection based on quantiles
high_returns = df[df['Return'] > df['Return'].quantile(0.95)]

# Filter for 'Buy' and 'BestBuyNow' recommendations. Adjust the filtering logic based on your actual data structure
buy_recommendations = df[(df['Rec Status'] == 'Buy') | (df['Rec Status'] == 'BestBuyNow')]

# Assuming you want to list these for LSE stocks specifically, you'd also need a way to filter by exchange.
# This step assumes there's a column 'Exchange' that contains this information. Adjust as necessary.
buy_recommendations_lse = buy_recommendations[buy_recommendations['Exchange'].str.contains('LSE', na=False)]

# Display the filtered DataFrame with only the relevant columns (e.g., 'Symbol', 'Rec Status', 'Price')
print(buy_recommendations_lse)
