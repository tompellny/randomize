import streamlit as st
import pandas as pd
import numpy as np

def generate_timeseries(data_size, start_value, max_change, annual_drift):
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

def main():
    st.title("Random Time Series Generator with Drift")
    st.subheader("Random Time Series Generator with Drift", divider="red")

    # Input fields for user configuration
    data_size = st.number_input("Data size (number of points)", min_value=1, value=100)
    start_value = st.number_input("Starting value", value=100.0)
    max_change = st.number_input("Max change in %", min_value=0.0, max_value=100.0, value=7.0)
    annual_drift = st.number_input("Annual drift in % (positive for growth, negative for decline)", value=5.0)

    # Button to generate the time series
    if st.button("Generate Time Series"):
        # Generate the timeseries data
        timeseries = generate_timeseries(data_size, start_value, max_change, annual_drift)
        
        # Create a DataFrame for plotting
        df = pd.DataFrame({
            "Time": pd.date_range(start='1/1/2020', periods=data_size, freq='D'),
            "Value": timeseries
        })
        
        # Display the line chart
        st.line_chart(df.set_index("Time"))

        # CSV download
        csv = df.to_csv(sep=';', index=False)
        st.download_button(
            label="Download Time Series",
            data=csv,
            file_name='random_timeseries.csv',
            mime='text/csv',
        )

# Run the Streamlit app
if __name__ == "__main__":
    main()
