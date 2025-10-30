import reflex as rx
from app.states.task_state import TaskState
from app.components.task_form import task_form
from app.components.task_list import task_list
from app.components.stats import stats_cards
from app.components.completed_tasks import completed_tasks_list
from app.components.documentation import documentation_section
from app.components.calendar import calendar_view


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("bot-message-square", class_name="h-8 w-8 text-emerald-600"),
                rx.el.h1(
                    "Virtual Advisor",
                    class_name="text-xl font-bold text-gray-800 tracking-tight",
                ),
                class_name="flex items-center gap-3 h-16 px-4 border-b shrink-0",
            ),
            rx.el.nav(
                rx.el.a(
                    rx.icon("layout-dashboard", class_name="h-5 w-5"),
                    rx.el.span("Dashboard"),
                    href="#",
                    on_click=lambda: TaskState.set_active_view("dashboard"),
                    class_name=rx.cond(
                        TaskState.active_view == "dashboard",
                        "flex items-center gap-3 rounded-lg bg-emerald-100 px-3 py-2 text-emerald-700 font-semibold transition-all hover:text-emerald-800",
                        "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-600 transition-all hover:text-gray-900",
                    ),
                ),
                class_name="flex-1 p-4 overflow-auto",
            ),
        ),
        class_name="hidden md:flex flex-col border-r bg-gray-100/40 w-64",
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.button(
            rx.icon("menu", class_name="h-6 w-6"),
            on_click=TaskState.toggle_mobile_menu,
            class_name="md:hidden p-2 rounded-md hover:bg-gray-200",
            aria_controls="mobile-sidebar",
            aria_expanded=TaskState.show_mobile_menu.to_string(),
        ),
        rx.el.div(class_name="flex-1"),
        rx.el.button(
            "Load Test Data",
            on_click=TaskState.load_test_data,
            class_name="px-3 py-1.5 text-sm bg-emerald-600 text-white rounded-md hover:bg-emerald-700 transition-colors",
        ),
        class_name="flex h-16 items-center gap-4 border-b bg-gray-100/40 px-6 shrink-0",
    )


def dashboard_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(stats_cards(), task_form(), class_name="flex flex-col gap-8"),
            task_list(),
            calendar_view(),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 items-start",
        ),
        rx.el.div(
            completed_tasks_list(),
            documentation_section(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start mt-8",
        ),
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.match(
                    TaskState.active_view,
                    ("dashboard", dashboard_view()),
                    rx.el.div("Unknown view"),
                ),
                class_name="p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col flex-1 overflow-hidden",
        ),
        rx.cond(
            TaskState.show_mobile_menu,
            rx.el.div(
                sidebar(),
                class_name="absolute inset-0 bg-black/50 z-10 md:hidden",
                id="mobile-sidebar",
            ),
            None,
        ),
        class_name="grid min-h-screen w-full md:grid-cols-[256px_1fr] font-['JetBrains_Mono'] relative",
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
app.add_page(index, on_load=TaskState.load_test_data)