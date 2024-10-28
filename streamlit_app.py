import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta

def generate_fund_figures(start_date, num_weekdays, num_share_classes):
    # Define fixed codes
    series_types = ["NAV", "FXRATES", "IR", "DISTR"]
    series_subtypes = [f"subtype{i}" for i in range(1, 6)]
    qualifiers = ["CHF", "EUR", "USD"]
    
    # Generate date range for the specified number of weekdays
    date_range = pd.bdate_range(start=start_date, periods=num_weekdays)
    
    # Calculate the number of records
    num_records = (num_share_classes * len(series_types) * 
                   len(series_subtypes) * len(qualifiers) * len(date_range))
    
    # Generate data
    data = {
        "shareclass_id": np.repeat(range(10, 10 + num_share_classes), len(series_types) * len(series_subtypes) * len(qualifiers) * len(date_range)),
        "series_type": np.tile(series_types, int(num_records / len(series_types))),
        "series_subtype": np.tile(series_subtypes, int(num_records / len(series_subtypes))),
        "qualifier": np.tile(qualifiers, int(num_records / len(qualifiers))),
        "value": np.random.uniform(100, 1000000, num_records).round(2),
        "value_date": np.tile(np.repeat(date_range, len(series_types) * len(series_subtypes) * len(qualifiers)), num_share_classes)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df

# Streamlit app layout
st.title("Random Fund Figures Generator")

# Input form for the parameters
with st.form("fund_figures_form"):
    start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
    num_weekdays = st.number_input("Number of Weekdays", min_value=1, max_value=10000, value=1000)
    num_share_classes = st.number_input("Number of Share Classes", min_value=1, max_value=1000, value=10)
    
    # Generate button
    generate_button = st.form_submit_button("Generate Data")

# Generate data and display if button is clicked
if generate_button:
    df = generate_fund_figures(start_date, num_weekdays, num_share_classes)
    
    # Streamlit filters
    st.sidebar.header("Filter options")
    selected_shareclass = st.sidebar.multiselect("Select Share Class ID", options=df["shareclass_id"].unique())
    selected_series_type = st.sidebar.multiselect("Select Series Type", options=df["series_type"].unique())
    selected_series_subtype = st.sidebar.multiselect("Select Series Subtype", options=df["series_subtype"].unique())
    selected_qualifier = st.sidebar.multiselect("Select Qualifier", options=df["qualifier"].unique())

    # Date filter
    date_range = st.sidebar.date_input("Select Date Range", [df["value_date"].min(), df["value_date"].max()])

    # Apply filters to the DataFrame
    filtered_df = df.copy()
    if selected_shareclass:
        filtered_df = filtered_df[filtered_df["shareclass_id"].isin(selected_shareclass)]
    if selected_series_type:
        filtered_df = filtered_df[filtered_df["series_type"].isin(selected_series_type)]
    if selected_series_subtype:
        filtered_df = filtered_df[filtered_df["series_subtype"].isin(selected_series_subtype)]
    if selected_qualifier:
        filtered_df = filtered_df[filtered_df["qualifier"].isin(selected_qualifier)]
    if date_range:
        filtered_df = filtered_df[(filtered_df["value_date"] >= pd.to_datetime(date_range[0])) &
                                (filtered_df["value_date"] <= pd.to_datetime(date_range[1]))]

    # Display filtered DataFrame
    st.write("Filtered Data")
    st.dataframe(filtered_df)
    
    # Optionally allow download as CSV
    #csv = df.to_csv(index=False)
    #st.download_button("Download CSV", data=csv, file_name="fund_figures.csv", mime="text/csv")
