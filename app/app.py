import reflex as rx
from app.states.task_state import TaskState
from app.components.task_form import task_form
from app.components.task_list import task_list
from app.components.stats import stats_cards
from app.components.completed_tasks import completed_tasks_list
from app.components.documentation import documentation_section


def index() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "bot-message-square", class_name="h-8 w-8 text-emerald-500"
                    ),
                    rx.el.h1(
                        "Virtual Advisor", class_name="text-2xl font-bold text-gray-800"
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.button(
                    "Load Test Data",
                    on_click=TaskState.load_test_data,
                    class_name="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors",
                ),
                class_name="container mx-auto flex items-center justify-between p-4 border-b border-gray-200",
            )
        ),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    task_form(),
                    stats_cards(),
                    class_name="grid lg:grid-cols-3 gap-8 items-start",
                ),
                task_list(),
                documentation_section(),
                completed_tasks_list(),
                class_name="container mx-auto p-4 md:p-8 flex flex-col gap-8",
            ),
            class_name="bg-gray-50/50",
        ),
        class_name="min-h-screen bg-white font-['JetBrains_Mono']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)