from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Habit, Habitlist
from . import db
from datetime import datetime, timedelta
from sqlalchemy.sql import func

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    habitlist = Habitlist.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, habitlist=habitlist)

@views.route('/add-habit', methods=['POST'])
@login_required
def add_habit():
    name = request.form.get('name')
    frequency = request.form.get('frequency')
    description = request.form.get('description')  # Add description field
    
    # Check if required fields are filled
    if not name or not frequency:
        flash('Please fill in all fields', 'error')
    else:
        # Add the new habit to the database
        new_habit = Habit(
            name=name,
            frequency=frequency,
            description=description,
            start_date=func.now(),  # Set the start date to the current time
            times_completed=0,      # Initialize times completed to 0
            last_completed=None    # Initialize last completed as None
        )
        db.session.add(new_habit)
        db.session.commit()

        # Create a new habit entry in the user's habitlist, with status as False (Todo)
        new_habitlist = Habitlist(user_id=current_user.id, habit_id=new_habit.id, status=False)
        db.session.add(new_habitlist)
        db.session.commit()

        flash('Habit added to your tracker!', 'success')

    return redirect(url_for('views.home'))

@views.route('/update-habit-status/<int:habit_id>', methods=['POST'])
@login_required
def update_habit_status(habit_id):
    data = request.get_json()
    new_status = data.get('status')

    # Find the habit in the Habitlist for the user and habit ID
    habitlist_item = Habitlist.query.filter_by(habit_id=habit_id, user_id=current_user.id).first()

    if habitlist_item:
        habitlist_item.status = True if new_status == 'Done' else False
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Habit not found."})

@views.route('/delete-habitlist/<int:id>', methods=['POST'])
@login_required
def delete_habitlist(id):
    habitlist_item = Habitlist.query.get_or_404(id)
    db.session.delete(habitlist_item)
    db.session.commit()
    return redirect(url_for('views.home'))

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/edit-habit/<int:habit_id>', methods=['GET', 'POST'])
@login_required
def edit_habit(habit_id):
    habit = Habit.query.get(habit_id)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        frequency = request.form.get('frequency')
        start_date = request.form.get('start_date')

        if habit:
            habit.name = name
            habit.description = description
            habit.frequency = frequency
            habit.start_date = datetime.strptime(start_date, '%Y-%m-%d')
            flash('Habit updated successfully!', category='success')
        else:
            new_habit = Habit(
                name=name,
                description=description,
                frequency=frequency,
                start_date=datetime.strptime(start_date, '%Y-%m-%d'),
                user_id=current_user.id
            )
            db.session.add(new_habit)
            flash('Habit created successfully!', category='success')
        
        db.session.commit()
        return redirect(url_for('views.home'))

    return render_template("edit_habit.html", user=current_user, habit=habit)

