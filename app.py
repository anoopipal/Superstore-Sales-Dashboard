
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Superstore Sales Analysis Dashboard")

# Load Dataset
df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')
    encoding='latin1'
)

df['Order Date'] = pd.to_datetime(df['Order Date'])

# Sidebar Filters
st.sidebar.header("Dashboard Filters")

category = st.sidebar.multiselect(
    "Select Category",
    df['Category'].unique(),
    default=df['Category'].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    df['Region'].unique(),
    default=df['Region'].unique()
)

segment = st.sidebar.multiselect(
    "Select Segment",
    df['Segment'].unique(),
    default=df['Segment'].unique()
)

# Filter Data
filtered_df = df[
    (df['Category'].isin(category)) &
    (df['Region'].isin(region)) &
    (df['Segment'].isin(segment))
]

# KPI Cards
st.subheader("Business Performance")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
col3.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")

# Chart 1
st.subheader("Sales by Category")

category_sales = filtered_df.groupby(
    'Category'
)['Sales'].sum().reset_index()

fig1 = px.bar(
    category_sales,
    x='Category',
    y='Sales',
    color='Category',
    title='Sales by Category'
)

st.plotly_chart(fig1, use_container_width=True)

# Chart 2
st.subheader("Profit by Region")

region_profit = filtered_df.groupby(
    'Region'
)['Profit'].sum().reset_index()

fig2 = px.bar(
    region_profit,
    x='Region',
    y='Profit',
    color='Region',
    title='Profit by Region'
)

st.plotly_chart(fig2, use_container_width=True)

# Chart 3
st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales']
    .sum()
    .reset_index()
)

monthly_sales['Month'] = monthly_sales['Order Date'].astype(str)

fig3 = px.line(
    monthly_sales,
    x='Month',
    y='Sales',
    markers=True,
    title='Monthly Sales Trend'
)

st.plotly_chart(fig3, use_container_width=True)

# Data Table
st.subheader("Sales Data")
st.dataframe(filtered_df.head(20))
