# from flask import render_template, request, jsonify, url_for, redirect
# from app.search import bp
# from app.models import Product
#
# @bp.route('/search', methods=['GET'])
# def search_form():
#     return render_template('search.html')
#
#
# @bp.route('/search_results', methods=['GET', 'POST'])
# def search():
#     query = request.args.get('query', '')  # Получение данных из формы
#     if query:
#         products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
#     else:
#         products = Product.query.all()
#     return render_template('search_results.html', products=products)

# app/search/routes.py
from flask import render_template, request, jsonify, url_for, redirect
from app.search import bp
from app.models import Product


@bp.route('/search', methods=['GET'])
def search_form():
    return render_template('search.html')


@bp.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get('query', '')  # Получение данных из запроса
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all() if query else []
    return render_template('search_results.html', products=products)