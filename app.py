from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('index.html', tasks=tasks, completed_tasks=completed_tasks, today=datetime.now().strftime("%Y-%m-%d"))

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task_content = request.form['task_content']
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'

@app.route('/complete_task/<int:task_id>', methods=['GET', 'POST'])
def complete_task(task_id):
    task_to_complete = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task_to_complete.completed = True

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue completing the task.'

    return render_template('index.html')  # Add the template name here

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task_to_delete = Task.query.get_or_404(task_id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the task.'

if __name__ == '__main__':
    app.run(debug=True)
