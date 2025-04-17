from flask import Blueprint, jsonify, request, render_template
from services import get_stock_data, get_news, generate_stock_plot, analyze_sentiment

api_bp = Blueprint('api', __name__)

@api_bp.route('/stock', methods=['GET'])
def stock_info():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return render_template('index.html', stock_data=None, news=None, plot=None)

    # Get stock data
    stock_data = get_stock_data(ticker).tail(1)
    stock_data_json = stock_data.reset_index().to_dict(orient='records')

    # Get news articles
    news_response = get_news(ticker)
    articles = news_response.get("articles", [])[:5]

    # Add sentiment analysis
    for article in articles:
        article['sentiment'] = analyze_sentiment(article['title'])

    # Get interactive plot
    plot = generate_stock_plot(get_stock_data(ticker))

    return render_template('index.html',
                           ticker=ticker,
                           stock_data=stock_data_json,
                           news=articles,
                           plot=plot)
