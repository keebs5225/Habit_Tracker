from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


from sqlalchemy.sql import func

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)  # Name of the habit
    description = db.Column(db.String(1000), nullable=True)  # Description of the habit
    frequency = db.Column(db.String(50), nullable=False)  # Daily, Weekly, etc.
    status = db.Column(db.Boolean, default=False)  # Track if the habit is completed for the day/week
    start_date = db.Column(db.DateTime(timezone=True), default=func.now())  # When the habit was started
    last_completed = db.Column(db.DateTime(timezone=True))  # When the habit was last marked as completed
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Reference to the user who owns this habit

    def __repr__(self):
        return f"<Habit {self.name}>"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    habits = db.relationship('Habit')