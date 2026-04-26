#!/usr/bin/env python
# coding: utf-8

# Import required libraries
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Configure page layout
st.set_page_config(page_title="Game Sales Analysis", layout="wide")
st.title("Global Game Sales Analysis Tool")

# Load dataset with cache
@st.cache_data()
def load_data():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_folder,"Gamesalesdata.csv")
    return pd.read_csv(file_path)

data = load_data()

# Data preprocessing
missing_values = data.isnull().sum()
df_clean = data.dropna()
df_clean['Year'] = df_clean['Year'].astype(int)
min_year = int(df_clean['Year'].min())
max_year = int(df_clean['Year'].max())

# Initialize session states
if "nav_choice" not in st.session_state:
    st.session_state.nav_choice = "Overview Trends"

if "platforms" not in st.session_state:
    st.session_state.platforms = []
if "genres" not in st.session_state:
    st.session_state.genres = []
if "year_range" not in st.session_state:
    st.session_state.year_range = (min_year, max_year)

# Sidebar navigation
with st.sidebar:
    st.subheader("Dashboard Navigation")
    nav_list = ["Overview Trends", "Game Search", "Top 10 Games", "Regional Analysis", "Data Overview"]
    st.session_state.nav_choice = st.selectbox("Jump to", nav_list, index=nav_list.index(st.session_state.nav_choice))
    
    # Reset button (only clear filters)
    if st.button("Reset Filters"):
        st.session_state.platforms = []
        st.session_state.genres = []
        st.session_state.year_range = (min_year, max_year)
        st.rerun()

# Filter widgets with session state
platforms = st.sidebar.multiselect("Platforms", df_clean["Platform"].unique(), key="platforms")
genres = st.sidebar.multiselect("Genres", df_clean["Genre"].unique(), key="genres")
year_range = st.sidebar.slider("Year Range", min_value=min_year, max_value=max_year, key="year_range")

# Apply filters
filtered_df = df_clean.copy()
if len(platforms) > 0:
    filtered_df = filtered_df[filtered_df['Platform'].isin(platforms)]
if len(genres) > 0:
    filtered_df = filtered_df[filtered_df['Genre'].isin(genres)]

filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]

# Sidebar info
with st.sidebar:
    st.caption("Filtered records")
    st.metric("", len(filtered_df))

    st.subheader("Data Cleaning")
    st.write("Cleaned records:", len(df_clean))
    st.subheader("Missing Values Summary")
    st.dataframe(missing_values, use_container_width=True)
    st.subheader("Basic Statistics")
    st.write("Total Games:", df_clean['Name'].nunique())
    st.write("Platforms:", len(df_clean['Platform'].unique()))
    st.write("Year Range:", f"{min_year}-{max_year}")
    st.write("Genres:", len(df_clean['Genre'].unique()))

# Anchor mapping
anchor_map = {"Overview Trends":"overview","Game Search":"search","Top 10 Games":"top10","Regional Analysis":"regional","Data Overview":"data"}

# Data Overview
st.markdown('<div id="data"></div>', unsafe_allow_html=True)
st.subheader("Data Overview")
st.dataframe(data.head(10), use_container_width=True)

# Overview Trends
st.markdown('<div id="overview"></div>', unsafe_allow_html=True)
st.subheader("Global Sales Overview & Trends")
col1, col2 = st.columns(2)
with col1:
    st.write("**Yearly Global Sales Trend**")
    st.line_chart(df_clean.groupby('Year')['Global_Sales'].sum())
with col2:
    st.write("**Yearly Game Releases Count**")
    st.line_chart(df_clean.groupby('Year').size())

col3, col4 = st.columns(2)
with col3:
    st.write("**Top 10 Platforms by Sales**")
    st.bar_chart(df_clean.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10))
with col4:
    st.write("**Top 10 Genres by Sales**")
    st.bar_chart(df_clean.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).head(10))

# Game Search
st.markdown('<div id="search"></div>', unsafe_allow_html=True)
st.subheader("Game Search")
game_name = st.text_input("🔍 Enter the game name to search:")
if game_name:
    game_data = df_clean[df_clean['Name'].str.contains(game_name, case=False, na=False)]
    if not game_data.empty:
        game_record = game_data.sort_values(by='Global_Sales', ascending=False).iloc[0]
        st.subheader(f"Sales Information: {game_record['Name']}")
        sales = {'North America': float(game_record['NA_Sales']), 'Europe': float(game_record['EU_Sales']), 'Japan': float(game_record['JP_Sales']), 'Other': float(game_record['Other_Sales'])}
        for region, sale in sales.items():
            st.write(f"{region}: {sale:.2f}M")
        st.bar_chart(pd.Series(sales))

# Top 10 Games
st.markdown('<div id="top10"></div>', unsafe_allow_html=True)
st.subheader("👑 Top 10 Best Selling Games")
top10 = filtered_df.sort_values('Global_Sales', ascending=False).head(10)[["Name","Platform","Year","Genre","Global_Sales"]]
st.dataframe(top10, use_container_width=True, hide_index=True)
st.bar_chart(top10.set_index("Name")["Global_Sales"])

# Regional Analysis
st.markdown('<div id="regional"></div>', unsafe_allow_html=True)
st.header("Regional Genre Preference Comparison")
if not filtered_df.empty:
    plot_type = st.radio("Chart Type", ["Bar Chart", "Pie Chart"], horizontal=True)
    regions = {"NA":"NA_Sales","EU":"EU_Sales","JP":"JP_Sales","Other":"Other_Sales"}
    for name, col in regions.items():
        data_region = filtered_df.groupby("Genre")[col].sum().sort_values(ascending=False).head(5)
        st.subheader(f"{name} Region Top Genres")
        if plot_type == "Bar Chart":
            st.bar_chart(data_region)
        else:
            fig, ax = plt.subplots()
            ax.pie(data_region, labels=data_region.index, autopct="%1.1f%%")
            st.pyplot(fig)

# Smooth scroll
target_id = anchor_map[st.session_state.nav_choice]
scroll_js = f"""<script>window.onload=function(){{let el=parent.document.getElementById('{target_id}');if(el)el.scrollIntoView({{behavior:'smooth'}});}}</script>"""
st.components.v1.html(scroll_js, height=0)
