# views/main_views.py
from flask import Blueprint, render_template,jsonify
from models.loan_classification import LoanClassification


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    loan_classifications = LoanClassification.query.all()  # Retrieve all loan classifications from the database
    # Serialize the records into a JSON format
    serialized_loan_classifications = []
    for classification in loan_classifications:
        serialized_loan_classifications.append({
            'id': classification.id,
            'loan_classification_name': classification.loan_classification_name,
            'loan_classification_desc': classification.loan_classification_desc,
        })
    
    # loan_classes = jsonify(serialized_loan_classifications)

    return render_template('index.html',loan_classes=serialized_loan_classifications)
