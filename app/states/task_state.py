import reflex as rx
import logging
from typing import TypedDict
import uuid
from datetime import datetime, timedelta
import calendar


class Tache(TypedDict):
    id: str
    nom: str
    urgente: bool
    importante: bool
    deadline: str
    temps_estime_min: int
    score: int
    completed: bool
    created_at: str


class TaskState(rx.State):
    taches: list[Tache] = []
    new_task_name: str = ""
    is_urgent: bool = False
    is_important: bool = False
    new_task_deadline: str = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    estimated_time: str = "30"
    sort_by: str = "score"
    active_filter: str = "all"
    show_rules: bool = False
    current_month: int = datetime.now().month
    current_year: int = datetime.now().year

    @rx.var
    def current_month_date_str(self) -> str:
        return f"{self.current_year:04d}-{self.current_month:02d}-01"

    @rx.var
    def calendar_days(self) -> list[dict[str, int | bool | str | list[Tache]]]:
        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)
        days = []
        for week in month_calendar:
            for day in week:
                if day == 0:
                    days.append({"day": "", "is_current_month": False, "tasks": []})
                else:
                    date_str = (
                        f"{self.current_year:04d}-{self.current_month:02d}-{day:02d}"
                    )
                    days.append(
                        {
                            "day": day,
                            "is_current_month": True,
                            "is_today": date_str == datetime.now().strftime("%Y-%m-%d"),
                            "date_str": date_str,
                            "tasks": self.tasks_by_date.get(date_str, []),
                        }
                    )
        return days

    @rx.var
    def tasks_by_date(self) -> dict[str, list[Tache]]:
        tasks_dict = {}
        for task in self.taches:
            if not task["completed"]:
                deadline = task["deadline"]
                if deadline not in tasks_dict:
                    tasks_dict[deadline] = []
                tasks_dict[deadline].append(task)
        return tasks_dict

    def _get_days_remaining(self, deadline_str: str) -> int:
        if not deadline_str:
            return 999
        deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d")
        return (deadline_date - datetime.now()).days

    def _calculate_score(self, tache: Tache) -> int:
        score = 0
        days_remaining = self._get_days_remaining(tache["deadline"])
        if tache["urgente"] and tache["importante"]:
            score += 1000
        if tache["importante"] and (not tache["urgente"]):
            score += 500
        if tache["urgente"] and (not tache["importante"]):
            score += 250
        if days_remaining <= 1:
            score += 200
        elif days_remaining <= 3:
            score += 100
        elif days_remaining <= 7:
            score += 50
        if tache["temps_estime_min"] <= 15:
            score += 40
        elif tache["temps_estime_min"] <= 30:
            score += 20
        if tache["temps_estime_min"] > 120:
            score -= 30
        if tache["importante"] and (not tache["urgente"]):
            score += 60
        if tache["urgente"] and (not tache["importante"]):
            score += 30
        if not tache["urgente"] and (not tache["importante"]):
            score -= 50
        if days_remaining <= 2 and tache["temps_estime_min"] > 60:
            score += 80
        if days_remaining > 30:
            score -= 100
        return score

    @rx.var
    def filtered_taches(self) -> list[Tache]:
        if not self.taches:
            return []
        active_tasks = [t for t in self.taches if not t["completed"]]
        if self.active_filter == "urgent":
            active_tasks = [t for t in active_tasks if t["urgente"]]
        elif self.active_filter == "important":
            active_tasks = [t for t in active_tasks if t["importante"]]
        elif self.active_filter == "quick":
            active_tasks = [t for t in active_tasks if t["temps_estime_min"] <= 15]
        return active_tasks

    @rx.var
    def sorted_taches(self) -> list[Tache]:
        taches_to_sort = self.filtered_taches
        if self.sort_by == "score":
            return sorted(taches_to_sort, key=lambda t: t["score"], reverse=True)
        elif self.sort_by == "name":
            return sorted(taches_to_sort, key=lambda t: t["nom"].lower())
        elif self.sort_by == "deadline":
            return sorted(taches_to_sort, key=lambda t: t["deadline"])
        return taches_to_sort

    @rx.var
    def completed_taches(self) -> list[Tache]:
        return sorted(
            [t for t in self.taches if t["completed"]],
            key=lambda t: t["created_at"],
            reverse=True,
        )

    @rx.var
    def urgent_tasks_count(self) -> int:
        return len([t for t in self.taches if t["urgente"] and (not t["completed"])])

    @rx.var
    def important_tasks_count(self) -> int:
        return len([t for t in self.taches if t["importante"] and (not t["completed"])])

    @rx.var
    def quick_tasks_count(self) -> int:
        return len(
            [
                t
                for t in self.taches
                if t["temps_estime_min"] <= 15 and (not t["completed"])
            ]
        )

    @rx.event
    def add_task(self):
        if not self.new_task_name.strip():
            return rx.toast.error("Task name cannot be empty.")
        try:
            temps = int(self.estimated_time)
            datetime.strptime(self.new_task_deadline, "%Y-%m-%d")
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return rx.toast.error(
                "Please enter valid numbers for time and a valid date."
            )
        new_tache: Tache = {
            "id": str(uuid.uuid4()),
            "nom": self.new_task_name.strip(),
            "urgente": self.is_urgent,
            "importante": self.is_important,
            "deadline": self.new_task_deadline,
            "temps_estime_min": temps,
            "score": 0,
            "completed": False,
            "created_at": datetime.now().isoformat(),
        }
        new_tache["score"] = self._calculate_score(new_tache)
        self.taches.append(new_tache)
        self.new_task_name = ""
        self.is_urgent = False
        self.is_important = False
        self.new_task_deadline = (datetime.now() + timedelta(days=7)).strftime(
            "%Y-%m-%d"
        )
        self.estimated_time = "30"

    @rx.event
    def delete_task(self, task_id: str):
        self.taches = [t for t in self.taches if t["id"] != task_id]

    @rx.event
    def toggle_complete(self, task_id: str):
        for i, tache in enumerate(self.taches):
            if tache["id"] == task_id:
                self.taches[i]["completed"] = not self.taches[i]["completed"]
                break

    @rx.event
    def set_sort_by(self, sort_key: str):
        self.sort_by = sort_key

    @rx.event
    def set_filter(self, filter_key: str):
        self.active_filter = filter_key

    @rx.event
    def toggle_rules(self):
        self.show_rules = not self.show_rules

    @rx.event
    def previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

    @rx.event
    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

    @rx.event
    def load_test_data(self):
        self.taches = []
        today = datetime.now()
        test_data = [
            {
                "nom": "Finish Q3 Report",
                "urgente": True,
                "importante": True,
                "deadline": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
                "temps_estime_min": 240,
            },
            {
                "nom": "Plan team offsite",
                "urgente": False,
                "importante": True,
                "deadline": (today + timedelta(days=30)).strftime("%Y-%m-%d"),
                "temps_estime_min": 180,
            },
            {
                "nom": "Book dentist appointment",
                "urgente": False,
                "importante": False,
                "deadline": (today + timedelta(days=14)).strftime("%Y-%m-%d"),
                "temps_estime_min": 10,
            },
            {
                "nom": "Reply to client email",
                "urgente": True,
                "importante": False,
                "deadline": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
                "temps_estime_min": 15,
            },
            {
                "nom": "Review design mockups",
                "urgente": False,
                "importante": True,
                "deadline": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
                "temps_estime_min": 60,
            },
            {
                "nom": "Organize digital files",
                "urgente": False,
                "importante": False,
                "deadline": (today + timedelta(days=60)).strftime("%Y-%m-%d"),
                "temps_estime_min": 90,
            },
            {
                "nom": "Pay electricity bill",
                "urgente": True,
                "importante": True,
                "deadline": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
                "temps_estime_min": 5,
            },
            {
                "nom": "Brainstorm new project ideas",
                "urgente": False,
                "importante": True,
                "deadline": (today + timedelta(days=45)).strftime("%Y-%m-%d"),
                "temps_estime_min": 75,
            },
        ]
        for item in test_data:
            new_tache: Tache = {
                "id": str(uuid.uuid4()),
                "nom": item["nom"],
                "urgente": item["urgente"],
                "importante": item["importante"],
                "deadline": item["deadline"],
                "temps_estime_min": item["temps_estime_min"],
                "score": 0,
                "completed": False,
                "created_at": datetime.now().isoformat(),
            }
            new_tache["score"] = self._calculate_score(new_tache)
            self.taches.append(new_tache)
        return rx.toast.info("Test data loaded!")