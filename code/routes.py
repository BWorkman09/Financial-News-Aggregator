from flask import Blueprint, jsonify, request, render_template
from services import get_stock_data, get_news, generate_stock_plot, analyze_sentiment

api_bp = Blueprint('api', __name__)

@api_bp.route('/stock', methods=['GET'])
def stock_info():
    ticker = request.args.get('ticker', '').upper()
    range_period = request.args.get('range', '1mo')  # Default to 1 month

    if not ticker:
        return render_template('index.html', stock_data=None, news=None, plot=None)

    try:
        # Get stock data
        stock_data = get_stock_data(ticker, period=range_period)

        if stock_data.empty or stock_data['Close'].max() == 0:
            raise ValueError("No valid stock data found for this ticker.")

        stock_data_latest = stock_data.tail(1).reset_index().to_dict(orient='records')

        # Get news articles
        news_response = get_news(ticker)
        articles = news_response.get("articles", [])[:5]

        # Add sentiment analysis
        for article in articles:
            article['sentiment'] = analyze_sentiment(article['title'])

        # Generate interactive plot
        plot = generate_stock_plot(stock_data)

        return render_template('index.html',
                               ticker=ticker,
                               range=range_period,
                               stock_data=stock_data_latest,
                               news=articles,
                               plot=plot)

    except Exception as e:
        return render_template('index.html',
                               ticker=ticker,
                               stock_data=None,
                               news=None,
                               plot=None,
                               error=str(e))
