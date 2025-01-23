from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Agreement, Room

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    agreements = Agreement.query.filter_by(user_id=current_user.id).all()
    rooms = Room.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', agreements=agreements, rooms=rooms)