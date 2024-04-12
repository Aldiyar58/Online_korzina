from flask import render_template, request, jsonify, url_for, redirect
from app.search import bp
from app.models import Product, ProductList
from app.extensions import db
from sqlalchemy import func

family_id = '1'


@bp.route('/search', methods=['GET'])
def search_form():
    return render_template('search.html')

from flask import request, render_template, url_for
from math import ceil

from flask import request, render_template, url_for, redirect, flash

from flask import request, render_template, url_for, redirect, flash

from flask import request, render_template, url_for, redirect, flash

@bp.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get('query', '')  # Получение данных из запроса
    page = request.args.get('page', 1, type=int)  # Получение номера страницы из запроса
    per_page = 10  # Количество продуктов на странице

    if query.strip() == "":  # Если запрос пуст, отправляем обратно на страницу поиска с предупреждением
        flash("Query cannot be empty. Please enter a search term.", "warning")
        return redirect(url_for('search.search_form'))

    # Используем метод paginate для определения страницы и количества записей на страницу
    pagination = Product.query.filter(Product.name.ilike(f'%{query}%')).paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items  # Текущая страница результатов
    total = pagination.total  # Общее количество найденных продуктов

    # Подсчет количества страниц
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1

    return render_template('search_results.html', products=products, total_pages=total_pages, current_page=page, query=query)



@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    selected_products = request.form.getlist('selected_products')
    for product_id in selected_products:
        new_cart_item = ProductList(family_id=family_id, product_id=product_id)
        db.session.add(new_cart_item)
    db.session.commit()

    # Получаем все продукты в корзине для этого пользователя
    cart_items = ProductList.query.filter_by(family_id=family_id).all()
    product_ids = [item.product_id for item in cart_items]
    products_in_cart = Product.query.filter(Product.id.in_(product_ids)).all()

    return render_template('cart.html', products=products_in_cart)
