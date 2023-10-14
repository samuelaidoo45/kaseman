# run.py
from app import create_app
from models import loan_classification

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
