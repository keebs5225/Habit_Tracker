from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Habit, Habitlist
from . import db
from datetime import datetime, timedelta
from sqlalchemy.sql import func

# Blueprint for organizing the views
views = Blueprint('views', __name__)

# Home route to display all habits for the logged-in user
@views.route('/')
@login_required
def home():
    # Fetch all habits for the current user
    habitlist = Habitlist.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, habitlist=habitlist)

# Route to add a new habit
@views.route('/add-habit', methods=['POST'])
@login_required
def add_habit():
    # Collect form data
    name = request.form.get('name')
    frequency = request.form.get('frequency')
    description = request.form.get('description')  # Optional description field

    # Ensure required fields are filled
    if not name or not frequency:
        flash('Please fill in all fields', 'error')
    else:
        # Create a new Habit entry
        new_habit = Habit(
            name=name,
            frequency=frequency,
            description=description,
            start_date=func.now(),  # Set start date to the current time
            times_completed=0,      # Initialize times completed to 0
            last_completed=None    # Initialize last completed as None
        )
        db.session.add(new_habit)
        db.session.commit()

        # Link the new habit to the current user in the Habitlist
        new_habitlist = Habitlist(user_id=current_user.id, habit_id=new_habit.id, status=False)
        db.session.add(new_habitlist)
        db.session.commit()

        flash('Habit added to your tracker!', 'success')

    return redirect(url_for('views.home'))

# Route to update the status of a habit
@views.route('/update-habit-status/<int:habit_id>', methods=['POST'])
@login_required
def update_habit_status(habit_id):
    # Get the new status from the client request
    data = request.get_json()
    new_status = data.get('status')

    # Find the habit in the Habitlist
    habitlist_item = Habitlist.query.filter_by(habit_id=habit_id, user_id=current_user.id).first()

    if habitlist_item:
        # Update the status based on the received data
        habitlist_item.status = True if new_status == 'Done' else False
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Habit not found."})

# Route to delete a habit from the user's habit list
@views.route('/delete-habitlist/<int:id>', methods=['POST'])
@login_required
def delete_habitlist(id):
    # Find and delete the habitlist item
    habitlist_item = Habitlist.query.get_or_404(id)
    db.session.delete(habitlist_item)
    db.session.commit()
    return redirect(url_for('views.home'))

# Route to display the user's profile
@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

# Route to edit an existing habit
@views.route('/edit-habit/<int:habit_id>', methods=['GET', 'POST'])
@login_required
def edit_habit(habit_id):
    # Fetch the habit to be edited
    habit = Habit.query.get(habit_id)

    if request.method == 'POST' and habit:
        # Collect updated form data
        name = request.form.get('name')
        description = request.form.get('description')
        frequency = request.form.get('frequency')
        start_date = request.form.get('start_date')

        # Update habit details
        habit.name = name
        habit.description = description
        habit.frequency = frequency
        db.session.commit()
        flash('Habit updated successfully!', category='success')

        return redirect(url_for('views.home'))

    return render_template("edit_habit.html", user=current_user, habit=habit)

@views.route('/update-habit-counter/<int:habit_id>', methods=['POST'])
@login_required
def update_habit_counter(habit_id):
    # Fetch the habit associated with the counter
    habit = Habit.query.get(habit_id)
    if habit:
        habit.times_completed += 1  # Increment the counter
        db.session.commit()
        return jsonify({"success": True, "counter": habit.times_completed})
    return jsonify({"success": False, "message": "Habit not found"})
