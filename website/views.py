from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Habit
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        habit = request.form.get('habit')#Gets the habit from the HTML 

        if len(habit) < 1:
            flash('Habit name is too short!', category='error') 
        else:
            new_habit = Habit(data=habit, user_id=current_user.id)  #providing the schema for the habit 
            db.session.add(new_habit) #adding the habit to the database 
            db.session.commit()
            flash('Habit added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-habit', methods=['POST'])
def delete_habit():  
    habit = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    habitId = habit['habitId']
    habit = Habit.query.get(habitId)
    if habit:
        if habit.user_id == current_user.id:
            db.session.delete(habit)
            db.session.commit()

    return jsonify({})