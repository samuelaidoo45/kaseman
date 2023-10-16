# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from views import main_views, auth_views, loan_classification,analytics,advance_classification
from flask_sqlalchemy import SQLAlchemy
from app.database import db

def create_app():
    app=Flask(__name__,template_folder='../templates', static_folder='../static')
    app.config.from_object('config.Config')

    db.init_app(app)
    
    migrate = Migrate(app,db)

    app.register_blueprint(main_views.bp)
    app.register_blueprint(loan_classification.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(advance_classification.bp)


    return app
