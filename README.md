# acc102_gamesales_tool_Yuhan.Jiang_2472066
XJTLU ACC102 Track4 - Global Game Sales Interactive Analysis Tool

# Online Tool Link


## 1. Project Purpose & Target Users
This interactive tool is designed for game industry analysts, researchers, marketing teams, and gaming enthusiasts.
It solves the problem of scattered game sales data and difficulty in analyzing industry trends, helping users quickly view and visualize global video game sales across platforms, genres, release years, and regions.

## 2. Dataset
1. Dataset name: Gamesalesdata.csv
2. Source: Kaggle
3. Date accessed: 2026-04-23
4. Features: Key Fields: Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales

## 3. Tools & Libraries Used
1. Python
2. Streamlit (Interactive interface)
3. Pandas (Data processing)
4. Matplotlib (Visualization)

## 4. Analysis Workflow
1. Load and cache data
2. Data cleaning (remove missing values in "Year" and "Publisher", adjust data types)
3. Data filtering by Platform, Genre, Year range
4. Group and aggregate sales data (e.g., sum sales by Genre/Region)
5. Visualize with bar charts (sales comparison), pie charts (region share), and trend lines (annual sales)

## 5. Key Functions
1. View data overview ( basic sales statistics)
2. Filter sales by Platform (e.g., only PS2 games)、Year range (e.g., 2000-2010)、Genre (e.g., only Action games)
3. Show top 10 best-selling games by Global_Sales/NA_Sales/JP_Sales
4. Compare regional sales preferences (e.g., JP_Sales vs NA_Sales for Role-Playing games)
5. Display global annual sales trends (1980-2020)

## 6. Key Findings
1. Action and Sports games dominate global sales (over 30% of total Global_Sales)
2. Regional preferences vary significantly: Role-Playing games have 40%+ share in JP_Sales, while Action games lead NA_Sales with 25%+
3. Global game sales peaked in 2008 (over 60 million USD in Global_Sales)

## 7. How to Run Locally
1. Install required packages: pip install -r requirements.txt
2. Navigate to the folder containing the script and run: streamlit run gamesales.py
3. Use the sidebar filters to select platform, genre, and release year.
4. Enter a game name to search.
5. View sales distribution by region and platform.
6. Analyze genre preferences and trends through visual charts.
7. View the Top 10 best-selling games list.


## 8. Author
1. Student ID: 2472066
2. Student Name: Yuhan.Jiang
3. Module: ACC102
