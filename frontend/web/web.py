import reflex as rx
import httpx
from typing import List, Dict, Any

# Custom Glassmorphism Style
glass_style = {
    "bg": "rgba(255, 255, 255, 0.05)",
    "backdrop_filter": "blur(16px)",
    "-webkit-backdrop-filter": "blur(16px)",
    "border": "1px solid rgba(255, 255, 255, 0.15)",
    "border_radius": "xl",
    "box_shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 1px 1px rgba(255,255,255,0.1)",
    "padding": "2rem",
}

class State(rx.State):
    # App State
    current_step: int = 1
    
    # Profile State
    level: str = "Intermediate"
    goal: str = "Bodybuilding"
    sex: str = "Male"
    age: str = "25"
    bw: str = "80"
    equipment: str = "All (Gym Mixed)"
    
    # Powerlifting Stats (SBD)
    squat: str = "0"
    bench: str = "0"
    deadlift: str = "0"

    def set_level(self, val: str): self.level = val
    def set_goal(self, val: str): self.goal = val
    def set_sex(self, val: str): self.sex = val
    def set_equipment(self, val: str): self.equipment = val
    def set_squat(self, val: str): self.squat = val
    def set_bench(self, val: str): self.bench = val
    def set_deadlift(self, val: str): self.deadlift = val
    def set_age(self, val: str): self.age = val
    def set_bw(self, val: str): self.bw = val
    
    def next_step(self):
        if self.current_step < 4:
            self.current_step += 1
            
    def prev_step(self):
        if self.current_step > 1:
            self.current_step -= 1

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
                    self.current_prediction = f"Optimal Target: {weight} kg x {reps} reps"
        except Exception as e:
            print(e)
            
        await self.get_recommendations()

    async def start_workout(self, first_ex_id: int, first_ex_name: str, raw_eq: str):
        self.history_ids = []
        self.history_names = []
        self.next_step()  # Move to step 4 (Workspace)
        await self.add_exercise(first_ex_id, first_ex_name, raw_eq)

    def reset_workout(self):
        self.history_ids = []
        self.history_names = []
        self.recommendations = []
        self.current_prediction = ""
        self.current_step = 1


def hero_section():
    return rx.box(
        rx.flex(
            rx.heading(
                "Gym Brain AI", 
                size="9", 
                weight="bold", 
                background_image="linear-gradient(270deg, #00f2fe, #4facfe)",
                background_clip="text",
                color="transparent",
                mb="2"
            ),
            rx.text(
                "Hyper-Personalized Fitness Intelligence", 
                size="4", 
                color="gray.300", 
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
        box_shadow="0 0 40px -10px rgba(79, 172, 254, 0.3)",
    )

def step_1_bio():
    return rx.box(
        rx.heading("Step 1: Biological Profile", size="6", color="white", mb="6"),
        rx.grid(
            rx.box(
                rx.text("Level", size="3", color="gray.200", mb="2", weight="medium"),
                rx.select(
                    ["Novice", "Beginner", "Intermediate", "Advanced"], 
                    value=State.level, on_change=State.set_level,
                    variant="soft", color_scheme="gray", size="3"
                ),
            ),
            rx.box(
                rx.text("Goal", size="3", color="gray.200", mb="2", weight="medium"),
                rx.select(
                    ['Powerbuilding', 'Bodybuilding', 'Athletics', 'Powerlifting', 'Muscle & Sculpting', 'Bodyweight Fitness', 'Fitness'], 
                    value=State.goal, on_change=State.set_goal,
                    variant="soft", color_scheme="gray", size="3"
                ),
            ),
            rx.box(
                rx.text("Sex", size="3", color="gray.200", mb="2", weight="medium"),
                rx.select(
                    ['Male', 'Female'], 
                    value=State.sex, on_change=State.set_sex,
                    variant="soft", color_scheme="gray", size="3"
                ),
            ),
            rx.box(
                rx.text("Age", size="3", color="gray.200", mb="2", weight="medium"),
                rx.input(value=State.age, on_change=State.set_age, type="number", variant="soft", color_scheme="gray", size="3"),
            ),
            rx.box(
                rx.text("Bodyweight (kg)", size="3", color="gray.200", mb="2", weight="medium"),
                rx.input(value=State.bw, on_change=State.set_bw, type="number", variant="soft", color_scheme="gray", size="3"),
            ),
            columns="2",
            spacing="6",
        ),
        rx.flex(
            rx.spacer(),
            rx.button("Next Step", on_click=State.next_step, size="4", color_scheme="cyan", mt="8"),
            width="100%"
        ),
        style=glass_style,
        mb="8"
    )

def step_2_stats():
    return rx.box(
        rx.heading("Step 2: Equipment & Base Strength", size="6", color="white", mb="6"),
        rx.grid(
            rx.box(
                rx.text("Available Equipment", size="3", color="gray.200", mb="2", weight="medium"),
                rx.select(
                    ['Machine', 'Dumbbell', 'Barbell', 'Bodyweight', 'All (Gym Mixed)'], 
                    value=State.equipment, on_change=State.set_equipment,
                    variant="soft", color_scheme="gray", size="3"
                ),
            ),
            rx.box(
                rx.text("Squat 1RM (kg)", size="3", color="gray.200", mb="2", weight="medium"),
                rx.input(value=State.squat, on_change=State.set_squat, type="number", variant="soft", color_scheme="gray", size="3"),
            ),
            rx.box(
                rx.text("Bench 1RM (kg)", size="3", color="gray.200", mb="2", weight="medium"),
                rx.input(value=State.bench, on_change=State.set_bench, type="number", variant="soft", color_scheme="gray", size="3"),
            ),
            rx.box(
                rx.text("Deadlift 1RM (kg)", size="3", color="gray.200", mb="2", weight="medium"),
                rx.input(value=State.deadlift, on_change=State.set_deadlift, type="number", variant="soft", color_scheme="gray", size="3"),
            ),
            columns="2",
            spacing="6",
        ),
        rx.flex(
            rx.button("Back", on_click=State.prev_step, size="4", variant="soft", color_scheme="gray", mt="8"),
            rx.spacer(),
            rx.button("Review Profile", on_click=State.next_step, size="4", color_scheme="cyan", mt="8"),
            width="100%"
        ),
        style=glass_style,
        mb="8"
    )

def step_3_summary():
    return rx.box(
        rx.heading("Step 3: Neural Initialization", size="6", color="white", mb="6"),
        rx.text("Please confirm your parameters before the AI generates your dynamic workout trajectory.", color="gray.300", mb="6", size="3"),
        
        rx.box(
            rx.grid(
                rx.text("Profile:", weight="bold", color="cyan.200"),
                rx.text(f"{State.sex}, {State.age} yrs, {State.bw} kg", color="white"),
                rx.text("Goal / Level:", weight="bold", color="cyan.200"),
                rx.text(f"{State.goal} ({State.level})", color="white"),
                rx.text("Equipment:", weight="bold", color="cyan.200"),
                rx.text(State.equipment, color="white"),
                rx.text("Strength (S/B/D):", weight="bold", color="cyan.200"),
                rx.text(f"{State.squat} / {State.bench} / {State.deadlift} kg", color="white"),
                columns="2",
                spacing="4",
                p="6",
                bg="rgba(0, 0, 0, 0.3)",
                border_radius="md",
                border="1px solid rgba(255,255,255,0.1)"
            ),
            mb="8"
        ),
        
        rx.heading("Initialize Seed Exercise", size="4", color="white", mb="4"),
        rx.grid(
            rx.button(
                "Initialize with Bench Press", 
                on_click=lambda: State.start_workout(324, "Bench Press", "Barbell"), 
                size="4", color_scheme="cyan", box_shadow="0 0 20px -3px rgba(6, 182, 212, 0.5)", _hover={"transform": "scale(1.02)"}
            ),
            rx.button(
                "Initialize with Squat", 
                on_click=lambda: State.start_workout(340, "Barbell Squat", "Barbell"), 
                size="4", color_scheme="indigo", box_shadow="0 0 20px -3px rgba(99, 102, 241, 0.5)", _hover={"transform": "scale(1.02)"}
            ),
            columns="2",
            spacing="4"
        ),
        rx.flex(
            rx.button("Edit Settings", on_click=State.prev_step, size="3", variant="soft", color_scheme="gray", mt="8"),
        ),
        style=glass_style,
        mb="8"
    )

def recommendation_card(rec):
    return rx.box(
        rx.flex(
            rx.box(
                rx.text(rec["exercise_name"], weight="bold", size="4", color="white"),
                rx.flex(
                    rx.badge(rec["equipment"], color_scheme="indigo", variant="soft", size="2", mr="2"),
                    rx.badge(f"Match Score: {rec['final_score']}", color_scheme="cyan", variant="surface", size="2"),
                    mt="3"
                )
            ),
            rx.spacer(),
            rx.button(
                rx.icon(tag="plus", size=20),
                "Add to Routine",
                on_click=lambda: State.add_exercise(rec["exercise_id"], rec["exercise_name"], rec["equipment"]),
                size="3",
                color_scheme="cyan",
                variant="solid",
                box_shadow="0 0 15px -3px rgba(6, 182, 212, 0.4)",
                _hover={"transform": "scale(1.05)", "box_shadow": "0 0 20px 0px rgba(6, 182, 212, 0.6)"}
            ),
            align_items="center"
        ),
        p="5",
        mb="4",
        border_radius="lg",
        bg="rgba(255, 255, 255, 0.05)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        _hover={"bg": "rgba(255, 255, 255, 0.08)", "border": "1px solid rgba(6, 182, 212, 0.5)"},
        transition="all 0.2s ease"
    )

def step_4_workspace():
    return rx.box(
        rx.flex(
            # Left Column: Trajectory
            rx.box(
                rx.heading("Current Trajectory", size="5", color="white", mb="4"),
                rx.flex(
                    rx.foreach(
                        State.history_names,
                        lambda name: rx.badge(
                            name, 
                            color_scheme="cyan", 
                            variant="outline", 
                            mr="2", mb="2", size="3",
                            border_color="rgba(6, 182, 212, 0.6)",
                            color="cyan.100"
                        )
                    ),
                    wrap="wrap"
                ),
                rx.cond(
                    State.current_prediction != "",
                    rx.box(
                        rx.text("AI Target Prediction", size="2", color="cyan.200", mb="1"),
                        rx.text(State.current_prediction, weight="bold", size="5", color="white"),
                        p="5",
                        mt="6",
                        border_radius="md",
                        bg="rgba(6, 182, 212, 0.15)",
                        border_left="4px solid #06b6d4"
                    )
                ),
                rx.button(
                    rx.icon(tag="rotate-ccw", mr="2"),
                    "End & Reset Workout", 
                    on_click=State.reset_workout, 
                    color_scheme="red", 
                    variant="soft",
                    mt="8",
                    size="3",
                    width="100%"
                ),
                width=["100%", "100%", "35%"],
                p="4",
            ),
            
            # Right Column: AI Recommendations
            rx.box(
                rx.heading("AI Next Step Generation", size="5", color="white", mb="4"),
                rx.cond(
                    State.is_loading,
                    rx.flex(rx.spinner(color="cyan", size="3"), justify="center", p="10"),
                    rx.box(
                        rx.foreach(
                            State.recommendations,
                            recommendation_card
                        ),
                        max_height="600px",
                        overflow_y="auto",
                        pr="2"
                    )
                ),
                width=["100%", "100%", "65%"],
                p="4",
                border_left=["none", "none", "1px solid rgba(255,255,255,0.1)"]
            ),
            direction=["column", "column", "row"],
            spacing="6",
            align_items="flex-start"
        ),
        style=glass_style,
        mb="8"
    )

def index():
    return rx.box(
        rx.container(
            hero_section(),
            rx.match(
                State.current_step,
                (1, step_1_bio()),
                (2, step_2_stats()),
                (3, step_3_summary()),
                (4, step_4_workspace()),
                step_1_bio()
            ),
            # Increase max width depending on the step
            max_width=rx.cond(State.current_step == 4, "1200px", "800px"),
            margin_x="auto",
            padding_y="10",
            transition="max-width 0.4s ease-in-out"
        ),
        bg="radial-gradient(circle at top center, #1e1b4b, #050505 80%)",
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
