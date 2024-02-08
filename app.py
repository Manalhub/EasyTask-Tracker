# app.py - Main Flask application file

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def initialize_database():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                 id INTEGER PRIMARY KEY,
                 description TEXT NOT NULL,
                 deadline DATE,
                 status TEXT DEFAULT 'Pending'
                 )''')
    conn.commit()
    conn.close()

# Route for displaying tasks
@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route for adding a new task
@app.route('/add', methods=['POST'])
def add_task():
    description = request.form['description']
    deadline = request.form['deadline']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (description, deadline) VALUES (?, ?)", (description, deadline))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route for updating a task
@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    status = request.form['status']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route for deleting a task
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
