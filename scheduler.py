from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set

try:
    from ortools.sat.python import cp_model
except ImportError:  # pragma: no cover - module may not be installed
    cp_model = None

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
SHIFTS = ['morning', 'evening', 'night']
SHIFT_HOURS = 8

@dataclass
class Employee:
    name: str
    max_hours: int = 40
    availability: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))
    time_off: Set[str] = field(default_factory=set)
    id: int = field(default=0)
    assigned_hours: int = 0

class Scheduler:
    def __init__(self):
        self.employees: List[Employee] = []
        self.next_id = 1

    def add_employee(self, employee: Employee):
        employee.id = self.next_id
        self.next_id += 1
        self.employees.append(employee)

    def update_availability(self, emp_id: int, days: List[str], shifts: List[str]):
        emp = self.get_employee(emp_id)
        for d in days:
            emp.availability[d].update(shifts)

    def request_time_off(self, emp_id: int, day: str):
        emp = self.get_employee(emp_id)
        emp.time_off.add(day)

    def get_employee(self, emp_id: int) -> Employee:
        for emp in self.employees:
            if emp.id == emp_id:
                return emp
        raise ValueError('Employee not found')

    def reset_hours(self):
        for emp in self.employees:
            emp.assigned_hours = 0

    def _heuristic_schedule(self, schedule: Dict[str, Dict[str, str]]):
        """Fallback simple scheduler if OR-Tools is unavailable."""
        for day in DAYS:
            for shift in SHIFTS:
                if schedule[day][shift] is not None:
                    continue
                for emp in sorted(self.employees, key=lambda e: e.assigned_hours):
                    if (shift in emp.availability.get(day, set()) and
                        day not in emp.time_off and
                        emp.assigned_hours + SHIFT_HOURS <= emp.max_hours):
                        schedule[day][shift] = emp.name
                        emp.assigned_hours += SHIFT_HOURS
                        break
        return schedule

    def generate_schedule(self):
        self.reset_hours()
        schedule = {d: {s: None for s in SHIFTS} for d in DAYS}

        if cp_model is None or not self.employees:
            return self._heuristic_schedule(schedule)

        # Build CP-SAT model for balanced scheduling
        model = cp_model.CpModel()
        assign = {}
        for emp in self.employees:
            for day in DAYS:
                if day in emp.time_off:
                    continue
                for shift in SHIFTS:
                    if shift in emp.availability.get(day, set()):
                        assign[(emp.id, day, shift)] = model.NewBoolVar(f"a_{emp.id}_{day}_{shift}")

        if not assign:
            return schedule

        # At most one employee per shift
        for day in DAYS:
            for shift in SHIFTS:
                vars_for_shift = [assign[(e.id, day, shift)]
                                  for e in self.employees
                                  if (e.id, day, shift) in assign]
                if vars_for_shift:
                    model.Add(sum(vars_for_shift) == 1)

        # Employee hour limits and fairness variable
        max_possible = SHIFT_HOURS * len(DAYS) * len(SHIFTS)
        max_hours_var = model.NewIntVar(0, max_possible, 'max_hours')
        for emp in self.employees:
            vars_for_emp = [assign[(emp.id, d, s)]
                            for d in DAYS for s in SHIFTS
                            if (emp.id, d, s) in assign]
            if vars_for_emp:
                hours = sum(vars_for_emp) * SHIFT_HOURS
                model.Add(hours <= emp.max_hours)
                model.Add(hours <= max_hours_var)
            else:
                model.Add(max_hours_var >= 0)

        # Objective: maximize coverage then minimize imbalance
        model.Maximize(sum(assign.values()) * 100 - max_hours_var)

        solver = cp_model.CpSolver()
        solver.Solve(model)

        for (eid, day, shift), var in assign.items():
            if solver.Value(var):
                emp = self.get_employee(eid)
                schedule[day][shift] = emp.name
                emp.assigned_hours += SHIFT_HOURS

        # Fill remaining shifts heuristically if any
        return self._heuristic_schedule(schedule)