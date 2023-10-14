# views/main_views.py
from flask import Blueprint, render_template

bp = Blueprint('loan_classification', __name__)

@bp.route('/loan_classification')
def loan_classification():
    return render_template('test_1.html')
    
