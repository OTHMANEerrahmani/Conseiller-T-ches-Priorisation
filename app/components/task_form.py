import reflex as rx
from app.states.task_state import TaskState


def form_field(
    label: str,
    placeholder: str,
    value: rx.Var,
    on_change: rx.event.EventHandler,
    type: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.input(
            placeholder=placeholder,
            on_change=on_change,
            type=type,
            class_name="mt-1 w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
            default_value=value,
        ),
        class_name="w-full",
    )


def checkbox_field(
    label: str, checked: rx.Var, on_change: rx.event.EventHandler
) -> rx.Component:
    return rx.el.div(
        rx.el.input(
            type="checkbox",
            checked=checked,
            on_change=on_change,
            class_name="h-4 w-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500",
        ),
        rx.el.label(label, class_name="ml-2 text-sm text-gray-900"),
        class_name="flex items-center",
    )


def task_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Add a new Task",
            class_name="text-lg font-semibold text-gray-800 border-b pb-2 mb-4",
        ),
        rx.el.form(
            rx.el.div(
                form_field(
                    "Task Name",
                    "e.g. Finish quarterly report",
                    TaskState.new_task_name,
                    TaskState.set_new_task_name,
                ),
                rx.el.div(
                    form_field(
                        "Deadline",
                        "",
                        TaskState.new_task_deadline,
                        TaskState.set_new_task_deadline,
                        type="date",
                    ),
                    form_field(
                        "Time (minutes)",
                        "e.g. 60",
                        TaskState.estimated_time,
                        TaskState.set_estimated_time,
                        type="number",
                    ),
                    class_name="grid grid-cols-2 gap-4",
                ),
                rx.el.div(
                    checkbox_field(
                        "Urgent", TaskState.is_urgent, TaskState.set_is_urgent
                    ),
                    checkbox_field(
                        "Important", TaskState.is_important, TaskState.set_is_important
                    ),
                    class_name="flex items-center space-x-6",
                ),
                rx.el.button(
                    rx.icon("circle_plus", class_name="mr-2 h-5 w-5"),
                    "Add Task",
                    type="submit",
                    class_name="w-full flex items-center justify-center px-4 py-2 bg-emerald-600 text-white rounded-lg shadow-md hover:bg-emerald-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500",
                ),
                class_name="flex flex-col space-y-4",
            ),
            on_submit=TaskState.add_task,
            width="100%",
        ),
        class_name="p-4 bg-white border border-gray-200 rounded-xl shadow-sm lg:col-span-2",
    )