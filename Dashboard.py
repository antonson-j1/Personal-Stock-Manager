import pandas as pd
import streamlit as st
from PIL import Image
import altair as alt
import datetime
import yfinance as yf
import os

stock_dict = {}
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
dataset_list = os.listdir(os.path.join(script_dir, "data"))
dataset_list = [filename.replace('.csv', '') for filename in dataset_list]

image1 = Image.open(os.path.join(script_dir, "images/img1.png"))


# Initialize session_state
if 'session_stock_dict' not in st.session_state:
    st.session_state.session_stock_dict = {}
    st.session_state.session_stock_list = []
    st.session_state.combined_chart_list = []

st.set_page_config(
    page_title="Hello",
    page_icon="G",
)

st.title("""
Stock Portfolio Manager
### Personal Portfolio Manager... 
""")

st.image(image1, use_column_width= True)
st.sidebar.header("Create Portfolio: ")

def get_input():
    start_date = st.sidebar.date_input("Start Date",value=datetime.date(2004, 8, 25), min_value=datetime.date(2004, 8, 25))
    end_date = st.sidebar.date_input("End Date", value=datetime.date(2021, 4, 30), min_value=start_date, max_value=datetime.date(2021, 4, 30))
    stock = st.sidebar.selectbox("Stock Symbol", dataset_list)
    return start_date, end_date, stock

def get_data(start, end, symbol):
    dataset_path = "data/" + symbol.upper() + ".csv"
    df      = pd.read_csv(os.path.join(script_dir, dataset_path))
    start   = pd.to_datetime(start)
    end     = pd.to_datetime(end)
    start_row = 0
    end_row = 0

    for i in range(0, len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break

    for i in range(0, len(df)):
        if end >= pd.to_datetime(df['Date'][len(df)-1-i]):
            end_row = len(df)-1-i
            break

    df = df.set_index(pd.DatetimeIndex(df["Date"].values))
    return df.iloc[start_row : end_row+1 , :]


start, end, selected_stock = get_input()
ticker = st.sidebar.text_input('Ticker', "MSFT")
data = yf.download(ticker, start=start, end=end)
data
st.line_chart(data['Close'])

# Check if the selected stock is not already in session_stock_list
if selected_stock not in st.session_state.session_stock_list:
    st.session_state.session_stock_list.append(selected_stock)

# Create or update session_stock_dict with the selected stock's data
st.session_state.session_stock_dict[selected_stock] = get_data(start, end, selected_stock)


# Display all selected stocks
st.write("## Line Charts for Selected Stocks")

for stock_symbol in st.session_state.session_stock_list:
    # st.write(f"### {stock_symbol} Stock Price")
    chart = alt.Chart(st.session_state.session_stock_dict[stock_symbol]).mark_line().encode(
        x='Date:T',
        y='Close:Q',
        tooltip=['Date:T', 'Close:Q'],
        text = alt.value(stock_symbol)
    ).properties(
        width=800,
        height=400
    )
    st.session_state.combined_chart_list.append(chart)
    
combined_chart = alt.layer(*st.session_state.combined_chart_list)
st.altair_chart(combined_chart.interactive(), use_container_width=True)

st.header("Data Statistics of {}".format(selected_stock))
st.write(st.session_state.session_stock_dict[selected_stock].describe())


st.sidebar.header("\n\nSelected Stocks: ")
for stock in st.session_state.session_stock_list:
    st.sidebar.markdown(stock)