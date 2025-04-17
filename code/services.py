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
    fig = go.Figure(data=[
        go.Scatter(x=hist_df.index, y=hist_df['Close'], mode='lines', name='Close')
    ])
    fig.update_layout(title="Stock Price Over Time", xaxis_title="Date", yaxis_title="Close Price")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
