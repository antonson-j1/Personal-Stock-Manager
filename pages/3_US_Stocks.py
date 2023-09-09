import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import os

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# US STOCKS SELECTOR")
st.sidebar.header("US Stocks")
st.write(
    """Live Data from US Stocks"""
)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
stock_listing_path = os.path.join(script_dir, "NASDAQ.csv")
stock_listing = pd.read_csv(stock_listing_path)


if 'stock' not in st.session_state:
    st.session_state.stock = None

start_date = st.sidebar.date_input("Start Date",value=datetime.date(2004, 8, 25), min_value=datetime.date(2004, 8, 25))
end_date = st.sidebar.date_input("End Date", value=datetime.date(2021, 4, 30), min_value=start_date, max_value=datetime.date(2021, 4, 30))
stock = st.sidebar.selectbox("Stock Symbol", stock_listing['Name'])
stock_add = st.sidebar.button("ADD")

if stock_add:
    st.session_state.stock = stock

# Initialize session_state
if 'session_stock_dict' not in st.session_state:
    st.session_state.session_stock_dict = {}
    st.session_state.session_stock_list = []


data = yf.download(stock, start=start_date, end=end_date)
data