# views/main_views.py
from flask import Blueprint, render_template

bp = Blueprint('returns', __name__)

@bp.route('/returns')
def returns():
    return render_template('returns.html')
    
