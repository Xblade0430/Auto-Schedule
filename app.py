import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from scheduler import Scheduler, Employee
from chatbot import ChatBot

app = Flask(__name__)

# Persistent scheduler using data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
scheduler = Scheduler(data_dir=DATA_DIR)
chatbot = ChatBot(scheduler, data_dir=DATA_DIR)

@app.route('/')
def index():
    method = request.args.get('method', 'ai')
    randomize = method == 'random'
    schedule = scheduler.generate_schedule(randomize=randomize)
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
        from werkzeug.utils import secure_filename
        fname = secure_filename(file.filename)
        path = os.path.join(scheduler.import_dir, fname)
        # avoid overwriting existing files
        base, ext = os.path.splitext(path)
        i = 1
        while os.path.exists(path):
            path = f"{base}_{i}{ext}"
            i += 1
        file.save(path)
        scheduler.import_file(path)
    return redirect(url_for('index'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json(force=True)
        message = data.get('message', '')
        reply = chatbot.handle_message(message)
        return jsonify({'reply': reply, 'prompt': chatbot.get_prompt()})
    # initial load
    prompt = chatbot.get_prompt()
    return render_template('chat.html', prompt=prompt)

if __name__ == '__main__':
    app.run(debug=True)