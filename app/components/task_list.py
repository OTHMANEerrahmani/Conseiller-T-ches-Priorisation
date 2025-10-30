import reflex as rx
from app.states.task_state import TaskState, Tache


def badge(text: str, color_class: str) -> rx.Component:
    return rx.el.span(
        text, class_name=f"px-2 py-0.5 text-xs font-semibold rounded-full {color_class}"
    )


def task_item(tache: Tache) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon(
                    rx.cond(tache["completed"], "check-circle-2", "circle"),
                    class_name="h-5 w-5",
                ),
                on_click=lambda: TaskState.toggle_complete(tache["id"]),
                class_name=rx.cond(
                    tache["completed"],
                    "text-gray-400 hover:text-gray-500",
                    "text-gray-600 hover:text-emerald-600",
                ),
                background="transparent",
                border="none",
                cursor="pointer",
            ),
            rx.el.span(
                tache["nom"],
                class_name=rx.cond(
                    tache["completed"],
                    "line-through text-gray-500",
                    "text-gray-800 font-medium",
                ),
            ),
            class_name="flex items-center gap-3",
        ),
        rx.el.div(
            rx.el.div(
                badge(f"{tache['delai_jours']}d", "bg-blue-100 text-blue-800"),
                badge(f"{tache['temps_estime_min']}m", "bg-purple-100 text-purple-800"),
                rx.cond(
                    tache["urgente"],
                    badge("Urgent", "bg-yellow-100 text-yellow-800"),
                    rx.fragment(),
                ),
                rx.cond(
                    tache["importante"],
                    badge("Important", "bg-red-100 text-red-800"),
                    rx.fragment(),
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                f"Score: {tache['score']}",
                class_name="text-sm font-bold text-emerald-700 w-24 text-right",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: TaskState.delete_task(tache["id"]),
                class_name="text-gray-400 hover:text-red-600",
                background="transparent",
                border="none",
                cursor="pointer",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:border-emerald-400 transition-colors",
    )


def filter_button(label: str, filter_key: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: TaskState.set_filter(filter_key),
        class_name=rx.cond(
            TaskState.active_filter == filter_key,
            "px-3 py-1 text-sm font-medium text-white bg-emerald-600 rounded-full shadow-sm",
            "px-3 py-1 text-sm font-medium text-gray-600 bg-gray-100 rounded-full hover:bg-gray-200",
        ),
        transition="all 0.2s",
    )


def task_list() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Recommended Tasks", class_name="text-lg font-semibold text-gray-800"
            ),
            rx.el.div(
                rx.el.p("Sort by:", class_name="text-sm text-gray-600"),
                rx.el.select(
                    rx.el.option("Priority Score", value="score"),
                    rx.el.option("Task Name", value="name"),
                    rx.el.option("Deadline", value="deadline"),
                    on_change=TaskState.set_sort_by,
                    value=TaskState.sort_by,
                    class_name="text-sm rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between pb-2 border-b",
        ),
        rx.el.div(
            filter_button("All", "all"),
            filter_button("Urgent", "urgent"),
            filter_button("Important", "important"),
            filter_button("Quick", "quick"),
            class_name="flex items-center gap-2 mt-4",
        ),
        rx.cond(
            TaskState.sorted_taches.length() > 0,
            rx.el.div(
                rx.foreach(TaskState.sorted_taches, task_item),
                class_name="flex flex-col gap-3 mt-4",
            ),
            rx.el.div(
                rx.icon("inbox", class_name="h-12 w-12 text-gray-300 mx-auto"),
                rx.el.p(
                    "No active tasks match your filters.",
                    class_name="text-center text-gray-500 mt-4",
                ),
                class_name="py-16 text-center border-2 border-dashed border-gray-200 rounded-lg mt-4",
            ),
        ),
        class_name="w-full",
    )