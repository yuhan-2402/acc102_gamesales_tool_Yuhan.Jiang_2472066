#!/usr/bin/env python
# coding: utf-8

# pip install streamlit pandas matplotlib seaborn

import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Set page title
st.title("Global Game Sales Analysis Tool")

# Load data with cache
@st.cache_data()
def load_data():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_folder,"Gamesalesdata.csv")
    df = pd.read_csv(file_path)
    return df

# Load data and handle error
try:
    data = load_data()
    st.write("Data Preview:")
    st.dataframe(data.head())
except Exception as e:
    st.error(f"Error loading data: {e}")

# Data cleaning and basic statistics
st.header("Data Cleaning and Basic Statistics")

missing_values = data.isnull().sum()
st.write("Number of rows with missing values per column:")
st.write(missing_values)

df_clean = data.dropna()
df_clean['Year'] = df_clean['Year'].astype(int)
st.write(f"Number of rows after cleaning: {len(df_clean)}")

# Game search function
game_name = st.text_input("🔍Enter the game name to search:")

if game_name:
    game_data = df_clean[df_clean['Name'].str.contains(game_name, case=False, na=False)]

    if not game_data.empty:
        game_record = game_data.sort_values(by='Global_Sales', ascending=False).iloc[0]
        global_sales = float(game_record['Global_Sales'])

        st.subheader(f"Sales information for: {game_record['Name']}")

        sales_by_region = {
            'North America': float(game_record['NA_Sales']),
            'Europe': float(game_record['EU_Sales']),
            'Japan': float(game_record['JP_Sales']),
            'Other': float(game_record['Other_Sales'])
        }
        total_sales = float(game_record['Global_Sales'])

        st.write("### Regional Sales (in millions)")
        for region, sale in sales_by_region.items():
            st.write(f"{region}: {sale:.2f}")

        st.write(f"### Total Global Sales: {total_sales:.2f}")
        st.bar_chart(pd.Series(sales_by_region))
    else:
        st.write("No game found with that name.")

# Basic dataset statistics
st.subheader("Basic Statistics")

total_games = df_clean['Name'].nunique()
st.write(f"Number of games: {total_games}")

total_platforms = df_clean['Platform'].nunique()
st.write(f"Number of platforms: {total_platforms}")

min_year = int(df_clean['Year'].min())
max_year = int(df_clean['Year'].max())
st.write(f"Release year range: {min_year} - {max_year}")

total_genres = df_clean['Genre'].nunique()
st.write(f"Number of genres: {total_genres}")

# Interactive filter section
st.header("Interactive Filters")

# Sidebar filters
platforms = st.sidebar.multiselect("Select Platform(s):", df_clean["Platform"].unique())
genres = st.sidebar.multiselect("Select Genre(s):", df_clean["Genre"].unique())
year_range = st.sidebar.slider("Select Release Year Range:", min_value = min_year, max_value = max_year,value = (min_year, max_year))

# Smart filtering logic
filtered_df = df_clean.copy()

if platforms:
    filtered_df = filtered_df[filtered_df['Platform'].isin(platforms)]

if genres:
    filtered_df = filtered_df[filtered_df['Genre'].isin(genres)]

filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]

total_sales = filtered_df["Global_Sales"].sum()
st.write(f"Total sales after filtering: {total_sales:.2f} million units")

# Platform sales chart
platform_sales = filtered_df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False)
st.subheader("Global Sales Distribution by Platform")
st.bar_chart(platform_sales)

# Genre sales pie chart
genre_sales = filtered_df.groupby('Genre')['Global_Sales'].sum()
st.subheader("Global Sales Distribution by Genre")

fig, ax = plt.subplots()
ax.pie(genre_sales, labels=genre_sales.index, autopct="%1.1f%%", startangle=140)
ax.axis('equal')
st.pyplot(fig)

# Top 10 best-selling games
st.subheader("👑 Top 10 Best Selling Games")

top10_games=filtered_df.sort_values(by="Global_Sales",ascending=False).head(10)
top10_display= top10_games[["Name","Platform","Year","Genre","Global_Sales"]]
st.dataframe(top10_display, use_container_width=True, hide_index=True)
st.bar_chart(top10_display.set_index("Name")["Global_Sales"], use_container_width=True)

# Regional genre preference analysis
st.header("Regional Genre Preference Comparison")

if filtered_df.empty:
    st.warning("No data available for the current filter.")
else:
    plot_type = st.radio("Chart Type:", ["Bar Chart", "Pie Chart"], horizontal=True)

    regions = {"North America": "NA_Sales", "Europe": "EU_Sales", "Japan": "JP_Sales", "Other Regions": "Other_Sales"}

    genre_by_region = {}
    for region_name, sale_col in regions.items():
        genre_sales = filtered_df.groupby("Genre")[sale_col].sum().sort_values(ascending=False)
        genre_by_region[region_name] = genre_sales

    if plot_type == "Bar Chart":
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        for i, (region, sales_data) in enumerate(genre_by_region.items()):
            axes[i].barh(sales_data.index, sales_data.values, color=f"C{i}")
            axes[i].set_title(f"{region} Genre Preference")
            axes[i].set_xlabel("Total Sales (millions)")
            axes[i].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)

    else:
        tabs = st.tabs(list(regions.keys()))
        for i, (region, sales_data) in enumerate(genre_by_region.items()):
            with tabs[i]:
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(sales_data, labels=sales_data.index, autopct="%1.1f%%", startangle=140)
                ax.axis("equal")
                st.pyplot(fig)

    st.subheader("Most Popular Genre by Region")
    summary = []
    for region, sales_data in genre_by_region.items():
        top_genre = sales_data.index[0]
        top_sales = round(sales_data.iloc[0], 2)
        summary.append({"Region": region, "Top Genre": top_genre, "Total Sales (M)": top_sales})
    
    st.table(summary)

# Add trend chart at bottom of sidebar
with st.sidebar:
    st.subheader("Sales Trend by Year")
    year_sales = df_clean.groupby('Year')['Global_Sales'].sum()
    st.line_chart(year_sales)

# Show filtered record count at sidebar bottom
with st.sidebar:
    st.markdown("---")
    st.caption("Filtered records:")
    st.metric("", len(filtered_df))