from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Room

bp = Blueprint('rooms', __name__)

@bp.route('/rooms')
@login_required
def rooms():
    rooms = Room.query.filter_by(user_id=current_user.id).all()
    return render_template('rooms.html', rooms=rooms)

@bp.route('/rooms/create', methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        room = Room(name=request.form['name'], description=request.form['description'], user_id=current_user.id)
        db.session.add(room)
        db.session.commit()
        flash('Room created successfully!')
        return redirect(url_for('rooms.rooms'))
    return render_template('create_room.html')