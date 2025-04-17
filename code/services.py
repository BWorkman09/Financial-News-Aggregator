import yfinance as yf
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d")
    return hist

def get_news(ticker):
    api_key = "410127e2b9e944089571482ea6d5c0eb"
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    return response.json()

def generate_stock_plot(hist_df):
    fig = go.Figure(data=[go.Scatter(x=hist_df.index, y=hist_df['Close'])])
    fig.update_layout(title="Stock Price Chart", xaxis_title="Date", yaxis_title="Close Price")
    return fig.to_json()

