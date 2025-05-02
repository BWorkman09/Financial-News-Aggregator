import yfinance as yf
import requests
import plotly.graph_objects as go
import plotly
import json
from textblob import TextBlob
from functools import lru_cache

@lru_cache(maxsize=50)
def get_stock_data(ticker, period="1mo"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def get_news(ticker):
    api_key = "410127e2b9e944089571482ea6d5c0eb"  # Replace with your real key
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    return response.json()

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def generate_stock_plot(hist_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hist_df.index,
        y=hist_df['Close'],
        mode='lines+markers',
        line=dict(color='#3182ce', width=2),
        marker=dict(size=5, color='#3182ce'),
        hovertemplate='<b>Date</b>: %{x|%b %d, %Y}<br><b>Close</b>: $%{y:.2f}<extra></extra>',
        name='Close Price'
    ))

    fig.update_layout(
        title='Stock Price Over Time',
        xaxis_title='Date',
        yaxis_title='Close Price (USD)',
        template='plotly_white',
        hovermode='x unified',
        margin=dict(l=40, r=30, t=60, b=40),
        height=450,
        font=dict(family='Segoe UI, sans-serif', size=14),
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


