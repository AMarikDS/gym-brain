import reflex as rx
import httpx
from typing import List, Dict, Any

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
                    self.current_prediction = f"Suggested: {weight} kg x {reps} reps"
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
        rx.heading("Gym Brain AI", size="9", weight="bold", color="white"),
        rx.text("Your personal AI trainer powered by Deep Learning.", size="4", color="gray.300", mt="2"),
        rx.text("Design intelligent workouts and predict optimal weights dynamically.", size="3", color="gray.400"),
        bg="linear-gradient(to right, #111827, #1f2937)",
        p="8",
        border_radius="xl",
        text_align="center",
        mb="8",
        box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.5)"
    )

def profile_section():
    return rx.card(
        rx.heading("1. Setup Your Profile", size="5", mb="4"),
        rx.flex(
            rx.box(
                rx.text("Level", weight="bold"),
                rx.select(
                    ["Novice", "Beginner", "Intermediate", "Advanced"], 
                    value=State.level, on_change=State.set_level
                ),
                width="100%"
            ),
            rx.box(
                rx.text("Goal", weight="bold"),
                rx.select(
                    ['Powerbuilding', 'Bodybuilding', 'Athletics', 'Powerlifting', 'Muscle & Sculpting', 'Bodyweight Fitness', 'Fitness'], 
                    value=State.goal, on_change=State.set_goal
                ),
                width="100%"
            ),
            rx.box(
                rx.text("Equipment", weight="bold"),
                rx.select(
                    ['Machine', 'Dumbbell', 'Barbell', 'Bodyweight', 'All (Gym Mixed)'], 
                    value=State.equipment, on_change=State.set_equipment
                ),
                width="100%"
            ),
            direction="row",
            spacing="4",
            mb="4"
        ),
        rx.flex(
            rx.box(
                rx.text("Squat 1RM (kg)", weight="bold"),
                rx.input(value=State.squat, on_change=State.set_squat, type="number"),
                width="100%"
            ),
            rx.box(
                rx.text("Bench 1RM (kg)", weight="bold"),
                rx.input(value=State.bench, on_change=State.set_bench, type="number"),
                width="100%"
            ),
            rx.box(
                rx.text("Deadlift 1RM (kg)", weight="bold"),
                rx.input(value=State.deadlift, on_change=State.set_deadlift, type="number"),
                width="100%"
            ),
            direction="row",
            spacing="4"
        ),
        p="6",
        box_shadow="md",
        mb="6"
    )

def workout_builder():
    return rx.card(
        rx.heading("2. Build Workout", size="5", mb="4"),
        rx.cond(
            State.history_names.length() > 0,
            rx.box(
                rx.text("Current Workout Routine:", weight="bold", mb="2"),
                rx.foreach(
                    State.history_names,
                    lambda name, idx: rx.badge(name, color_scheme="blue", mr="2", mb="2", size="2")
                ),
                rx.cond(
                    State.current_prediction != "",
                    rx.callout(State.current_prediction, icon="info", color_scheme="green", mt="4", mb="4")
                ),
                rx.divider(mb="4", mt="4"),
                rx.text("Next Suggested Exercises:", weight="bold", mb="2"),
                rx.cond(
                    State.is_loading,
                    rx.spinner(),
                    rx.foreach(
                        State.recommendations,
                        lambda rec: rx.card(
                            rx.flex(
                                rx.box(
                                    rx.text(rec["exercise_name"], weight="bold"),
                                    rx.text(f"Match Score: {rec['final_score']} | Equipment: {rec['equipment']}", size="2", color="gray.500")
                                ),
                                rx.spacer(),
                                rx.button("Add", on_click=lambda: State.add_exercise(rec["exercise_id"], rec["exercise_name"], rec["equipment"]), size="2"),
                                align_items="center"
                            ),
                            mb="2",
                            _hover={"bg": "gray.50"}
                        )
                    )
                ),
                rx.button("Reset Workout", on_click=State.reset_workout, color_scheme="red", mt="4")
            ),
            rx.box(
                rx.text("Start your workout by choosing the first exercise. (Example IDs used for UI demo)"),
                # For demo purposes we can just have a button to start with Bench Press (id 324)
                rx.button("Start with Bench Press", on_click=lambda: State.start_workout(324, "Bench Press", "Barbell"), mt="2")
            )
        ),
        p="6",
        box_shadow="md"
    )

def index():
    return rx.container(
        hero_section(),
        profile_section(),
        workout_builder(),
        max_width="800px",
        margin_x="auto",
        padding_y="8"
    )

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="blue",
    )
)
app.add_page(index, title="Gym Brain")
