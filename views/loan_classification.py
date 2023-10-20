# views/main_views.py
from flask import Blueprint, render_template,request
from app.database import db
from models.loan_classification import LoanClassification


bp = Blueprint('loan_classification', __name__)

@bp.route('/loan_classification')
def loan_classification():
    return render_template('test_1.html')

@bp.route('/loan_classification_uploads')
def loan_classification_uploads():
    return render_template('loan_classification_uploads.html')

@bp.route('/loan_file_upload', methods=['POST'])
def loan_file_upload():
    branchName = request.form.get('branchName')
    loanFile = request.form.get('loanFile')

    print(loanFile)

    return branchName
    
@bp.route('/create_loan_classification',methods=['POST'])
def create_loan_classification():
    loanClassName = request.form.get('loanClassName')
    loanClassDesc = request.form.get('loanClassDesc')

    new_loan_class = LoanClassification(loan_classification_name=loanClassName,loan_classification_desc=loanClassDesc)

    db.session.add(new_loan_class)
    db.session.commit()

    loan_classifications = LoanClassification.query.all()  # Retrieve all loan classifications from the database
    
    serialized_loan_classifications = []
    for classification in loan_classifications:
        serialized_loan_classifications.append({
            'id': classification.id,
            'loan_classification_name': classification.loan_classification_name,
            'loan_classification_desc': classification.loan_classification_desc,
        })
    
    return render_template('index.html',loan_classes=serialized_loan_classifications)
