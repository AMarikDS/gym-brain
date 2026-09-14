"""
Модуль фронтенда для приложения Gym Brain AI.
Содержит описание интерфейса и состояний на базе Reflex.
"""

import httpx
import reflex as rx

# Custom Glassmorphism Style

SEED_BUTTON_STYLE = {
    "background": "rgba(255, 255, 255, 0.03)",
    "border": "1px solid rgba(6, 182, 212, 0.3)",
    "box_shadow": "0 4px 15px -3px rgba(6, 182, 212, 0.15)",
    "color": "#e2e8f0",
    "width": "100%",
    "transition": "all 0.3s ease",
    "border_radius": "0.75rem",
    "_hover": {
        "background": "linear-gradient(90deg, rgba(6, 182, 212, 0.15), rgba(99, 102, 241, 0.15))",
        "border": "1px solid rgba(6, 182, 212, 0.8)",
        "box_shadow": "0 0 20px -3px rgba(6, 182, 212, 0.4)",
        "transform": "translateY(-2px)",
        "color": "white",
    },
}

GLASS_STYLE = {
    "bg": "rgba(255, 255, 255, 0.05)",
    "backdrop_filter": "blur(16px)",
    "-webkit-backdrop-filter": "blur(16px)",
    "border": "1px solid rgba(255, 255, 255, 0.15)",
    "border_radius": "1.5rem",
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

    def next_step(self):
        """Переключает форму на следующий шаг с валидацией."""
        if self.current_step == 1:
            try:
                age_val = float(self.age)
                if age_val < 12 or age_val > 100:
                    self.error_msg = "Invalid Age: Must be between 12 and 100 years."
                    return
            except ValueError:
                self.error_msg = "Invalid Age: Must be a number."
                return

            try:
                bw_val = float(self.bw)
                if bw_val < 30 or bw_val > 300:
                    self.error_msg = (
                        "Invalid Bodyweight: Must be between 30kg and 300kg."
                    )
                    return
            except ValueError:
                self.error_msg = "Invalid Bodyweight: Must be a number."
                return

        elif self.current_step == 2:
            for lift_name, lift_val in [
                ("Squat", self.squat),
                ("Bench", self.bench),
                ("Deadlift", self.deadlift),
            ]:
                try:
                    val = float(lift_val)
                    if val < 0 or val > 500:
                        self.error_msg = (
                            f"Invalid {lift_name} 1RM: Must be between 0 and 500kg."
                        )
                        return
                except ValueError:
                    self.error_msg = f"Invalid {lift_name} 1RM: Must be a number."
                    return

        self.error_msg = ""
        if self.current_step < 4:
            self.current_step += 1

    def prev_step(self) -> None:
        """Возвращает форму на предыдущий шаг."""
        self.error_msg = ""
        if self.current_step > 1:
            self.current_step -= 1

    history_ids: list[int] = []
    history_names: list[str] = []
    recommendations: list[dict[str, str | float | int]] = []

    current_prediction: str = ""
    is_loading: bool = False
    error_msg: str = ""

    async def get_recommendations(self) -> None:
        """Запрашивает список рекомендованных упражнений у ML-сервиса."""
        self.is_loading = True
        try:
            profile = {
                "sex": self.sex,
                "age": max(10.0, min(120.0, float(self.age))) if self.age else 25.0,
                "bw": max(20.0, min(300.0, float(self.bw))) if self.bw else 80.0,
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
        self.history_names.append(f"{len(self.history_names) + 1}. {ex_name}")

        self.is_loading = True
        try:
            profile = {
                "sex": self.sex,
                "age": max(10.0, min(120.0, float(self.age))) if self.age else 25.0,
                "bw": max(20.0, min(300.0, float(self.bw))) if self.bw else 80.0,
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
                    self.current_prediction = data.get("target_text", "")
        except (httpx.RequestError, ValueError) as e:
            print(f"Error predicting weight: {e}")

        await self.get_recommendations()
        return rx.call_script(
            "setTimeout(() => { "
            "const el = document.getElementById('trajectory-end'); "
            "if (el) el.scrollIntoView({behavior: 'smooth', block: 'end'}); "
            "}, 100);"
        )

    async def start_workout(
        self, first_ex_id: int, first_ex_name: str, raw_eq: str
    ) -> None:
        """Инициализирует сессию первым базовым упражнением."""
        self.history_ids = []
        self.history_names = []
        self.next_step()
        return await self.add_exercise(first_ex_id, first_ex_name, raw_eq)

    def reset_workout(self) -> None:
        """Сбрасывает текущую тренировочную сессию."""
        self.history_ids = []
        self.history_names = []
        self.recommendations = []
        self.current_prediction = ""
        self.current_step = 1

    @rx.var
    def trajectory_items(self) -> list[dict[str, str | bool]]:
        """Возвращает список элементов текущей траектории с флагом последнего элемента."""
        items = []
        for i, name in enumerate(self.history_names):
            items.append(
                {
                    "name": name,
                    "is_last": i == len(self.history_names) - 1,
                }
            )
        return items

    async def undo_last_exercise(self) -> None:
        """Удаляет последнее добавленное упражнение из истории и пересчитывает рекомендации."""
        if not self.history_ids:
            return

        self.history_ids.pop()
        self.history_names.pop()

        if not self.history_ids:
            self.history_ids = []
            self.history_names = []
            self.recommendations = []
            self.current_prediction = ""
            self.current_step = 3
            return

        self.is_loading = True
        try:
            await self.get_recommendations()
            self.current_prediction = "Recalculated"
        finally:
            self.is_loading = False


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
                margin_bottom="0.5rem",
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
        padding="2.5rem",
        margin_bottom="2rem",
        border_radius="xl",
        text_align="center",
        style=GLASS_STYLE,
        box_shadow="0 0 40px -10px rgba(79, 172, 254, 0.3)",
    )


def step_1_bio() -> rx.Component:
    """Генерирует первый шаг Wizard-а (Биометрический профиль)."""
    return rx.box(
        rx.heading(
            "Step 1: Biological Profile",
            size="6",
            color="white",
            margin_bottom="1.5rem",
        ),
        rx.grid(
            rx.box(
                rx.text(
                    "Level",
                    size="4",
                    color="#cbd5e1",
                    margin_bottom="0.5rem",
                    weight="medium",
                ),
                rx.select(
                    ["Novice", "Beginner", "Intermediate", "Advanced"],
                    value=State.level,
                    on_change=State.set_level,
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                    style={"width": "100%"},
                ),
            ),
            rx.box(
                rx.text(
                    "Goal",
                    size="4",
                    color="#cbd5e1",
                    margin_bottom="0.5rem",
                    weight="medium",
                ),
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
                    style={"width": "100%"},
                ),
            ),
            rx.box(
                rx.text(
                    "Sex",
                    size="4",
                    color="#cbd5e1",
                    margin_bottom="0.5rem",
                    weight="medium",
                ),
                rx.select(
                    ["Male", "Female"],
                    value=State.sex,
                    on_change=State.set_sex,
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                    style={"width": "100%"},
                ),
            ),
            rx.box(
                rx.text(
                    "Age",
                    size="4",
                    color="#cbd5e1",
                    margin_bottom="0.5rem",
                    weight="medium",
                ),
                rx.input(
                    value=State.age,
                    on_change=State.set_age,
                    type="number",
                    min="10",
                    max="120",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                    style={"width": "100%"},
                ),
            ),
            rx.box(
                rx.text(
                    "Bodyweight (kg)",
                    size="4",
                    color="#cbd5e1",
                    margin_bottom="0.5rem",
                    weight="medium",
                ),
                rx.input(
                    value=State.bw,
                    on_change=State.set_bw,
                    type="number",
                    min="20",
                    max="300",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                    style={"width": "100%"},
                ),
                style={"grid_column": "span 2"},
            ),
            columns="2",
            spacing="4",
            style={"width": "100%"},
        ),
        rx.cond(
            State.error_msg != "",
            rx.callout(
                State.error_msg,
                icon="triangle_alert",
                color_scheme="red",
                variant="surface",
                margin_top="1rem",
                margin_bottom="1rem",
            ),
        ),
        rx.flex(
            rx.button(
                "Next Step",
                on_click=State.next_step,
                size="4",
                color_scheme="cyan",
            ),
            style={"width": "100%"},
            justify="end",
            align="center",
            margin_top="1rem",
        ),
        style=GLASS_STYLE,
        margin_bottom="2rem",
    )


def step_2_stats() -> rx.Component:
    """Генерирует второй шаг Wizard-а (Инвентарь и силовые показатели)."""
    return rx.box(
        rx.heading(
            "Step 2: Equipment & Base Strength",
            size="6",
            color="white",
            margin_bottom="1.5rem",
        ),
        rx.grid(
            rx.box(
                rx.text(
                    "Available Equipment",
                    size="4",
                    color="#cbd5e1",
                    margin_bottom="0.5rem",
                    weight="medium",
                ),
                rx.select(
                    ["Machine", "Dumbbell", "Barbell", "Bodyweight", "All (Gym Mixed)"],
                    value=State.equipment,
                    on_change=State.set_equipment,
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                    style={"width": "100%"},
                ),
            ),
            rx.box(
                rx.text(
                    "Squat 1RM (kg)",
                    size="4",
                    color="#cbd5e1",
                    margin_bottom="0.5rem",
                    weight="medium",
                ),
                rx.input(
                    value=State.squat,
                    on_change=State.set_squat,
                    type="number",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                    style={"width": "100%"},
                ),
            ),
            rx.box(
                rx.text(
                    "Bench 1RM (kg)",
                    size="4",
                    color="#cbd5e1",
                    margin_bottom="0.5rem",
                    weight="medium",
                ),
                rx.input(
                    value=State.bench,
                    on_change=State.set_bench,
                    type="number",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                    style={"width": "100%"},
                ),
            ),
            rx.box(
                rx.text(
                    "Deadlift 1RM (kg)",
                    size="4",
                    color="#cbd5e1",
                    margin_bottom="0.5rem",
                    weight="medium",
                ),
                rx.input(
                    value=State.deadlift,
                    on_change=State.set_deadlift,
                    type="number",
                    variant="surface",
                    color_scheme="gray",
                    size="3",
                    style={"width": "100%"},
                ),
            ),
            columns="2",
            spacing="4",
            style={"width": "100%"},
        ),
        rx.cond(
            State.error_msg != "",
            rx.callout(
                State.error_msg,
                icon="triangle_alert",
                color_scheme="red",
                variant="surface",
                margin_top="1rem",
                margin_bottom="1rem",
            ),
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
            style={"width": "100%"},
            justify="between",
            align="center",
            margin_top="1rem",
        ),
        style=GLASS_STYLE,
        margin_bottom="2rem",
    )


def step_3_summary() -> rx.Component:
    """Генерирует третий шаг Wizard-а (Сводка и инициализация)."""
    return rx.box(
        rx.heading(
            "Step 3: Neural Initialization",
            size="6",
            color="white",
            margin_bottom="1.5rem",
        ),
        rx.text(
            "Please confirm your parameters before the AI generates your dynamic workout trajectory.",
            color="white",
            margin_bottom="1.5rem",
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
                padding="2.5rem",
                bg="rgba(0, 0, 0, 0.3)",
                border_radius="1.5rem",
                border="1px solid rgba(255,255,255,0.1)",
                style={"width": "100%"},
            ),
            margin_bottom="2rem",
        ),
        rx.heading(
            "Select Initial Muscle Group", size="4", color="white", margin_bottom="1rem"
        ),
        rx.grid(
            rx.button(
                "Chest (Bench Press)",
                on_click=lambda: State.start_workout(324, "Bench Press", "Barbell"),
                size="4",
                style=SEED_BUTTON_STYLE,
            ),
            rx.button(
                "Legs (Squat)",
                on_click=lambda: State.start_workout(340, "Barbell Squat", "Barbell"),
                size="4",
                style=SEED_BUTTON_STYLE,
            ),
            rx.button(
                "Back (Deadlift)",
                on_click=lambda: State.start_workout(
                    720, "Deadlift (Barbell)", "Barbell"
                ),
                size="4",
                style=SEED_BUTTON_STYLE,
            ),
            rx.button(
                "Shoulders (OHP)",
                on_click=lambda: State.start_workout(
                    1778, "Overhead Press (Barbell)", "Barbell"
                ),
                size="4",
                style=SEED_BUTTON_STYLE,
            ),
            rx.button(
                "Arms (Bicep Curl)",
                on_click=lambda: State.start_workout(
                    363, "Bicep Curl (Dumbbell)", "Dumbbell"
                ),
                size="4",
                style=SEED_BUTTON_STYLE,
            ),
            rx.button(
                "Core (Abs Crunch)",
                on_click=lambda: State.start_workout(
                    130, "Abs Crunch (Bodyweight)", "Bodyweight"
                ),
                size="4",
                style=SEED_BUTTON_STYLE,
            ),
            columns="2",
            spacing="4",
            style={"width": "100%"},
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
            style={"width": "100%"},
            justify="start",
            align="center",
            margin_top="1rem",
        ),
        style=GLASS_STYLE,
        margin_bottom="2rem",
    )


def recommendation_card(rec: dict[str, str | float | int]) -> rx.Component:
    """Генерирует карточку отдельного рекомендованного упражнения."""
    return rx.box(
        rx.flex(
            rx.text(rec["exercise_name"], weight="bold", size="5", color="white"),
            rx.spacer(),
            rx.badge(
                rec["equipment"],
                color_scheme="indigo",
                variant="surface",
                size="3",
            ),
            align_items="center",
        ),
        padding="1.25rem",
        margin_bottom="1rem",
        border_radius="1rem",
        bg="rgba(255, 255, 255, 0.02)",
        border="1px solid rgba(255, 255, 255, 0.05)",
        cursor="pointer",
        on_click=lambda: State.add_exercise(
            rec["exercise_id"], rec["exercise_name"], rec["equipment"]
        ),
        _hover={
            "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%)",
            "border": "1px solid rgba(6, 182, 212, 0.5)",
            "box_shadow": "0 0 20px -5px rgba(6, 182, 212, 0.3)",
        },
        transition="all 0.3s ease",
        style={"width": "100%"},
    )


def step_4_workspace() -> rx.Component:
    """Генерирует четвертый шаг Wizard-а (Рабочее пространство ML)."""
    return rx.box(
        rx.flex(
            rx.box(
                rx.heading(
                    "Current Trajectory", size="4", color="white", margin_bottom="1rem"
                ),
                rx.flex(
                    rx.foreach(
                        State.trajectory_items,
                        lambda item: rx.flex(
                            rx.text(
                                item["name"],
                                color="white",
                                size="4",
                            ),
                            rx.spacer(),
                            rx.cond(
                                item["is_last"],
                                rx.icon_button(
                                    rx.icon(tag="trash"),
                                    on_click=State.undo_last_exercise,
                                    color_scheme="red",
                                    variant="ghost",
                                    size="2",
                                    cursor="pointer",
                                    _hover={"background": "rgba(239, 68, 68, 0.2)"},
                                ),
                            ),
                            align="center",
                            width="100%",
                            bg="rgba(255, 255, 255, 0.05)",
                            border="1px solid rgba(255, 255, 255, 0.1)",
                            padding="0.75rem",
                            padding_left="1rem",
                            border_left="4px solid #06b6d4",
                            border_radius="0.75rem",
                        ),
                    ),
                    rx.box(id="trajectory-end", height="1px"),
                    direction="column",
                    spacing="3",
                    bg="rgba(255, 255, 255, 0.02)",
                    padding="1.5rem",
                    border_radius="1rem",
                    border="1px solid rgba(255, 255, 255, 0.05)",
                    max_height="350px",
                    overflow_y="auto",
                ),
                rx.cond(
                    State.current_prediction != "",
                    rx.box(
                        rx.text(
                            "AI Target Prediction",
                            size="2",
                            weight="bold",
                            letter_spacing="0.05em",
                            color="#4facfe",
                            margin_bottom="0.5rem",
                            text_transform="uppercase",
                        ),
                        rx.text(
                            State.current_prediction,
                            weight="bold",
                            size="5",
                            color="white",
                            white_space="nowrap",
                        ),
                        padding="1.5rem",
                        margin_top="1.5rem",
                        border_radius="1rem",
                        bg="rgba(6, 182, 212, 0.05)",
                        border="1px solid rgba(6, 182, 212, 0.3)",
                        border_left="6px solid #06b6d4",
                        box_shadow="0 0 20px -5px rgba(6, 182, 212, 0.1)",
                    ),
                ),
                rx.flex(
                    rx.button(
                        rx.icon(tag="arrow-left", mr="2"),
                        "Undo Last Action",
                        on_click=State.undo_last_exercise,
                        color_scheme="gray",
                        variant="soft",
                        size="3",
                        style={"width": "100%"},
                    ),
                    rx.button(
                        rx.icon(tag="rotate-ccw", mr="2"),
                        "Restart Session",
                        on_click=State.reset_workout,
                        color_scheme="red",
                        variant="soft",
                        size="3",
                        style={"width": "100%"},
                    ),
                    direction="column",
                    spacing="3",
                    margin_top="1rem",
                    width="100%",
                ),
                width="40%",
                p="4",
            ),
            rx.box(
                rx.heading(
                    "AI Next Step Generation",
                    size="4",
                    color="white",
                    margin_bottom="1rem",
                ),
                rx.cond(
                    State.is_loading,
                    rx.flex(
                        rx.spinner(color="cyan", size="3"), justify="center", p="10"
                    ),
                    rx.box(
                        rx.foreach(State.recommendations, recommendation_card),
                        max_height="600px",
                        overflow_y="auto",
                        padding_right="1rem",
                        padding_left="0.5rem",
                        padding_top="0.5rem",
                        padding_bottom="0.5rem",
                    ),
                ),
                width="60%",
                p="4",
                border_left="1px solid rgba(255,255,255,0.1)",
            ),
            direction="row",
            spacing="4",
            align_items="flex-start",
            style={"width": "100%"},
        ),
        style=GLASS_STYLE,
        margin_bottom="2rem",
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
        style={"width": "100%"},
        font_family="Inter, sans-serif",
    )


app = rx.App()
app.add_page(index, title="Gym Brain AI")
