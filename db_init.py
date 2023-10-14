from app import create_app, db
from models import loan_classification


app = create_app()

with app.app_context():
    db.create_all()