import pandas as pd
import streamlit as st
import plotly.express as px

# Set the page layout to wide
st.set_page_config(layout="wide")

# Apply custom styling for a cleaner look
st.markdown("""
    <style>
    .main {
        background-color: #1c1e22;
        padding: 10px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
data = pd.read_csv("data/weather_data.csv")

# App Title and Introduction
st.title("Weather-Based Recommendation System")
st.write("Analyze weather data, get personalized recommendations, and visualize key weather patterns.")

# Sidebar for User Preferences
st.sidebar.header("Set Your Weather Preferences")
temp_threshold = st.sidebar.slider("Temperature Threshold (°C)", min_value=15, max_value=40, value=30)
uv_threshold = st.sidebar.slider("UV Index Threshold", min_value=1, max_value=12, value=8)
rain_threshold = st.sidebar.slider("Precipitation Threshold (mm)", min_value=0, max_value=100, value=50)

# Date Range Filter
st.sidebar.header("Filter Data by Date Range")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime(data["Date"]).min())
end_date = st.sidebar.date_input("End Date", pd.to_datetime(data["Date"]).max())

# Apply date range filter
data = data[(pd.to_datetime(data["Date"]) >= pd.to_datetime(start_date)) & 
            (pd.to_datetime(data["Date"]) <= pd.to_datetime(end_date))]

# Create three columns with adjusted widths
col1, col2, col3 = st.columns([1.2, 2.3, 2.0])

# Column 1: Recommendations
with col1:
    st.subheader("Weather-Based Recommendations")
    filtered_data = data[
        (data["Temperature"] >= temp_threshold) |
        (data["UV_Index"] >= uv_threshold) |
        (data["Precipitation"] >= rain_threshold)
    ]

    if not filtered_data.empty:
        for _, row in filtered_data.iterrows():
            recommendations = []

            if row["Temperature"] >= temp_threshold:
                recommendations.append(f"High Temperature Alert: {row['Temperature']}°C. Stay hydrated and avoid outdoor activities.")

            if row["UV_Index"] >= uv_threshold:
                recommendations.append(f"High UV Index Alert: {row['UV_Index']}. Apply sunscreen and wear protective clothing.")

            if row["Precipitation"] >= rain_threshold:
                recommendations.append(f"Heavy Rain Alert: {row['Precipitation']}mm. Consider carrying an umbrella.")

            if recommendations:
                st.write(f"**Date: {row['Date']}** - {' '.join(recommendations)}")
    else:
        st.write("No alerts for the selected thresholds.")

# Column 2: Data Overview and Temperature Trend
with col2:
    st.subheader("Data Overview")
    st.write(data.head())

    st.subheader("Temperature Trend Over Time")
    fig_temp = px.line(
        data, 
        x="Date", 
        y="Temperature", 
        title="Daily Temperature Over Time",
        color_discrete_sequence=["#3498db"],
        height=300  # Reduced height
    )

    # Highlight high temperatures
    fig_temp.add_scatter(
        x=data[data["Temperature"] >= temp_threshold]["Date"],
        y=data[data["Temperature"] >= temp_threshold]["Temperature"],
        mode="markers",
        marker=dict(color="red", size=6),
        name="High Temp Alert"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

# Column 3: UV Index and Precipitation
with col3:
    st.subheader("UV Index Distribution")
    fig_uv = px.bar(
        data, 
        x="Date", 
        y="UV_Index", 
        title="UV Index Levels Over Time", 
        color="UV_Index",
        color_continuous_scale="Blues",
        height=250  # Reduced height
    )
    st.plotly_chart(fig_uv, use_container_width=True)

    st.subheader("Precipitation Levels Over Time")
    fig_precip = px.bar(
        data, 
        x="Date", 
        y="Precipitation", 
        title="Precipitation Levels Over Time", 
        color="Precipitation",
        color_continuous_scale="Blues",
        height=250  # Reduced height
    )
    st.plotly_chart(fig_precip, use_container_width=True)
