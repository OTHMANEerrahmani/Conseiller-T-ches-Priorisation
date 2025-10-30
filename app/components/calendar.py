import reflex as rx
from app.states.task_state import TaskState, Tache
from datetime import datetime


def calendar_task_item(tache: Tache) -> rx.Component:
    color = rx.cond(
        tache["score"] > 1000,
        "bg-red-500",
        rx.cond(
            tache["score"] > 500,
            "bg-orange-500",
            rx.cond(tache["score"] > 250, "bg-yellow-500", "bg-emerald-500"),
        ),
    )
    return rx.el.div(
        rx.el.div(class_name=f"h-2 w-2 rounded-full {color}"),
        rx.el.p(tache["nom"], class_name="text-xs truncate"),
        on_click=lambda: TaskState.toggle_complete(tache["id"]),
        class_name="flex items-center gap-1.5 p-1 rounded-md hover:bg-gray-200 cursor-pointer",
        title=tache["nom"],
    )


def calendar_day(day: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                day["day"].to_string(),
                class_name=rx.cond(
                    day["is_today"],
                    "flex items-center justify-center h-6 w-6 rounded-full bg-emerald-600 text-white font-bold",
                    "text-sm",
                ),
            ),
            class_name="flex justify-end",
        ),
        rx.el.div(
            rx.foreach(day["tasks"].to(list[Tache]), calendar_task_item),
            class_name="flex flex-col gap-1 mt-1 overflow-y-auto max-h-20",
        ),
        class_name=rx.cond(
            day["is_current_month"],
            "p-2 h-36 border border-gray-200 bg-white rounded-lg",
            "p-2 h-36 border border-gray-100 bg-gray-50",
        ),
    )


def calendar_view() -> rx.Component:
    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Task Calendar", class_name="text-lg font-semibold text-gray-800"),
            rx.el.div(
                rx.el.button(
                    rx.icon("chevron-left"),
                    on_click=TaskState.previous_month,
                    class_name="p-1 text-gray-600 hover:bg-gray-100 rounded-md",
                ),
                rx.el.p(
                    rx.moment(TaskState.current_month_date_str, format="MMMM YYYY"),
                    class_name="text-center font-semibold w-32",
                ),
                rx.el.button(
                    rx.icon("chevron-right"),
                    on_click=TaskState.next_month,
                    class_name="p-1 text-gray-600 hover:bg-gray-100 rounded-md",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between pb-2 border-b",
        ),
        rx.el.div(
            rx.foreach(
                week_days,
                lambda d: rx.el.div(
                    d, class_name="text-center text-sm font-medium text-gray-500"
                ),
            ),
            class_name="grid grid-cols-7 gap-2 mt-4",
        ),
        rx.el.div(
            rx.foreach(TaskState.calendar_days, calendar_day),
            class_name="grid grid-cols-7 gap-2 mt-2",
        ),
        class_name="p-4 bg-white border border-gray-200 rounded-xl shadow-sm",
    )