from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Agreement

bp = Blueprint('agreements', __name__)

@bp.route('/agreements')
@login_required
def list_agreements():
    agreements = Agreement.query.filter_by(user_id=current_user.id).all()
    return render_template('agreements.html', agreements=agreements)

@bp.route('/agreements/create', methods=['GET', 'POST'])
@login_required
def create_agreement():
    if request.method == 'POST':
        agreement = Agreement(
            title=request.form['title'],
            description=request.form['description'],
            user_id=current_user.id
        )
        db.session.add(agreement)
        db.session.commit()
        flash('Agreement created successfully!')
        return redirect(url_for('agreements.list_agreements'))
    return render_template('create.html')