import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_timeseries(data_size, start_value, max_change, annual_drift, start_date):
    # Initialize the time series with the starting value
    timeseries = [start_value]
    
    # Assume max_change corresponds to 3 standard deviations (99.7% confidence)
    std_dev = max_change / 3
    
    # Calculate daily drift, assuming 252 trading days in a year
    daily_drift = (annual_drift / 252) / 100
    for _ in range(data_size - 1):
        # Generate a change using a normal distribution with drift
        change_percent = np.random.normal(daily_drift, std_dev)

        # Calculate the next value ensuring it does not exceed the max_change limits
        change_factor = 1 + max(min(change_percent, max_change), -max_change) / 100
        next_value = timeseries[-1] * change_factor

        # Append the next value to the timeseries
        timeseries.append(next_value)
    return timeseries

def calculate_daily_returns(timeseries):
    # Calculate daily returns as percentage changes
    returns = np.diff(timeseries) / timeseries[:-1] * 100
    return returns

def plot_returns_histogram(returns):
    plt.figure(figsize=(10, 4))
    plt.hist(returns, bins=50, color='blue', alpha=0.7)
    plt.title('Distribution of Daily Returns')
    plt.xlabel('Returns (%)')
    plt.ylabel('Frequency')
    plt.grid(True)
    return plt

def main():
    st.title("Time Series Generator with Drift")
    st.markdown('This tool generates a random time series based on the specified parameters. It also includes a histogram showing the distribution of daily returns.')

    st.subheader("Enter Parameters", divider="red")
    st.write("")

    # Input fields for user configuration with unique keys
    start_date = st.date_input("Start Date", value=pd.to_datetime('2020-01-01'), format="YYYY-MM-DD")
    start_value = st.number_input("Starting value", value=100.0, key='start_value')
    data_size = st.slider("Data size (number of points)", min_value=250, max_value=5000, step=250, value=1250, key='data_size')
    max_change = st.slider("Max daily change in %", min_value=1, max_value=25, step=1, value=15, key='max_change')
    annual_drift = st.slider("Annual drift in % (positive for growth, negative for decline)", min_value=-15, max_value=15, step=1, value=7, key='annual_drift')

    # Generate and display the time series on button click
    if st.button("Generate Timeseries", key='generate_ts'):
        timeseries = generate_timeseries(data_size, start_value, max_change, annual_drift, start_date)
        
        # Generate dates only for weekdays
        dates = pd.bdate_range(start=start_date, periods=data_size, freq='B')
        df = pd.DataFrame({"Time": dates.strftime('%Y-%m-%d'), "Value": timeseries})
        
        # Calculate daily returns and add to DataFrame
        daily_returns = calculate_daily_returns(timeseries)
        df['Daily Return'] = np.append([np.nan], daily_returns)  # First value is NaN
        
        st.subheader("Random Time Series with Drift", divider="red")
        st.write("")
        st.line_chart(df.set_index("Time")[['Value']])  # Select only the 'Value' column for the line chart
        
        # Calculate and display the total return
        total_return = ((timeseries[-1] / timeseries[0]) - 1) * 100
        st.metric(label="Total Return", value=f"{total_return:.2f}%")
        
        st.subheader("Daily Returns Bar Chart", divider="red")
        st.write("")
        fig = plot_returns_histogram(daily_returns)
        st.pyplot(fig)

        csv = df.to_csv(sep=';', index=False)
        st.download_button("Download Time Series", data=csv, file_name='timeseries.csv', mime='text/csv')

if __name__ == "__main__":
    main()
