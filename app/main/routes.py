from flask import render_template, jsonify, url_for, redirect
from app.main import bp


@bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    return render_template('signup.html')