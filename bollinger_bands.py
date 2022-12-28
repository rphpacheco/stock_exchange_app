import plotly.graph_objects as go

def get(ticker, df):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Lower Band'], 
        name='Low Band',
        line_color='rgba(0, 184, 148,0.3)'
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
        plot_bgcolor="rgba(0,0,0,0)",
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