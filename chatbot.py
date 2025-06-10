import os
import json
from typing import Dict, List
import requests
from scheduler import Scheduler, Employee

class ChatBot:
    """Very simple stateful chatbot for gathering schedule info."""
    def __init__(self, scheduler: Scheduler, data_dir: str = "data"):
        self.scheduler = scheduler
        self.data_file = os.path.join(data_dir, "chat_state.json")
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "state": "ask_roles",
                "roles": {},
                "employees": [],
            }
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def handle_message(self, msg: str) -> str:
        state = self.data.get("state", "ask_roles")
        text = msg.strip()

        # allow user to ask arbitrary questions starting with 'search' or ending with '?'
        lower = text.lower()
        if lower.startswith('search '):
            query = text.split(' ', 1)[1]
            return self._search_web(query)
        if text.endswith('?') and state == 'done':
            return self._search_web(text)
        if state == "ask_roles":
            self.data["roles"] = self._parse_roles(msg)
            self.data["state"] = "ask_employees"
            self._save()
            return "Thanks. Now list employees as 'Name, MaxHours'. One per line."
        elif state == "ask_employees":
            for line in msg.splitlines():
                parts = [p.strip() for p in line.split(',')]
                if not parts or not parts[0]:
                    continue
                name = parts[0]
                max_hours = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 40
                emp = Employee(name=name, max_hours=max_hours)
                self.scheduler.add_employee(emp)
                self.data.setdefault("employees", []).append({"id": emp.id, "name": name, "max_hours": max_hours})
            self.data["state"] = "ask_availability"
            self._save()
            return "Great! Provide availability like 'Name: Mon morning, Tue evening'."
        elif state == "ask_availability":
            for line in msg.splitlines():
                if ':' not in line:
                    continue
                name, rest = line.split(':', 1)
                emp = self._find_employee(name.strip())
                if not emp:
                    continue
                tokens = [t.strip() for t in rest.split(',') if t.strip()]
                days = []
                shifts = []
                for t in tokens:
                    parts = t.split()
                    if not parts:
                        continue
                    days.append(parts[0])
                    if len(parts) > 1:
                        shifts.extend(parts[1:])
                self.scheduler.update_availability(emp.id, days, shifts)
            self.data["state"] = "ask_timeoff"
            self._save()
            return "Any time-off requests? Use 'Name: Fri'. If none, just reply 'none'."
        elif state == "ask_timeoff":
            if msg.strip().lower() != 'none':
                for line in msg.splitlines():
                    if ':' not in line:
                        continue
                    name, rest = line.split(':', 1)
                    emp = self._find_employee(name.strip())
                    if not emp:
                        continue
                    for day in rest.split():
                        self.scheduler.request_time_off(emp.id, day.strip())
            schedule = self.scheduler.generate_schedule()
            self.data["state"] = "done"
            self._save()
            return self._format_schedule(schedule)
        else:
            # after setup, treat questions ending with '?' as web searches
            if msg.strip().endswith('?'):
                return self._search_web(msg.strip())
            schedule = self.scheduler.generate_schedule()
            return self._format_schedule(schedule)

    def get_prompt(self) -> str:
        state = self.data.get("state", "ask_roles")
        prompts = {
            "ask_roles": "What roles are needed each day of the week? e.g. 'Mon: cook, manager'",
            "ask_employees": "List employees as 'Name, MaxHours'",
            "ask_availability": "Provide availability like 'Name: Mon morning, Tue evening'",
            "ask_timeoff": "Any time-off requests? Use 'Name: Fri' or reply 'none'",
            "done": "Ask me a question or type anything to regenerate the schedule",
        }
        return prompts.get(state, "")

    def _parse_roles(self, msg: str) -> Dict[str, List[str]]:
        roles = {}
        for line in msg.splitlines():
            if ':' not in line:
                continue
            day, rest = line.split(':', 1)
            roles[day.strip()] = [r.strip() for r in rest.split(',') if r.strip()]
        return roles

    def _find_employee(self, name: str):
        for emp in self.scheduler.employees:
            if emp.name.lower() == name.lower():
                return emp
        return None

    def _format_schedule(self, schedule: Dict[str, Dict[str, str]]) -> str:
        lines = []
        for day, shifts in schedule.items():
            parts = [f"{sh}:{shifts[sh] or '-'}" for sh in ['morning','evening','night']]
            lines.append(f"{day}: " + ', '.join(parts))
        return "\n".join(lines)

    def _search_web(self, query: str) -> str:
        """Use DuckDuckGo Instant Answer API for simple web search."""
        try:
            resp = requests.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "t": "auto-scheduler"},
                timeout=5,
            )
            data = resp.json()
            if data.get("AbstractText"):
                return data["AbstractText"]
            elif data.get("RelatedTopics"):
                # grab text from first related topic
                for topic in data["RelatedTopics"]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        return topic["Text"]
            return "No results found."
        except Exception:
            return "Sorry, I couldn't search the web right now."