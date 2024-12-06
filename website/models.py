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
    times_completed = db.Column(db.Integer, default=0)  
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

