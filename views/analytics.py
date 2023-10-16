# views/main_views.py
from flask import Blueprint, render_template

bp = Blueprint('analytics', __name__)

@bp.route('/analytics')
def analytics():
    return render_template('analytics.html')
    
