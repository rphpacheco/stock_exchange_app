import streamlit as st
import investpy as inv
import datetime
import history as hist
import bollinger_bands as bollinger
import styles
import  streamlit_toggle as tog
import time

tickers = inv.get_stocks_list("brazil")

st.set_page_config(
    page_title='Stock Exchange',
    page_icon=':bar_chart:',
    layout='wide')

styles.set()

with st.sidebar:
    ticker = st.selectbox(
        'Select the Action or Real Estate Fund',
        tickers,
    )

    date_reference = st.date_input(
        "Select a init of period",
        datetime.datetime.today()
    )

    number_of_days = st.number_input('Insert a number of days', value=30)

    sleep_time = st.select_slider(
        'Select update time (seconds)',
        options=[5, 10, 15, 30, 60]
    )

    init_date = date_reference + datetime.timedelta(days=-(30 + number_of_days))
    end_date = date_reference

    toogle_column1, toogle_column2 = st.columns(2)

    with toogle_column1:
        st.write(f"Auto Refresh ({sleep_time}s)")
    with toogle_column2:
        toogle = tog.st_toggle_switch(
            key="Key1", 
            default_value=False, 
            label_after = False, 
            inactive_color = 'rgba(255, 75, 75, .5)', 
            active_color="rgb(255, 75, 75)", 
            track_color="rgba(255, 75, 75, .5)"
        )

def prepare_history_visualization():
    history, instance = hist.get(ticker, init_date=init_date, end_date=end_date) if init_date else hist.get(ticker)
    print("CURRENT PRICE ->", history["Close"].iat[-1])
    bollinger_figure = bollinger.get(ticker, history)

    current_value.metric("Current Value", f"R$ {round(history['Close'][history.index.max()],2)}", f"{round((history['Close'][history.index.max()] / history['Close'][history.index[-2]] - 1) * 100, 2)}%")
    min_value.metric("Minimum Value", f"R$ {round(history['Close'].min(),2)}", f"{round((history['Close'].min() / history['Close'][history.index.max()] - 1) * 100,2)}%")
    max_value.metric("Maximum Value", f"R$ {round(history['Close'].max(),2)}", f"{round((history['Close'].max() / history['Close'][history.index.max()] - 1) * 100,2)}%")

    graph.plotly_chart(bollinger_figure, use_container_width=True, sharing="streamlit")

if ticker and sleep_time:

    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_value = st.empty()
    with col2:
        min_value = st.empty()
    with col3:
        max_value = st.empty()
    graph = st.empty()

    while toogle:
        prepare_history_visualization()
        time.sleep(sleep_time)
    else:
        prepare_history_visualization()