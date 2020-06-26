from flask import Flask

from blueprints.auth import bp as auth_bp
from blueprints.users import bp as users_bp
from blueprints.categories import bp as categories_bp
from blueprints.transactions import bp as transactions_bp
from blueprints.report import bp as report_bp

from database import db


def create_app():
	app = Flask(__name__)
	app.config.from_object('config.Config')
	app.register_blueprint(auth_bp, url_prefix='/auth')
	app.register_blueprint(users_bp, url_prefix='/users')
	app.register_blueprint(categories_bp, url_prefix='/categories')
	app.register_blueprint(transactions_bp, url_prefix='/transactions')
	app.register_blueprint(report_bp, url_prefix='/report')
	db.init_app(app)
	return app
