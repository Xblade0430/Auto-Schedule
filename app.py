 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a//dev/null b/app.py
index 0000000000000000000000000000000000000000..90e9df1acc9674eb93fc5559caa8c3b3d46bd3da 100644
--- a//dev/null
+++ b/app.py
@@ -0,0 +1,35 @@
+from flask import Flask, render_template, request, redirect, url_for
+from scheduler import Scheduler, Employee
+
+app = Flask(__name__)
+
+# In-memory store
+scheduler = Scheduler()
+
+@app.route('/')
+def index():
+    schedule = scheduler.generate_schedule()
+    return render_template('index.html', schedule=schedule, employees=scheduler.employees)
+
+@app.route('/employees', methods=['POST'])
+def add_employee():
+    name = request.form['name']
+    max_hours = int(request.form.get('max_hours', 40))
+    scheduler.add_employee(Employee(name=name, max_hours=max_hours))
+    return redirect(url_for('index'))
+
+@app.route('/availability/<int:emp_id>', methods=['POST'])
+def update_availability(emp_id):
+    days = request.form.getlist('days')
+    shifts = request.form.getlist('shifts')
+    scheduler.update_availability(emp_id, days, shifts)
+    return redirect(url_for('index'))
+
+@app.route('/timeoff/<int:emp_id>', methods=['POST'])
+def request_timeoff(emp_id):
+    day = request.form['day']
+    scheduler.request_time_off(emp_id, day)
+    return redirect(url_for('index'))
+
+if __name__ == '__main__':
+    app.run(debug=True)
 
EOF
)