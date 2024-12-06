Habit Tracker
Habit Tracker is a web application designed to help users track and manage their daily, weekly, and monthly habits. The application provides features such as adding habits, setting frequencies, toggling habit statuses, and sorting habits for better organization.

Features
Add Habits: Create new habits with custom names, descriptions, frequencies, and start dates.
Toggle Status: Mark habits as "Done" or "Todo" with a single click.
Deadline Tracking: Automatically calculate deadlines for habits based on their frequency.
Sort Habits: Organize habits by name, status, or deadline.
Responsive Design: The interface is user-friendly and accessible on all devices.


Technologies Used
Backend: Flask (Python)
Frontend: HTML, CSS (Bootstrap), JavaScript
Database: SQLite
Other Tools: SQLAlchemy for ORM, Flask-Login for authentication


Setup Instructions
Prerequisites
Python 3.9 or higher
Virtual environment manager (optional but recommended)
SQLite (pre-installed with Python)
Steps to Run Locally

Clone the Repository:

git clone <https://github.com/keebs5225/Habit_Tracker>
cd habit-tracker


Create a Virtual Environment:

python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows


Install Dependencies:

pip install -r requirements.txt
Set Up the Database:

flask db init
flask db migrate
flask db upgrade

Run the Application:

flask run

Open your browser and navigate to http://127.0.0.1:5000.

Folder Structure

habit-tracker/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── home.html
│   └── add_habit.html
├── app.py
├── models.py
├── views.py
├── forms.py
├── requirements.txt
└── README.md


Key Routes

/: Home page displaying the habit list.
/add-habit: Add a new habit.
/update-habit-status/<habit_id>: Update the status of a habit.
/delete-habitlist/<habit_id>: Delete a habit from the list.


Future Enhancements

Add custom categories for habits.
Include progress visualizations.
Provide detailed analytics for habit tracking.
Enable account settings and profile management.


Contributing please follow these steps:

Fork the repository.
Create a new feature branch.
Commit changes and push to your fork.
Submit a pull request.


License

This project is licensed under the MIT License. See the LICENSE file for more details.