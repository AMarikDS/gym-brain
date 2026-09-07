"""
Модуль фронтенда для приложения Gym Brain AI.
Содержит описание интерфейса и состояний на базе Reflex.
"""

# BSL License
# Copyright (c) 2025 RTA Technologies

import httpx
import reflex as rx

# Custom Glassmorphism Style
GLASS_STYLE = {
    "bg": "rgba(255, 255, 255, 0.05)",
    "backdrop_filter": "blur(16px)",
    "-webkit-backdrop-filter": "blur(16px)",
    "border": "1px solid rgba(255, 255, 255, 0.15)",
    "border_radius": "xl",
    "box_shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 1px 1px rgba(255,255,255,0.1)",
    "padding": "2rem",
}


class State(rx.State):
    """
    Класс, описывающий глобальное состояние приложения (Wizard-формы и логику ML).
    """

    current_step: int = 1

    level: str = "Intermediate"
    goal: str = "Bodybuilding"
    sex: str = "Male"
    age: str = "25"
    bw: str = "80"
    equipment: str = "All (Gym Mixed)"

    squat: str = "0"
    bench: str = "0"
    deadlift: str = "0"

    def set_level(self, val: str) -> None:
        """Устанавливает уровень подготовки."""
        self.level = val

    def set_goal(self, val: str) -> None:
        """Устанавливает тренировочную цель."""
        self.goal = val

    def set_sex(self, val: str) -> None:
        """Устанавливает пол."""
        self.sex = val

    def set_equipment(self, val: str) -> None:
        """Устанавливает доступный инвентарь."""
        self.equipment = val

    def set_squat(self, val: str) -> None:
        """Устанавливает 1RM для приседаний."""
        self.squat = val

    def set_bench(self, val: str) -> None:
        """Устанавливает 1RM для жима лежа."""
        self.bench = val

    def set_deadlift(self, val: str) -> None:
        """Устанавливает 1RM для становой тяги."""
        self.deadlift = val

    def set_age(self, val: str) -> None:
        """Устанавливает возраст."""
        self.age = val

    def set_bw(self, val: str) -> None:
        """Устанавливает собственный вес."""
        self.bw = val

    def next_step(self) -> None:
        """Переключает форму на следующий шаг."""
        if self.current_step < 4:
            self.current_step += 1

    def prev_step(self) -> None:
        """Возвращает форму на предыдущий шаг."""
        if self.current_step > 1:
            self.current_step -= 1

    history_ids: list[int] = []
    history_names: list[str] = []
    recommendations: list[dict[str, str | float | int]] = []

    current_prediction: str = ""
    is_loading: bool = False

    async def get_recommendations(self) -> None:
        """Запрашивает список рекомендованных упражнений у ML-сервиса."""
        self.is_loading = True
        try:
            profile = {
                "sex": self.sex,
                "age": float(self.age) if self.age else 25.0,
                "bw": float(self.bw) if self.bw else 80.0,
                "level": self.level,
                "goal": self.goal,
                "equipment": self.equipment,
                "sbd": [
                    float(self.squat or 0.0),
                    float(self.bench or 0.0),
                    float(self.deadlift or 0.0),
                ],
            }

            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://backend:8080/api/v1/recommend",
                    json={
                        "history_ids": self.history_ids,
                        "profile": profile,
                        "top_k": 10,
                    },
                    timeout=10.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    self.recommendations = data.get("recommendations", [])
                else:
                    self.recommendations = []
        except (httpx.RequestError, ValueError) as e:
            print(f"Error fetching recommendations: {e}")
            self.recommendations = []
        finally:
            self.is_loading = False

    async def add_exercise(self, ex_id: int, ex_name: str, raw_eq: str) -> None:
        """Добавляет упражнение в историю и предсказывает целевой рабочий вес."""
        self.history_ids.append(ex_id)
        self.history_names.append(ex_name)

        self.is_loading = True
        try:
            profile = {
                "sex": self.sex,
                "age": float(self.age) if self.age else 25.0,
                "bw": float(self.bw) if self.bw else 80.0,
                "level": self.level,
                "goal": self.goal,
                "equipment": self.equipment,
                "sbd": [
                    float(self.squat or 0.0),
                    float(self.bench or 0.0),
                    float(self.deadlift or 0.0),
                ],
            }

            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://backend:8080/api/v1/predict_weight",
                    json={
                        "profile": profile,
                        "exercise_name": ex_name,
                        "raw_equipment": raw_eq,
                    },
                    timeout=10.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    weight = data.get("weight", 0)
                    reps = data.get("reps", 0)
                    self.current_prediction = (
                        f"Optimal Target: {weight} kg x {reps} reps"
                    )
        except (httpx.RequestError, ValueError) as e:
            print(f"Error predicting weight: {e}")

        await self.get_recommendations()

    async def start_workout(
        self, first_ex_id: int, first_ex_name: str, raw_eq: str
    ) -> None:
        """Инициализирует сессию первым базовым упражнением."""
        self.history_ids = []
        self.history_names = []
        self.next_step()
        await self.add_exercise(first_ex_id, first_ex_name, raw_eq)

    def reset_workout(self) -> None:
        """Сбрасывает текущую тренировочную сессию."""
        self.history_ids = []
        self.history_names = []
        self.recommendations = []
        self.current_prediction = ""
        self.current_step = 1


def hero_section() -> rx.Component:
    """Генерирует верхний промо-заголовок (Hero Section)."""
    return rx.box(
        rx.flex(
            rx.heading(
                "Gym Brain AI",
                size="9",
                weight="bold",
                background_image="linear-gradient(270deg, #00f2fe, #4facfe)",
                background_clip="text",
                color="transparent",
                mb="2",
            ),
            rx.text(
                "Hyper-Personalized Fitness Intelligence",
                size="4",
                color="white",
                weight="medium",
                letter_spacing="0.05em",
            ),
            direction="column",
            align_items="center",
        ),
        p="6",
        mb="8",
        border_radius="xl",
        text_align="center",
        style=GLASS_STYLE,
        box_shadow="0 0 40px -10px rgba(79, 172, 254, 0.3)",
    )


def step_1_bio() -> rx.Component:
    """Генерирует первый шаг Wizard-а (Биометрический профиль)."""
    return rx.box(
        rx.heading("Step 1: Biological Profile", size="6", color="white", mb="6"),
        rx.grid(
            rx.box(
                rx.text("Level", size="3", color="#cbd5e1", mb="2", weight="medium"),
                rx.select(
                    ["Novice", "Beginner", "Intermediate", "Advanced"],
                    value=State.level,
                    on_change=State.set_level,
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                ),
            ),
            rx.box(
                rx.text("Goal", size="3", color="#cbd5e1", mb="2", weight="medium"),
                rx.select(
                    [
                        "Powerbuilding",
                        "Bodybuilding",
                        "Athletics",
                        "Powerlifting",
                        "Fitness",
                    ],
                    value=State.goal,
                    on_change=State.set_goal,
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                ),
            ),
            rx.box(
                rx.text("Sex", size="3", color="#cbd5e1", mb="2", weight="medium"),
                rx.select(
                    ["Male", "Female"],
                    value=State.sex,
                    on_change=State.set_sex,
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                ),
            ),
            rx.box(
                rx.text("Age", size="3", color="#cbd5e1", mb="2", weight="medium"),
                rx.input(
                    value=State.age,
                    on_change=State.set_age,
                    type="number",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                ),
            ),
            rx.box(
                rx.text(
                    "Bodyweight (kg)",
                    size="3",
                    color="#cbd5e1",
                    mb="2",
                    weight="medium",
                ),
                rx.input(
                    value=State.bw,
                    on_change=State.set_bw,
                    type="number",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                ),
            ),
            columns="2",
            spacing="6",
        ),
        rx.flex(
            rx.button(
                "Next Step", on_click=State.next_step, size="4", color_scheme="cyan"
            ),
            width="100%",
            justify="end",
            align="center",
            mt="9",
        ),
        style=GLASS_STYLE,
        mb="8",
    )


def step_2_stats() -> rx.Component:
    """Генерирует второй шаг Wizard-а (Инвентарь и силовые показатели)."""
    return rx.box(
        rx.heading(
            "Step 2: Equipment & Base Strength", size="6", color="white", mb="6"
        ),
        rx.grid(
            rx.box(
                rx.text(
                    "Available Equipment",
                    size="3",
                    color="#cbd5e1",
                    mb="2",
                    weight="medium",
                ),
                rx.select(
                    ["Machine", "Dumbbell", "Barbell", "Bodyweight", "All (Gym Mixed)"],
                    value=State.equipment,
                    on_change=State.set_equipment,
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                ),
            ),
            rx.box(
                rx.text(
                    "Squat 1RM (kg)", size="3", color="#cbd5e1", mb="2", weight="medium"
                ),
                rx.input(
                    value=State.squat,
                    on_change=State.set_squat,
                    type="number",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                ),
            ),
            rx.box(
                rx.text(
                    "Bench 1RM (kg)", size="3", color="#cbd5e1", mb="2", weight="medium"
                ),
                rx.input(
                    value=State.bench,
                    on_change=State.set_bench,
                    type="number",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                ),
            ),
            rx.box(
                rx.text(
                    "Deadlift 1RM (kg)",
                    size="3",
                    color="#cbd5e1",
                    mb="2",
                    weight="medium",
                ),
                rx.input(
                    value=State.deadlift,
                    on_change=State.set_deadlift,
                    type="number",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                ),
            ),
            columns="2",
            spacing="6",
        ),
        rx.flex(
            rx.button(
                "Back",
                on_click=State.prev_step,
                size="4",
                style={
                    "background_color": "rgba(255,255,255,0.1)",
                    "color": "white",
                    "border": "1px solid rgba(255,255,255,0.2)",
                    "cursor": "pointer",
                },
            ),
            rx.button(
                "Review Profile",
                on_click=State.next_step,
                size="4",
                color_scheme="cyan",
            ),
            width="100%",
            justify="between",
            align="center",
            mt="9",
        ),
        style=GLASS_STYLE,
        mb="8",
    )


def step_3_summary() -> rx.Component:
    """Генерирует третий шаг Wizard-а (Сводка и инициализация)."""
    return rx.box(
        rx.heading("Step 3: Neural Initialization", size="6", color="white", mb="6"),
        rx.text(
            "Please confirm your parameters before the AI generates your dynamic workout trajectory.",
            color="white",
            mb="6",
            size="3",
        ),
        rx.box(
            rx.grid(
                rx.text("Profile:", weight="bold", color="#4facfe"),
                rx.text(f"{State.sex}, {State.age} yrs, {State.bw} kg", color="white"),
                rx.text("Goal / Level:", weight="bold", color="#4facfe"),
                rx.text(f"{State.goal} ({State.level})", color="white"),
                rx.text("Equipment:", weight="bold", color="#4facfe"),
                rx.text(State.equipment, color="white"),
                rx.text("Strength (S/B/D):", weight="bold", color="#4facfe"),
                rx.text(
                    f"{State.squat} / {State.bench} / {State.deadlift} kg",
                    color="white",
                ),
                columns="2",
                spacing="4",
                p="6",
                bg="rgba(0, 0, 0, 0.3)",
                border_radius="md",
                border="1px solid rgba(255,255,255,0.1)",
            ),
            mb="8",
        ),
        rx.heading("Initialize Seed Exercise", size="4", color="white", mb="4"),
        rx.grid(
            rx.button(
                "Initialize with Bench Press",
                on_click=lambda: State.start_workout(324, "Bench Press", "Barbell"),
                size="4",
                color_scheme="cyan",
                box_shadow="0 0 20px -3px rgba(6, 182, 212, 0.5)",
                _hover={"transform": "scale(1.02)"},
            ),
            rx.button(
                "Initialize with Squat",
                on_click=lambda: State.start_workout(340, "Barbell Squat", "Barbell"),
                size="4",
                color_scheme="indigo",
                box_shadow="0 0 20px -3px rgba(99, 102, 241, 0.5)",
                _hover={"transform": "scale(1.02)"},
            ),
            columns="2",
            spacing="4",
        ),
        rx.flex(
            rx.button(
                "Edit Settings",
                on_click=State.prev_step,
                size="3",
                style={
                    "background_color": "rgba(255,255,255,0.1)",
                    "color": "white",
                    "border": "1px solid rgba(255,255,255,0.2)",
                    "cursor": "pointer",
                },
            ),
            width="100%",
            justify="start",
            align="center",
            mt="9",
        ),
        style=GLASS_STYLE,
        mb="8",
    )


def recommendation_card(rec: dict[str, str | float | int]) -> rx.Component:
    """Генерирует карточку отдельного рекомендованного упражнения."""
    return rx.box(
        rx.flex(
            rx.box(
                rx.text(rec["exercise_name"], weight="bold", size="4", color="white"),
                rx.flex(
                    rx.badge(
                        rec["equipment"],
                        color_scheme="indigo",
                        variant="soft",
                        size="2",
                        mr="2",
                    ),
                    rx.badge(
                        f"Match Score: {rec['final_score']}",
                        color_scheme="cyan",
                        variant="surface",
                        size="2",
                    ),
                    mt="3",
                ),
            ),
            rx.spacer(),
            rx.button(
                rx.icon(tag="plus", size=20),
                "Add to Routine",
                on_click=lambda: State.add_exercise(
                    rec["exercise_id"], rec["exercise_name"], rec["equipment"]
                ),
                size="3",
                color_scheme="cyan",
                variant="solid",
                box_shadow="0 0 15px -3px rgba(6, 182, 212, 0.4)",
                _hover={
                    "transform": "scale(1.05)",
                    "box_shadow": "0 0 20px 0px rgba(6, 182, 212, 0.6)",
                },
            ),
            align_items="center",
        ),
        p="5",
        mb="4",
        border_radius="lg",
        bg="rgba(255, 255, 255, 0.05)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        _hover={
            "bg": "rgba(255, 255, 255, 0.08)",
            "border": "1px solid rgba(6, 182, 212, 0.5)",
        },
        transition="all 0.2s ease",
    )


def step_4_workspace() -> rx.Component:
    """Генерирует четвертый шаг Wizard-а (Рабочее пространство ML)."""
    return rx.box(
        rx.flex(
            rx.box(
                rx.heading("Current Trajectory", size="5", color="white", mb="4"),
                rx.flex(
                    rx.foreach(
                        State.history_names,
                        lambda name: rx.badge(
                            name,
                            color_scheme="cyan",
                            variant="outline",
                            mr="2",
                            mb="2",
                            size="3",
                            border_color="rgba(6, 182, 212, 0.6)",
                            color="cyan.100",
                        ),
                    ),
                    wrap="wrap",
                ),
                rx.cond(
                    State.current_prediction != "",
                    rx.box(
                        rx.text(
                            "AI Target Prediction", size="2", color="#4facfe", mb="1"
                        ),
                        rx.text(
                            State.current_prediction,
                            weight="bold",
                            size="5",
                            color="white",
                        ),
                        p="5",
                        mt="6",
                        border_radius="md",
                        bg="rgba(6, 182, 212, 0.15)",
                        border_left="4px solid #06b6d4",
                    ),
                ),
                rx.button(
                    rx.icon(tag="rotate-ccw", mr="2"),
                    "End & Reset Workout",
                    on_click=State.reset_workout,
                    color_scheme="red",
                    variant="soft",
                    mt="9",
                    size="3",
                    width="100%",
                ),
                width="35%",
                p="4",
            ),
            rx.box(
                rx.heading("AI Next Step Generation", size="5", color="white", mb="4"),
                rx.cond(
                    State.is_loading,
                    rx.flex(
                        rx.spinner(color="cyan", size="3"), justify="center", p="10"
                    ),
                    rx.box(
                        rx.foreach(State.recommendations, recommendation_card),
                        max_height="600px",
                        overflow_y="auto",
                        pr="2",
                    ),
                ),
                width="65%",
                p="4",
                border_left="1px solid rgba(255,255,255,0.1)",
            ),
            direction="row",
            spacing="6",
            align_items="flex-start",
        ),
        style=GLASS_STYLE,
        mb="8",
    )


def index() -> rx.Component:
    """Главная страница приложения."""
    return rx.box(
        rx.container(
            rx.script(
                (
                    "document.documentElement.classList.add('dark'); "
                    "document.documentElement.setAttribute('data-theme', 'dark'); "
                    "localStorage.setItem('theme', 'dark');"
                )
            ),
            hero_section(),
            rx.match(
                State.current_step,
                (1, step_1_bio()),
                (2, step_2_stats()),
                (3, step_3_summary()),
                (4, step_4_workspace()),
                step_1_bio(),
            ),
            max_width="1200px",
            margin_x="auto",
            padding_y="10",
            transition="max-width 0.4s ease-in-out",
        ),
        bg="radial-gradient(circle at top center, #1e1b4b, #050505 80%)",
        min_height="100vh",
        width="100%",
        font_family="Inter, sans-serif",
    )


app = rx.App()
app.add_page(index, title="Gym Brain AI")
