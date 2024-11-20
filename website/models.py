from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    habitlist = db.relationship('Habitlist', backref='user', lazy=True)

# Habit Model (Updated: No status field)
class Habit(db.Model):
    __tablename__ = 'habits'  # define the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    frequency = db.Column(db.String(50), nullable=False)  # e.g., Daily, Weekly, Monthly
    start_date = db.Column(db.DateTime(timezone=True), default=func.now())
    times_completed = db.Column(db.Integer, default=0)  # Total count of completions
    last_completed = db.Column(db.DateTime(timezone=True))  # Timestamp of the last completion

    # Relationships
    habitlist = db.relationship('Habitlist', backref='habit', lazy=True)

# Habitlist Model (Track habit completion status for each user)
class Habitlist(db.Model):
    __tablename__ = 'habitlist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)  # Boolean field

    # The relationships are implicitly inferred from ForeignKey.
    # The 'user' relationship will allow access to the associated User.
    # The 'habit' relationship will allow access to the associated Habit.
    

# Goal Model (optional, for setting target goals per habit)
# class Goal(db.Model):
#     __tablename__ = 'goals'
#     id = db.Column(db.Integer, primary_key=True)
#     habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
#     target_count = db.Column(db.Integer, nullable=False)  # Target completion count
#     timeframe = db.Column(db.String(50), nullable=False)  # Timeframe, e.g., Daily, Weekly
#     status = db.Column(db.Boolean, default=False)  # Goal achievement status

# Reminder Model (optional, for setting reminders)
# class Reminder(db.Model):
#     __tablename__ = 'reminders'
#     id = db.Column(db.Integer, primary_key=True)
#     habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
#     reminder_time = db.Column(db.Time, nullable=False)  # Time for reminder
#     frequency = db.Column(db.String(50), nullable=False)  # e.g., Daily, Weekly
#     active = db.Column(db.Boolean, default=True)  # Is the reminder active?

# Example Relationships:
# - Each `User` can have multiple `Habits`.
# - Each `Habit` can have multiple `HabitLogs` (for tracking completions),
#   multiple `Goals` (for targets), and multiple `Reminders` (for notifications).
