# run.py
from app import create_app
from models import loan_classification, loan_classification_files, loan_classification_items

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


