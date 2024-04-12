from flask import render_template, jsonify, url_for, redirect, request, make_response, current_app
from flask_jwt_extended import jwt_required, get_jwt
from app import mail
from flask_mail import Message
from app.models import Product, User
from app.main import bp
import requests as rq
from http.cookies import SimpleCookie


def extract_cookies(response):
    cookies = SimpleCookie()
    for value in response.headers.get_all('Set-Cookie'):
        cookies.load(value)
    return {key: morsel.value for key, morsel in cookies.items()}


@bp.route('/')
def index():
    return redirect(url_for(endpoint='main.sign_up'))


@bp.route('/send/invite', methods=['GET', 'POST'])
def send_invite():
    if request.method == "POST":
        recipient = request.form['recipient_email']
        user_id = "0cdfd8e0-f7d4-4e86-85a2-0a3ec16f6c2b"
        sender = User.get_user_by_id(user_id=user_id)
        msg = Message(f"http://127.0.0.1:5000/claim/invite/{sender.email}/{recipient}/",
                      recipients=[recipient])
        mail.send(msg)
        return redirect(url_for(endpoint="main.index"))


    return render_template("SendMail.html")


@bp.route("/claim/invite/<string:inviter>/<string:email>/", methods=["GET", "POST"])
def claim_invite(inviter, email):
    response = User.join_in_family(inviter_email=inviter, email=email)
    print(inviter, email)
    print(response)
    return redirect(url_for(endpoint='main.index'))


@bp.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        with current_app.test_client() as client:
            response = client.post('/api/auth/login', json={
                'email': request.form['email'],
                'password': request.form['password']
            })

            if response.status_code == 200:
                cookies = extract_cookies(response)

                data = response.get_json()
                access_token = data.get('access_token')
                print(cookies['refresh_token_cookie'])
                refresh_token = cookies['refresh_token_cookie']

                redirect_response = make_response(redirect(url_for('main.index')))

                redirect_response.set_cookie('refresh_token_cookie', value=refresh_token, httponly=True, secure=True,
                                             path='/api/auth/refresh')
                redirect_response.set_cookie('access_token_cookie', value=access_token, httponly=True, secure=True)

                return redirect_response

    return render_template('signin.html')


@bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/api/auth/register'
        data = {
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_password': request.form['RepeatPassword'],
            'firstname': request.form['firstname'],
            'lastname': request.form['lastname'],
            'family_name': request.form['FamilyName']
            }
        response = rq.post(url, json=data)
        if response.status_code == 200:
            return redirect(url_for(endpoint='main.sign_in'))
        print(response)
    return render_template('signup.html')
