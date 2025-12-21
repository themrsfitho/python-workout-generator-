import json
import random
from typing import List
from models import Exercise, WorkoutDay, Program

# ---------------------------
# LOAD EXERCISE DATA
# ---------------------------
def load_exercises() -> List[Exercise]:
    with open("data/base_exercises.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return [
        Exercise(
            name=item["name"],
            muscle_group=item["muscle_group"],
            equipment=item["equipment"],
            sets=0,
            reps="0",
            difficulty=item["difficulty"],
        )
        for item in data
    ]


# ---------------------------
# FILTERING FUNCTIONS
# ---------------------------
def filter_by_muscle(exercises: List[Exercise], muscle: str) -> List[Exercise]:
    return [ex for ex in exercises if ex.muscle_group.lower() == muscle.lower()]

def filter_by_level(exercises: List[Exercise], level: str) -> List[Exercise]:
    level_lower = level.lower()
    if level_lower == "beginner":
        allowed = ["Beginner", "All"]
    elif level_lower == "intermediate":
        allowed = ["Beginner", "Intermediate", "All"]
    else:  # advanced
        allowed = ["Beginner", "Intermediate", "Advanced", "All"]
    return [ex for ex in exercises if ex.difficulty in allowed]

def filter_for_home_gym(exercises: List[Exercise]) -> List[Exercise]:
    allowed_keywords = ["dumbbells", "barbell"]
    return [ex for ex in exercises if any(kw in ex.equipment.lower() for kw in allowed_keywords)]


# ---------------------------
# RANDOM PICK
# ---------------------------
def pick(exercises: List[Exercise]) -> Exercise:
    if not exercises:
        raise ValueError("No exercises available")
    return random.choice(exercises)


# ---------------------------
# APPLY GOAL SETS/REPS (UPDATED)
# ---------------------------
def apply_goal_sets_reps(exercise: Exercise, goal: str) -> None:
    goal_lower = goal.lower()
    
    if goal_lower == "fat loss" or goal_lower == "endurance":
        exercise.sets = 3
        exercise.reps = "12-20"
    elif goal_lower == "muscle gain" or goal_lower == "hypertrophy":
        exercise.sets = 4
        exercise.reps = "8-12"
    else:  # Strength (default)
        exercise.sets = 5
        exercise.reps = "3-5"


# ---------------------------
# BUILD DAY
# ---------------------------
def build_day(
    day_name: str,
    focus: str,
    muscles: List[str],
    all_exercises: List[Exercise],
    level: str,
    goal: str,
    home_gym_only: bool,
) -> WorkoutDay:
    day_exercises: List[Exercise] = []
    usable_exercises = all_exercises
    if home_gym_only:
        usable_exercises = filter_for_home_gym(usable_exercises)

    for muscle in muscles:
        muscle_exs = filter_by_muscle(usable_exercises, muscle)
        level_exs = filter_by_level(muscle_exs, level)
        if not level_exs:
            level_exs = muscle_exs
        if not level_exs:
            continue
        ex = pick(level_exs)
        apply_goal_sets_reps(ex, goal)
        day_exercises.append(ex)

    return WorkoutDay(name=day_name, focus=focus, exercises=day_exercises)


# ---------------------------
# GENERATE PROGRAM (UPDATED)
# ---------------------------
def generate_program(
    goal: str,
    experience_level: str,
    days_per_week: int,
    client_name: str = "Client",
    home_gym_only: bool = False,
) -> Program:
    # UPDATED: Added the goals your app actually uses
    VALID_GOALS = ["strength", "muscle gain", "fat loss", "hypertrophy", "endurance"]
    VALID_LEVELS = ["beginner", "intermediate", "advanced"]
    
    # Make comparison case-insensitive
    goal_lower = goal.lower()
    level_lower = experience_level.lower()
    
    if goal_lower not in VALID_GOALS:
        # Try to map common variations
        goal_mapping = {
            "gain": "muscle gain",
            "muscle": "muscle gain",
            "weight loss": "fat loss",
            "fat": "fat loss",
            "power": "strength"
        }
        goal_lower = goal_mapping.get(goal_lower, goal_lower)
        
        if goal_lower not in VALID_GOALS:
            raise ValueError(f"Invalid goal: {goal}. Valid options: {', '.join(VALID_GOALS)}")
    
    if level_lower not in VALID_LEVELS:
        raise ValueError(f"Invalid experience level: {experience_level}")
    
    if days_per_week < 1:
        raise ValueError("days_per_week must be >= 1")

    all_exercises = load_exercises()
    days: List[WorkoutDay] = []

    # --- Simple split logic ---
    for i in range(days_per_week):
        day_name = f"Day {i+1}"
        muscles = ["Chest", "Back", "Legs", "Shoulders", "Biceps", "Triceps"]
        day = build_day(
            day_name=day_name,
            focus=f"{goal_lower} - {level_lower}",
            muscles=muscles,
            all_exercises=all_exercises,
            level=level_lower,
            goal=goal_lower,
            home_gym_only=home_gym_only,
        )
        days.append(day)

    program = Program(
        goal=goal_lower.title(),  # Format nicely: "muscle gain" -> "Muscle Gain"
        experience_level=level_lower.title(),
        days=len(days),
        client_name=client_name,
        home_gym_only=home_gym_only,
        days_list=days,
    )
    return program