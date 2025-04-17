from flask import Blueprint, jsonify, request
from .services import get_stock_data, get_news, generate_stock_plot

api_bp = Blueprint('api', __name__)

@api_bp.route('/stock/<string:ticker>', methods=['GET'])
def stock_info(ticker):
    stock_data = get_stock_data(ticker).tail(1).to_dict()
    news = get_news(ticker, api_key="YOUR_NEWSAPI_KEY")
    return jsonify({
        "stock_data": stock_data,
        "news": news["articles"][:5]
    })

@api_bp.route('/plot/<string:ticker>', methods=['GET'])
def stock_plot(ticker):
    hist = get_stock_data(ticker)
    plot_json = generate_stock_plot(hist)
    return jsonify({"plot": plot_json})

