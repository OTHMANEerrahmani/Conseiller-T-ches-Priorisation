import reflex as rx
from app.states.task_state import TaskState


def stat_card(icon: str, label: str, value: rx.Var, color_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 {color_class}"),
            class_name="p-2 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-800"),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-xl shadow-sm",
    )


def stats_cards() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "At a Glance",
            class_name="text-lg font-semibold text-gray-800 border-b pb-2 mb-4",
        ),
        rx.el.div(
            stat_card(
                "flag_triangle_right",
                "Urgent",
                TaskState.urgent_tasks_count,
                "text-yellow-600",
            ),
            stat_card(
                "star", "Important", TaskState.important_tasks_count, "text-red-600"
            ),
            stat_card(
                "zap", "Quick Tasks", TaskState.quick_tasks_count, "text-blue-600"
            ),
            stat_card(
                "square_check",
                "Completed",
                TaskState.completed_taches.length(),
                "text-emerald-600",
            ),
            class_name="flex flex-col gap-4",
        ),
        class_name="p-4 bg-white border border-gray-200 rounded-xl shadow-sm lg:col-span-1",
    )