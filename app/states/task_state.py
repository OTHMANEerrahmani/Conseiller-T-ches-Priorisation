import reflex as rx
import logging
from typing import TypedDict
import uuid
from datetime import datetime, timedelta


class Tache(TypedDict):
    id: str
    nom: str
    urgente: bool
    importante: bool
    delai_jours: int
    temps_estime_min: int
    score: int
    completed: bool
    created_at: str


class TaskState(rx.State):
    taches: list[Tache] = []
    new_task_name: str = ""
    is_urgent: bool = False
    is_important: bool = False
    deadline_days: str = "7"
    estimated_time: str = "30"
    sort_by: str = "score"
    active_filter: str = "all"
    show_rules: bool = False

    def _calculate_score(self, tache: Tache) -> int:
        score = 0
        if tache["urgente"] and tache["importante"]:
            score += 1000
        if tache["importante"] and (not tache["urgente"]):
            score += 500
        if tache["urgente"] and (not tache["importante"]):
            score += 250
        if tache["delai_jours"] <= 1:
            score += 200
        elif tache["delai_jours"] <= 3:
            score += 100
        elif tache["delai_jours"] <= 7:
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
        if tache["delai_jours"] <= 2 and tache["temps_estime_min"] > 60:
            score += 80
        if tache["delai_jours"] > 30:
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
            return sorted(taches_to_sort, key=lambda t: t["delai_jours"])
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
            delai = int(self.deadline_days)
            temps = int(self.estimated_time)
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return rx.toast.error("Please enter valid numbers for deadline and time.")
        new_tache: Tache = {
            "id": str(uuid.uuid4()),
            "nom": self.new_task_name.strip(),
            "urgente": self.is_urgent,
            "importante": self.is_important,
            "delai_jours": delai,
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
        self.deadline_days = "7"
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
    def load_test_data(self):
        self.taches = []
        test_data = [
            {
                "nom": "Finish Q3 Report",
                "urgente": True,
                "importante": True,
                "delai_jours": 2,
                "temps_estime_min": 240,
            },
            {
                "nom": "Plan team offsite",
                "urgente": False,
                "importante": True,
                "delai_jours": 30,
                "temps_estime_min": 180,
            },
            {
                "nom": "Book dentist appointment",
                "urgente": False,
                "importante": False,
                "delai_jours": 14,
                "temps_estime_min": 10,
            },
            {
                "nom": "Reply to client email",
                "urgente": True,
                "importante": False,
                "delai_jours": 1,
                "temps_estime_min": 15,
            },
            {
                "nom": "Review design mockups",
                "urgente": False,
                "importante": True,
                "delai_jours": 7,
                "temps_estime_min": 60,
            },
            {
                "nom": "Organize digital files",
                "urgente": False,
                "importante": False,
                "delai_jours": 60,
                "temps_estime_min": 90,
            },
            {
                "nom": "Pay electricity bill",
                "urgente": True,
                "importante": True,
                "delai_jours": 1,
                "temps_estime_min": 5,
            },
            {
                "nom": "Brainstorm new project ideas",
                "urgente": False,
                "importante": True,
                "delai_jours": 45,
                "temps_estime_min": 75,
            },
        ]
        for item in test_data:
            new_tache: Tache = {
                "id": str(uuid.uuid4()),
                "nom": item["nom"],
                "urgente": item["urgente"],
                "importante": item["importante"],
                "delai_jours": item["delai_jours"],
                "temps_estime_min": item["temps_estime_min"],
                "score": 0,
                "completed": False,
                "created_at": datetime.now().isoformat(),
            }
            new_tache["score"] = self._calculate_score(new_tache)
            self.taches.append(new_tache)
        return rx.toast.info("Test data loaded!")