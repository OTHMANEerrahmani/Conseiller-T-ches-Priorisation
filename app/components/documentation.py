import reflex as rx
from app.states.task_state import TaskState


def rule_item(title: str, description: str, score_effect: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(title, class_name="font-semibold text-gray-800"),
            rx.el.span(
                score_effect,
                class_name="px-2 py-0.5 text-xs font-bold text-emerald-800 bg-emerald-100 rounded-full",
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.p(description, class_name="text-sm text-gray-600 mt-1"),
        class_name="p-3 bg-gray-50 border border-gray-200/80 rounded-lg",
    )


def documentation_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Scoring Logic Explained",
                class_name="text-lg font-semibold text-gray-800",
            ),
            rx.el.button(
                rx.icon(rx.cond(TaskState.show_rules, "chevron-up", "chevron-down")),
                "Show/Hide Rules",
                on_click=TaskState.toggle_rules,
                class_name="flex items-center gap-2 px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors",
            ),
            class_name="flex items-center justify-between pb-2 border-b",
        ),
        rx.cond(
            TaskState.show_rules,
            rx.el.div(
                rule_item(
                    "Matrix Quadrant I: Urgent & Important",
                    "Highest priority for critical, time-sensitive tasks.",
                    "+1000",
                ),
                rule_item(
                    "Matrix Quadrant II: Important, Not Urgent",
                    "High priority for long-term goals and planning.",
                    "+500",
                ),
                rule_item(
                    "Matrix Quadrant III: Urgent, Not Important",
                    "Medium priority for interruptions that need quick handling.",
                    "+250",
                ),
                rule_item("Imminent Deadline", "Task is due within 1 day.", "+200"),
                rule_item("Short-Term Deadline", "Task is due within 3 days.", "+100"),
                rule_item("Mid-Term Deadline", "Task is due within 7 days.", "+50"),
                rule_item(
                    "Quick Win", "Can be completed in 15 minutes or less.", "+40"
                ),
                rule_item("Focus Task", "Takes 16-30 minutes, easy to fit in.", "+20"),
                rule_item(
                    "Strategic Importance Boost",
                    "Extra points for important tasks that are not urgent.",
                    "+60",
                ),
                rule_item(
                    "Urgent Push",
                    "Extra points for urgent tasks that are not important.",
                    "+30",
                ),
                rule_item(
                    "Critical Pressure",
                    "Short deadline (<= 2 days) but requires significant time (> 60 min).",
                    "+80",
                ),
                rule_item(
                    "Long Task Penalty",
                    "Tasks requiring over 2 hours are slightly deprioritized.",
                    "-30",
                ),
                rule_item(
                    "Matrix Quadrant IV: Not Urgent/Important",
                    "Low priority tasks are penalized to focus on what matters.",
                    "-50",
                ),
                rule_item(
                    "Far-Future Penalty",
                    "Tasks with deadlines over a month away are heavily deprioritized.",
                    "-100",
                ),
                class_name="grid md:grid-cols-2 lg:grid-cols-3 gap-3 mt-4",
            ),
            rx.fragment(),
        ),
        class_name="w-full",
    )