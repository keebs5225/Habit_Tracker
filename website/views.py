from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Habit, Goal
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, habits=habits)

@views.route('/edit-habit/<int:habit_id>', methods=['GET', 'POST'])
@login_required
def edit_habit(habit_id=None):
    habit = Habit.query.get(habit_id) if habit_id else None

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

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/goals')
@login_required
def goals():
    goals = Goal.query.filter(Goal.habit.has(user_id=current_user.id)).all()
    return render_template("goals.html", user=current_user, goals=goals)
