import reflex as rx
from app.states.task_state import TaskState, Tache


def completed_task_item(tache: Tache) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("square_check", class_name="h-5 w-5 text-emerald-600"),
            rx.el.span(tache["nom"], class_name="text-gray-500 line-through"),
            class_name="flex items-center gap-3",
        ),
        rx.el.button(
            rx.icon("undo-2", class_name="h-4 w-4"),
            on_click=lambda: TaskState.toggle_complete(tache["id"]),
            class_name="text-gray-400 hover:text-blue-600",
            background="transparent",
            border="none",
            cursor="pointer",
            title="Mark as incomplete",
        ),
        class_name="flex items-center justify-between p-3 bg-gray-50 border border-gray-200/80 rounded-lg",
    )


def completed_tasks_list() -> rx.Component:
    return rx.cond(
        TaskState.completed_taches.length() > 0,
        rx.el.div(
            rx.el.h2(
                "Completed Tasks",
                class_name="text-lg font-semibold text-gray-800 pb-2 border-b",
            ),
            rx.el.div(
                rx.foreach(TaskState.completed_taches, completed_task_item),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mt-4",
            ),
            class_name="w-full",
        ),
        rx.fragment(),
    )