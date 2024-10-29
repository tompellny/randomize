import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Randomize", layout="centered")
st.image("assets/logo-finstory-symboltext.png", width=80)

def generate_fund_figures(start_date, num_weekdays, num_share_classes):
    # Fixed values
    series_types = ["NAV", "FXRATES", "IR", "DISTR"]
    series_subtypes = [f"subtype{i}" for i in range(1, 6)]
    qualifiers = ["CHF", "EUR", "USD"]
    
    # Generate date range for weekdays
    date_range = pd.bdate_range(start=start_date, periods=num_weekdays).strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
    
    # Calculate the number of total records needed
    total_records = num_share_classes * len(series_types) * len(series_subtypes) * len(qualifiers) * len(date_range)
    
    # Generate each column
    shareclass_ids = np.repeat(range(10, 10 + num_share_classes), len(series_types) * len(series_subtypes) * len(qualifiers) * len(date_range))
    series_types_col = np.tile(np.repeat(series_types, len(series_subtypes) * len(qualifiers) * len(date_range)), num_share_classes)
    series_subtypes_col = np.tile(np.repeat(series_subtypes, len(qualifiers) * len(date_range)), num_share_classes * len(series_types))
    qualifiers_col = np.tile(np.repeat(qualifiers, len(date_range)), num_share_classes * len(series_types) * len(series_subtypes))
    values = np.random.uniform(100, 1000000, total_records).round(2)
    value_dates = np.tile(np.repeat(date_range, len(series_types) * len(series_subtypes) * len(qualifiers)), num_share_classes)
    
    # Create DataFrame
    df = pd.DataFrame({
        "shareclass_id": shareclass_ids,
        "series_type": series_types_col,
        "series_subtype": series_subtypes_col,
        "qualifier": qualifiers_col,
        "value": values,
        "value_date": value_dates
    })
    
    return df

# Streamlit app layout
st.title("Random Fund Figures Generator")

# Input form for the parameters
with st.form("fund_figures_form"):
    start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
    num_weekdays = st.number_input("Number of Weekdays", min_value=1, max_value=10000, value=10)
    num_share_classes = st.number_input("Number of Share Classes", min_value=1, max_value=1000, value=5)
    
    # Generate button
    generate_button = st.form_submit_button("Generate Data")

# Generate data and store in session_state
if generate_button:
    st.session_state.df = generate_fund_figures(start_date, num_weekdays, num_share_classes)
    num_records = num_weekdays * num_share_classes * 4 * 5 * 3
    st.success(f"{num_records:,} records generated!")

# Sidebar filters and display if data exists
if "df" in st.session_state:
    df = st.session_state.df
    st.sidebar.header("Apply Filters:")

    # Filter options
    selected_shareclass = st.sidebar.multiselect("Share Class ID", options=df["shareclass_id"].unique(), placeholder="choose")
    selected_series_type = st.sidebar.multiselect("Series Type", options=df["series_type"].unique(), placeholder="choose")
    selected_series_subtype = st.sidebar.multiselect("Series Subtype", options=df["series_subtype"].unique(), placeholder="choose")
    selected_qualifier = st.sidebar.multiselect("Qualifier", options=df["qualifier"].unique(), placeholder="choose")
    selected_date = st.sidebar.multiselect("Value Date", options=df["value_date"].unique(), placeholder="choose")

    # Apply filters
    filtered_df = df.copy()
    if selected_shareclass:
        filtered_df = filtered_df[filtered_df["shareclass_id"].isin(selected_shareclass)]
    if selected_series_type:
        filtered_df = filtered_df[filtered_df["series_type"].isin(selected_series_type)]
    if selected_series_subtype:
        filtered_df = filtered_df[filtered_df["series_subtype"].isin(selected_series_subtype)]
    if selected_qualifier:
        filtered_df = filtered_df[filtered_df["qualifier"].isin(selected_qualifier)]
    if selected_date:
        filtered_df = filtered_df[filtered_df["value_date"].isin(selected_date)]

    # Display filtered data
    num_filtered = len(filtered_df)

    st.write(f"Data set filtered to {num_filtered:,} records.")
    st.dataframe(filtered_df, height=800)
else:
    st.write("No data generated yet.")
