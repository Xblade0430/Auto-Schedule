from flask import Flask, render_template, request, redirect, url_for
from scheduler import Scheduler, Employee

app = Flask(__name__)

# In-memory store
scheduler = Scheduler()

@app.route('/')
def index():
    schedule = scheduler.generate_schedule()
    return render_template('index.html', schedule=schedule, employees=scheduler.employees)

@app.route('/employees', methods=['POST'])
def add_employee():
    name = request.form['name']
    max_hours = int(request.form.get('max_hours', 40))
    scheduler.add_employee(Employee(name=name, max_hours=max_hours))
    return redirect(url_for('index'))

@app.route('/availability/<int:emp_id>', methods=['POST'])
def update_availability(emp_id):
    days = request.form.getlist('days')
    shifts = request.form.getlist('shifts')
    scheduler.update_availability(emp_id, days, shifts)
    return redirect(url_for('index'))

@app.route('/timeoff/<int:emp_id>', methods=['POST'])
def request_timeoff(emp_id):
    day = request.form['day']
    scheduler.request_time_off(emp_id, day)
    return redirect(url_for('index'))

@app.route('/import', methods=['POST'])
def import_file():
    file = request.files.get('file')
    if file and file.filename:
        import os, tempfile
        from werkzeug.utils import secure_filename
        path = os.path.join(tempfile.gettempdir(), secure_filename(file.filename))
        file.save(path)
        scheduler.import_file(path)
        os.remove(path)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)