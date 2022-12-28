import streamlit as st
import yfinance as yf
import investpy as inv
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid

periods = ['30d','3mo','6mo','1y','5y']
tickers = inv.get_stocks_list("brazil")

def get_history():
    stock = yf.Ticker(ticker + ".SA")
    hist = stock.history(period=period)
    df = hist[['Open','Close','High','Low']]

    df.insert(4, 'Moving Average', df['Close'].rolling(window=20).mean(), allow_duplicates=False)
    df.insert(5, 'Standard Deviation', df['Close'].rolling(window=20).std(), allow_duplicates=False)
    df = df.dropna(axis=0, inplace=False)

    df.insert(6, 'Upper Band', df['Moving Average'] + (df['Standard Deviation'] * 2), allow_duplicates=False)
    df.insert(7, 'Lower Band', df['Moving Average'] - (df['Standard Deviation'] * 2), allow_duplicates=False)

    df.insert(8, 'Purchase', df['Close'][df['Close'] >= df['Upper Band']], allow_duplicates=False)
    df.insert(9, 'Sell', df['Close'][df['Close'] <= df['Lower Band']], allow_duplicates=False)

    return [df, stock]

def get_dividends_graph(df):

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['MonthYear'],
        y=df['Dividends'],
        name='Dividends',
        text=df['Dividends'],
    ))

    # fig.add_trace(
    #     go.Scatter(
    #     x=df['MonthYear'][df['Stock Splits'] > 0.0],
    #     y=df['Stock Splits'][df['Stock Splits'] > 0.0],
    #     name='Stock Splits',
    #     mode='markers',
    #     marker=dict(
    #         color='#c23616',
    #         size=12,
    #         symbol='x',
    #     ),
    # ))

    fig.update_layout(
        title=f'Dividends - {ticker}',
        showlegend=True,
        legend=dict(
            y=1.15,
            orientation="h"
        ),
        font=dict(color='#8a8d93'),
        yaxis=dict(
            showgrid=False, 
            showline=False,
        ),
        xaxis=dict(
            type='category', # Create Button to change this
            showgrid=False, 
            showline=False,
            linecolor='#8a8d93',
        ),
        margin=dict(t=100, b=30, l=30, r=30),
    )

    fig.update_traces(
        textfont_color='white', 
        marker=dict(
            color='#ff4b4b',
            opacity=0.7,
            line=dict(
                color='#ff4b4b',
                width=2
            )
        ),
        selector=dict(type='bar')
    )

    fig.update_layout(height=400)

    return fig

def get_analysis_graph(df):

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['YearPeriod'],
        y=df['Growth'],
        name='Growth',
        text=df['Growth'],
    ))

    fig.update_layout(
        title=f'Growth - {ticker}',
        showlegend=True,
        legend=dict(
            y=1.15,
            orientation="h"
        ),
        font=dict(color='#8a8d93'),
        yaxis=dict(
            showgrid=False, 
            showline=False,
        ),
        xaxis=dict(
            type='category', # Create Button to change this
            showgrid=False, 
            showline=False,
            linecolor='#8a8d93',
        ),
        margin=dict(t=100, b=30, l=30, r=30),
    )

    fig.update_traces(
        textfont_color='white', 
        marker=dict(
            color='#ff4b4b',
            opacity=0.7,
            line=dict(
                color='#ff4b4b',
                width=2
            )
        ),
        selector=dict(type='bar')
    )

    fig.update_layout(height=400)

    return fig

def get_bollinger_bands(df):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Lower Band'], 
        name='Low Band',
        line_color='rgba(0, 184, 148,0.3)',
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Upper Band'],
        name='Up Band',
        fill='tonexty',
        fillcolor='rgba(173, 204, 255, 0.05)',
        line_color='rgba(225, 112, 85,0.3)',
    ))
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Operation',
        increasing_line_color='rgba(0, 184, 148,0.7)',
        decreasing_line_color='rgba(225, 112, 85,0.7)',
        increasing_fillcolor='rgba(0, 184, 148,0.7)',
        decreasing_fillcolor='rgba(225, 112, 85,0.7)',
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Moving Average'],
        name='Moving Avg',
        line_color='rgba(253, 203, 110,0.5)',
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Purchase'],
        name='Purchase',
        mode='markers',
        marker=dict(
            color='#c23616',
            size=12,
            symbol='x',
        ),
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Sell'],
        name='Sell',
        mode='markers',
        marker=dict(
            color='#44bd32',
            size=12,
            symbol='cross',
        )
    ))

    fig.update_layout(
        title=f'Bollinger Bands - {ticker}',
        legend=dict(
            y=1,
            orientation="h"
        ),
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            tickmode='auto',
        )
    )

    fig.update_xaxes(gridcolor="rgba(255,255,255,0.15)", )
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.15)", )
    fig.update_layout(
        width=1700,
        height=900,
        font=dict(color='#8a8d93'),
        xaxis=dict(color='#8a8d93'),
        margin=dict(t=100, b=30, l=30, r=30),
    )

    return fig

st.set_page_config(layout='wide')

column1, column2, column3 = st.columns(3)

with column1:
    ticker = st.selectbox(
        'Select the Action or Real Estate Fund',
        tickers
    )

with column3:
    st.button(
        "REFRESH (1M)",
        type='primary'
    )

st.markdown(
    """
    <style>
        .etr89bj1{
            border-radius: 8px;
        }
        .stButton {
            display: flex;
            justify-content: flex-end;
        }
        .e1tzin5v4 {
            align-items: center;
        }
        .main-svg{
            border: solid 1px #303239;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

period =  option_menu(
    menu_title='Select the desired period',
    options=periods,
    icons=["calendar-check"] * len(periods),  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

if ticker:
    data = get_history()
    df = data[0]

    actions = data[1].get_actions()
    actions['Year'] = pd.DatetimeIndex(actions.index).year
    actions['Month'] = actions.index.month_name()
    actions['MonthYear'] = actions['Month'].apply(lambda x: x[:3]) + "-" + actions['Year'].apply(str)

    analysis = data[1].get_analysis()
    analysis = analysis[analysis["End Date"] != "NaT"]
    analysis['Year'] = pd.DatetimeIndex(analysis["End Date"]).year
    analysis['MonthNum'] = pd.DatetimeIndex(analysis["End Date"]).month
    analysis["YearPeriod"] = analysis['Year'].astype(str).apply(lambda x: None if x == "nan" else x.split(".")[0]) + " (" + analysis.index + ")"
    
    info = data[1].get_info()

    dividends_fig = get_dividends_graph(actions)
    analysis_fig = get_analysis_graph(analysis)
    fig = get_bollinger_bands(df)

    col1, col2, col3, col4 = st.columns(4)
    if len(info["logo_url"]) > 0:
        col1.image(info["logo_url"],width=90,use_column_width='never')
    else:
        pass
    col2.metric("Current Value", f"R$ {round(df['Close'][df.index.max()],2)}", f"{round((df['Close'][df.index.max()] / df['Close'][df.index[-2]] - 1) * 100, 2)}%")
    col3.metric("Minimum Value", f"R$ {round(df['Close'].min(),2)}", f"{round((df['Close'].min() / df['Close'][df.index.max()] - 1) * 100,2)}%")
    col4.metric("Maximum Value", f"R$ {round(df['Close'].max(),2)}", f"{round((df['Close'].max() / df['Close'][df.index.max()] - 1) * 100,2)}%")

    dividends_column, analysis_collumn = st.columns(2)

    with dividends_column:
        
        dividends_type_tab1, dividends_type_tab2 = st.tabs(['GRAPH','TABLE'])
            
        with dividends_type_tab1:
            st.plotly_chart(
                dividends_fig,
                use_container_width=True, 
                sharing="streamlit"
            )

        with dividends_type_tab2:
            df_actions_to_table = actions[['MonthYear', 'Dividends']]
            AgGrid(
                df_actions_to_table, 
                theme="streamlit",
                key='MonthYear', 
                fit_columns_on_grid_load=True, 
                reload_data=True, 
                width=200,
                height=400
            ) 

    with analysis_collumn:

        analysis_type_tab1, analysis_type_tab2 = st.tabs(['GRAPH','TABLE'])
            
        with analysis_type_tab1:
            st.plotly_chart(
                analysis_fig,
                use_container_width=True, 
                sharing="streamlit"
            )
        
        with analysis_type_tab2:
            df_analysis_to_table = analysis[['End Date', 'Growth']]
            AgGrid(
                df_analysis_to_table, 
                theme="streamlit",
                key='End Date', 
                fit_columns_on_grid_load=True, 
                reload_data=True, 
                width=200,
                height=400
            )
    # st.subheader("BOLLINGER BANDS")

    tab1, tab2 = st.tabs(["GRAPH", "TABLE"])
    
    with tab1:
        st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
    
    with tab2:
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].dt.normalize()
        df = df[['Date','Open','Close','High','Low','Upper Band','Lower Band','Purchase','Sell']]
        
        
        AgGrid(
            df, 
            theme="streamlit",
            key='Date', 
            fit_columns_on_grid_load=True, 
            reload_data=True, 
            height=600
        ) 
