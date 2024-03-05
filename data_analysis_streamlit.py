import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit app title
st.title('Stocks Data Analysis')

# File uploader allows the user to upload CSV directly
uploaded_file = st.file_uploader("Choose a file", type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Initial conversion and handling of 'Rec Date'
    df['Rec Date'] = df['Rec Date'].apply(lambda x: x[:-2] + "20" + x[-2:])
    df['Rec Date'] = pd.to_datetime(df['Rec Date'], format='%d/%m/%Y', errors='coerce')
    df['Rec Date'] = df['Rec Date'].fillna(pd.Timestamp('2020-01-01'))

    # Display basic statistics for numeric columns
    st.subheader('Basic Statistics')
    st.write(df.describe())

    # Display count of 'Rec Status' to see distribution of recommendations
    st.subheader('Recommendation Status Distribution')
    st.write(df['Rec Status'].value_counts())

    # Plot count of 'Rec Status' over time
    fig, ax = plt.subplots(figsize=(10, 6))
    df.set_index('Rec Date').groupby('Rec Status').resample('M').size().unstack(level=0).plot(kind='line', ax=ax)
    plt.title('Recommendation Status Over Time')
    plt.ylabel('Count')
    plt.xlabel('Rec Date')
    st.pyplot(fig)

    # Display correlation matrix
    st.subheader('Correlation Matrix')
    st.write(df[['Return', 'S&P UK']].corr())

    # Simple outlier detection based on quantiles
    high_returns = df[df['Return'] > df['Return'].quantile(0.95)]
    st.subheader('High Returns')
    st.write(high_returns)

    # Filter for 'Buy' and 'BestBuyNow' recommendations
    buy_recommendations = df[(df['Rec Status'] == 'Buy') | (df['Rec Status'] == 'BestBuyNow')]

    # Assuming there's a column 'Exchange' to filter by LSE stocks
    buy_recommendations_lse = buy_recommendations[buy_recommendations['Exchange'].str.contains('LSE', na=False)]
    st.subheader('Buy Recommendations for LSE Stocks')
    st.write(buy_recommendations_lse)