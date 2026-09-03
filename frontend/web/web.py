import reflex as rx
import httpx
from typing import List, Dict, Any

# Custom Glassmorphism Style
glass_style = {
    "bg": "rgba(255, 255, 255, 0.03)",
    "backdrop_filter": "blur(12px)",
    "-webkit-backdrop-filter": "blur(12px)",
    "border": "1px solid rgba(255, 255, 255, 0.08)",
    "border_radius": "xl",
    "box_shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
    "padding": "1.5rem",
}

class State(rx.State):
    # Profile State
    level: str = "Intermediate"
    goal: str = "Bodybuilding"
    equipment: str = "All (Gym Mixed)"
    sex: str = "Male"
    age: str = "25"
    bw: str = "80"
    
    # Powerlifting Stats (SBD)
    squat: str = "0"
    bench: str = "0"
    deadlift: str = "0"

    def set_level(self, val: str):
        self.level = val

    def set_goal(self, val: str):
        self.goal = val

    def set_equipment(self, val: str):
        self.equipment = val

    def set_squat(self, val: str):
        self.squat = val

    def set_bench(self, val: str):
        self.bench = val

    def set_deadlift(self, val: str):
        self.deadlift = val
    
    # Workout State
    history_ids: List[int] = []
    history_names: List[str] = []
    recommendations: List[Dict[str, Any]] = []
    
    # Current Selected Exercise Details
    current_prediction: str = ""
    is_loading: bool = False

    async def get_recommendations(self):
        self.is_loading = True
        try:
            profile = {
                "sex": self.sex,
                "age": float(self.age) if self.age else 25,
                "bw": float(self.bw) if self.bw else 80,
                "level": self.level,
                "goal": self.goal,
                "equipment": self.equipment,
                "sbd": [float(self.squat or 0), float(self.bench or 0), float(self.deadlift or 0)]
            }
            
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://backend:8080/api/v1/recommend",
                    json={
                        "history_ids": self.history_ids,
                        "profile": profile,
                        "top_k": 10
                    },
                    timeout=10.0
                )
                if resp.status_code == 200:
                    data = resp.json()
                    self.recommendations = data.get("recommendations", [])
                else:
                    self.recommendations = []
        except Exception as e:
            print(e)
        finally:
            self.is_loading = False

    async def add_exercise(self, ex_id: int, ex_name: str, raw_eq: str):
        self.history_ids.append(ex_id)
        self.history_names.append(ex_name)
        
        # Get weight prediction
        self.is_loading = True
        try:
            profile = {
                "sex": self.sex,
                "age": float(self.age) if self.age else 25,
                "bw": float(self.bw) if self.bw else 80,
                "level": self.level,
                "goal": self.goal,
                "equipment": self.equipment,
                "sbd": [float(self.squat or 0), float(self.bench or 0), float(self.deadlift or 0)]
            }
            
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://backend:8080/api/v1/predict_weight",
                    json={
                        "profile": profile,
                        "exercise_name": ex_name,
                        "raw_equipment": raw_eq
                    },
                    timeout=10.0
                )
                if resp.status_code == 200:
                    data = resp.json()
                    weight = data.get("weight", 0)
                    reps = data.get("reps", 0)
                    self.current_prediction = f"🎯 Optimal Target: {weight} kg x {reps} reps"
        except Exception as e:
            print(e)
            
        await self.get_recommendations()

    async def start_workout(self, first_ex_id: int, first_ex_name: str, raw_eq: str):
        self.history_ids = []
        self.history_names = []
        await self.add_exercise(first_ex_id, first_ex_name, raw_eq)

    def reset_workout(self):
        self.history_ids = []
        self.history_names = []
        self.recommendations = []
        self.current_prediction = ""


def hero_section():
    return rx.box(
        rx.flex(
            rx.heading(
                "Gym Brain AI", 
                size="9", 
                weight="bold", 
                background_image="linear-gradient(270deg, #06b6d4, #3b82f6)",
                background_clip="text",
                color="transparent",
                mb="2"
            ),
            rx.text(
                "Hyper-Personalized Fitness Intelligence", 
                size="4", 
                color="gray.400", 
                weight="medium",
                letter_spacing="0.05em"
            ),
            direction="column",
            align_items="center",
        ),
        p="6",
        mb="8",
        border_radius="xl",
        text_align="center",
        style=glass_style,
        box_shadow="0 0 40px -10px rgba(6, 182, 212, 0.2)",
    )

def profile_section():
    return rx.box(
        rx.flex(
            rx.icon(tag="settings", color="cyan", size=24, mr="2"),
            rx.heading("Biological & Context Profile", size="5", color="gray.200"),
            align_items="center",
            mb="6"
        ),
        rx.grid(
            rx.box(
                rx.text("Level", size="2", color="gray.400", mb="1"),
                rx.select(
                    ["Novice", "Beginner", "Intermediate", "Advanced"], 
                    value=State.level, on_change=State.set_level,
                    variant="soft", color_scheme="gray"
                ),
            ),
            rx.box(
                rx.text("Goal", size="2", color="gray.400", mb="1"),
                rx.select(
                    ['Powerbuilding', 'Bodybuilding', 'Athletics', 'Powerlifting', 'Muscle & Sculpting', 'Bodyweight Fitness', 'Fitness'], 
                    value=State.goal, on_change=State.set_goal,
                    variant="soft", color_scheme="gray"
                ),
            ),
            rx.box(
                rx.text("Equipment", size="2", color="gray.400", mb="1"),
                rx.select(
                    ['Machine', 'Dumbbell', 'Barbell', 'Bodyweight', 'All (Gym Mixed)'], 
                    value=State.equipment, on_change=State.set_equipment,
                    variant="soft", color_scheme="gray"
                ),
            ),
            rx.box(
                rx.text("Squat 1RM (kg)", size="2", color="gray.400", mb="1"),
                rx.input(value=State.squat, on_change=State.set_squat, type="number", variant="soft", color_scheme="gray"),
            ),
            rx.box(
                rx.text("Bench 1RM (kg)", size="2", color="gray.400", mb="1"),
                rx.input(value=State.bench, on_change=State.set_bench, type="number", variant="soft", color_scheme="gray"),
            ),
            rx.box(
                rx.text("Deadlift 1RM (kg)", size="2", color="gray.400", mb="1"),
                rx.input(value=State.deadlift, on_change=State.set_deadlift, type="number", variant="soft", color_scheme="gray"),
            ),
            columns="3",
            spacing="4",
        ),
        style=glass_style,
        mb="8"
    )

def recommendation_card(rec):
    return rx.box(
        rx.flex(
            rx.box(
                rx.text(rec["exercise_name"], weight="bold", size="3", color="gray.100"),
                rx.flex(
                    rx.badge(rec["equipment"], color_scheme="indigo", variant="soft", size="1", mr="2"),
                    rx.badge(f"Match: {rec['final_score']}", color_scheme="cyan", variant="surface", size="1"),
                    mt="2"
                )
            ),
            rx.spacer(),
            rx.button(
                rx.icon(tag="plus", size=16),
                "Add",
                on_click=lambda: State.add_exercise(rec["exercise_id"], rec["exercise_name"], rec["equipment"]),
                size="2",
                color_scheme="cyan",
                variant="solid",
                border_radius="full",
                box_shadow="0 0 15px -3px rgba(6, 182, 212, 0.4)",
                _hover={"transform": "scale(1.05)", "box_shadow": "0 0 20px 0px rgba(6, 182, 212, 0.6)"}
            ),
            align_items="center"
        ),
        p="4",
        mb="3",
        border_radius="lg",
        bg="rgba(255, 255, 255, 0.02)",
        border="1px solid rgba(255, 255, 255, 0.05)",
        _hover={"bg": "rgba(255, 255, 255, 0.04)", "border": "1px solid rgba(6, 182, 212, 0.3)"},
        transition="all 0.2s ease"
    )

def workout_builder():
    return rx.box(
        rx.flex(
            rx.icon(tag="activity-log", color="cyan", size=24, mr="2"),
            rx.heading("Workout Sequence", size="5", color="gray.200"),
            align_items="center",
            mb="6"
        ),
        rx.cond(
            State.history_names.length() > 0,
            rx.box(
                rx.text("Current Trajectory:", size="2", color="gray.400", mb="3"),
                rx.flex(
                    rx.foreach(
                        State.history_names,
                        lambda name, idx: rx.badge(
                            name, 
                            color_scheme="cyan", 
                            variant="outline", 
                            mr="2", mb="2", size="2",
                            border_color="rgba(6, 182, 212, 0.4)"
                        )
                    ),
                    wrap="wrap"
                ),
                rx.cond(
                    State.current_prediction != "",
                    rx.box(
                        rx.text(State.current_prediction, weight="bold", size="4", color="cyan.300"),
                        p="4",
                        mt="4",
                        mb="6",
                        border_radius="md",
                        bg="rgba(6, 182, 212, 0.1)",
                        border_left="4px solid #06b6d4"
                    )
                ),
                rx.divider(mb="6", mt="4", border_color="rgba(255, 255, 255, 0.1)"),
                rx.text("AI Generated Next Steps:", size="2", color="gray.400", mb="3"),
                rx.cond(
                    State.is_loading,
                    rx.flex(rx.spinner(color="cyan"), justify="center", p="6"),
                    rx.foreach(
                        State.recommendations,
                        recommendation_card
                    )
                ),
                rx.button(
                    "Reset Matrix", 
                    on_click=State.reset_workout, 
                    color_scheme="red", 
                    variant="soft",
                    mt="4",
                    width="100%"
                )
            ),
            rx.box(
                rx.flex(
                    rx.icon(tag="lightning-bolt", size=40, color="gray.500", mb="4"),
                    rx.text("Initialize neural network by selecting the first movement.", color="gray.400", text_align="center", mb="6"),
                    rx.button(
                        "Initialize with Bench Press", 
                        on_click=lambda: State.start_workout(324, "Bench Press", "Barbell"), 
                        size="3",
                        color_scheme="cyan",
                        box_shadow="0 0 20px -3px rgba(6, 182, 212, 0.5)",
                        _hover={"transform": "scale(1.02)"}
                    ),
                    direction="column",
                    align_items="center",
                    justify="center",
                    p="8"
                )
            )
        ),
        style=glass_style
    )

def index():
    return rx.box(
        rx.container(
            hero_section(),
            profile_section(),
            workout_builder(),
            max_width="800px",
            margin_x="auto",
            padding_y="12",
        ),
        bg="radial-gradient(circle at top right, #1e1b4b, #000000 60%)",
        min_height="100vh",
        width="100%",
        font_family="Inter, sans-serif"
    )

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=False,
        radius="large",
        accent_color="cyan",
        gray_color="slate"
    )
)
app.add_page(index, title="Gym Brain AI")
