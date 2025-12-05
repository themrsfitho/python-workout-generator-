import sys
import os
import pytest

# --- Fix Python path for Windows so imports work ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workout_generator import generate_program
from models import Program, WorkoutDay, Exercise

# --- Helper for home gym check ---
HOME_GYM_KEYWORDS = ["dumbbells", "barbell"]

def exercises_home_gym_only(exercises):
    """Return True if all exercises are home-gym compatible."""
    for ex in exercises:
        if not any(kw in ex.equipment.lower() for kw in HOME_GYM_KEYWORDS):
            return False
    return True

# --- Basic return type ---
def test_generate_program_returns_program():
    program = generate_program("strength", "beginner", 3)
    assert isinstance(program, Program)
    assert isinstance(program.days, list)
    assert all(isinstance(day, WorkoutDay) for day in program.days)

# --- Optional arguments ---
def test_generate_program_custom_client_name():
    program = generate_program("strength", "beginner", 3, client_name="Evie")
    assert program.client_name == "Evie"

def test_generate_program_home_gym_only_flag():
    program = generate_program("strength", "beginner", 3, home_gym_only=True)
    # Ensure all exercises in all days use home-gym equipment
    for day in program.days:
        assert exercises_home_gym_only(day.exercises)

# --- Days per week ---
def test_generate_program_days_per_week():
    for days in range(1, 7):
        program = generate_program("strength", "beginner", days)
        assert len(program.days) == days
        for day in program.days:
            assert isinstance(day.exercises, list)
            assert len(day.exercises) > 0  # each day has exercises

# --- Valid goals ---
@pytest.mark.parametrize("goal", ["strength", "hypertrophy", "endurance"])
def test_generate_program_valid_goals(goal):
    program = generate_program(goal, "beginner", 3)
    assert program.goal == goal

# --- Valid experience levels ---
@pytest.mark.parametrize("level", ["beginner", "intermediate", "advanced"])
def test_generate_program_experience_levels(level):
    program = generate_program("strength", level, 3)
    assert program.experience_level == level

# --- Invalid inputs ---
def test_generate_program_invalid_goal():
    with pytest.raises(ValueError):
        generate_program("unknown_goal", "beginner", 3)

def test_generate_program_invalid_experience_level():
    with pytest.raises(ValueError):
        generate_program("strength", "expert", 3)

def test_generate_program_invalid_days():
    with pytest.raises(ValueError):
        generate_program("strength", "beginner", 0)
