 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a//dev/null b/scheduler.py
index 0000000000000000000000000000000000000000..643ee5a4c87097e1a64141ada27ff7e8de5df2a2 100644
--- a//dev/null
+++ b/scheduler.py
@@ -0,0 +1,59 @@
+from collections import defaultdict
+from dataclasses import dataclass, field
+from typing import Dict, List, Set
+
+DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
+SHIFTS = ['morning', 'evening', 'night']
+SHIFT_HOURS = 8
+
+@dataclass
+class Employee:
+    name: str
+    max_hours: int = 40
+    availability: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))
+    time_off: Set[str] = field(default_factory=set)
+    id: int = field(default=0)
+    assigned_hours: int = 0
+
+class Scheduler:
+    def __init__(self):
+        self.employees: List[Employee] = []
+        self.next_id = 1
+
+    def add_employee(self, employee: Employee):
+        employee.id = self.next_id
+        self.next_id += 1
+        self.employees.append(employee)
+
+    def update_availability(self, emp_id: int, days: List[str], shifts: List[str]):
+        emp = self.get_employee(emp_id)
+        for d in days:
+            emp.availability[d].update(shifts)
+
+    def request_time_off(self, emp_id: int, day: str):
+        emp = self.get_employee(emp_id)
+        emp.time_off.add(day)
+
+    def get_employee(self, emp_id: int) -> Employee:
+        for emp in self.employees:
+            if emp.id == emp_id:
+                return emp
+        raise ValueError('Employee not found')
+
+    def reset_hours(self):
+        for emp in self.employees:
+            emp.assigned_hours = 0
+
+    def generate_schedule(self):
+        self.reset_hours()
+        schedule = {d: {s: None for s in SHIFTS} for d in DAYS}
+        for day in DAYS:
+            for shift in SHIFTS:
+                for emp in sorted(self.employees, key=lambda e: e.assigned_hours):
+                    if (shift in emp.availability.get(day, set()) and
+                        day not in emp.time_off and
+                        emp.assigned_hours + SHIFT_HOURS <= emp.max_hours):
+                        schedule[day][shift] = emp.name
+                        emp.assigned_hours += SHIFT_HOURS
+                        break
+        return schedule
 
EOF
)