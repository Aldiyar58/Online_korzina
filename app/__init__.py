from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app.extensions import db, jwt, mail  # , socketio
from app.models import User, TokenBlocklist


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    # Initialize Flask extensions here
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    # socketio.init_app(app)
    print(db)

    # Register blueprints here
    from app.search import bp as search_bp
    app.register_blueprint(search_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    # load user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(email=identity).one_or_none

    # additional claims

    # @jwt.additional_claims_loader
    # def make_additional_claims(identity):
    #     if identity.get('role') == "admin":
    #         return {"is_staff": True}
    #     return {'is_staff': False}

    # jwt error handlers

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"error": "token_expired", "message": "Token jas expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'message': 'signature verification failed', "error": 'invalid_token'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'message': 'Request doesnt contain valid token', 'error': 'authorization_header'}), 401

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']
        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

        return token is not None

    return app


if __name__ == '__main__':
    app = create_app()
    # from app.extensions import db
    # from app.models import User, Profile, TokenBlocklist, product, ProductList
    # with app.app_context():
    #     db.drop_all()
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
