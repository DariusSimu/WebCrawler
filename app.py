from flask import Flask, request, jsonify, send_from_directory
from Backend.MainCrawler import search_all
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('Frontend', 'MainPage.html')

@app.route('/Style.css')
def styles():
    return send_from_directory('Frontend', 'Style.css')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))
    if not query:
        return jsonify([])
    results = search_all(query, limit)
    return jsonify([result.__dict__ for result in results])

if __name__ == '__main__':
    app.run(debug=True)