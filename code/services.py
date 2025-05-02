# services.py
import yfinance as yf
import requests
import plotly.graph_objects as go
import plotly
import json
from textblob import TextBlob
from functools import lru_cache
import pandas as pd

@lru_cache(maxsize=50)
def get_stock_data(ticker, period="1mo"):
    """Get stock data from Yahoo Finance with caching"""
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval="1d")
    # Sanity check: drop invalid rows
    hist = hist[hist['Close'] > 0]
    if hist.empty:
        raise ValueError("No valid stock data found for this ticker.")
    return hist

def get_news(ticker):
    """Get news for a stock ticker"""
    api_key = "410127e2b9e944089571482ea6d5c0eb"  # Replace with your real key
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    return response.json()

def analyze_sentiment(text):
    """Analyze sentiment of text"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def generate_stock_plot(hist_df):
    """Generate a JSON representation of a stock plot"""
    print("\n=== Plotting Close Prices ===")
    print(f"Data shape: {hist_df.shape}")
    print(hist_df[['Close']].head(5))
    
    # Reset index so Date becomes a column
    hist_df = hist_df.reset_index()
    
    # Ensure Date is in datetime format
    hist_df['Date'] = pd.to_datetime(hist_df['Date'])
    
    # Ensure 'Close' column is numeric and drop NaNs
    hist_df['Close'] = pd.to_numeric(hist_df['Close'], errors='coerce')
    hist_df = hist_df.dropna(subset=['Close'])
    
    print("\nAfter cleaning:")
    print(f"Data shape: {hist_df.shape}")
    print(hist_df[['Date', 'Close']].head(5))
    
    # Create trace for Plotly
    trace = go.Scatter(
        x=hist_df['Date'].dt.strftime('%Y-%m-%d'),  # Format dates as strings
        y=hist_df['Close'],
        mode='lines+markers',
        line=dict(color='#3182ce', width=2),
        marker=dict(size=5, color='#3182ce'),
        hovertemplate='<b>Date</b>: %{x}<br><b>Close</b>: $%{y:.2f}<extra></extra>',
        name='Close Price'
    )
    
    # Set y-axis range with some padding
    y_min = hist_df['Close'].min() * 0.98
    y_max = hist_df['Close'].max() * 1.02
    
    # Create layout
    layout = go.Layout(
        title='Stock Price Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(
            title='Close Price (USD)',
            range=[y_min, y_max],
            autorange=False
        ),
        template='plotly_white',
        hovermode='x unified',
        margin=dict(l=40, r=30, t=60, b=40),
        height=450,
        font=dict(family='Segoe UI, sans-serif', size=14)
    )
    
    # Create a plot dict in the format expected by the template
    plot_dict = {
        'data': [trace],
        'layout': layout
    }
    
    # Convert to JSON for embedding in template
    return json.dumps(plot_dict, cls=plotly.utils.PlotlyJSONEncoder)