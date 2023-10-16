# views/main_views.py
from flask import Blueprint, render_template,request

bp = Blueprint('loan_classification', __name__)

@bp.route('/loan_classification')
def loan_classification():
    return render_template('test_1.html')
    
@bp.route('/create_loan_classification',methods=['POST'])
def create_loan_classification():
    loan_class_name = request.form.get('loanClassName')
    loan_class_desc = request.form.get('loanClassDesc')
    
    print("Loan Class Name:",loan_class_name)
    print("Loan Class Description:",loan_class_desc)

    return render_template('index.html')