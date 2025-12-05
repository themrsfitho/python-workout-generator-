# models.py

class Exercise:
    def __init__(self, name, muscle_group, equipment, sets=0, reps="0", difficulty="Beginner"):
        self.name = name
        self.muscle_group = muscle_group
        self.equipment = equipment
        self.sets = sets
        self.reps = reps
        self.difficulty = difficulty


class WorkoutDay:
    def __init__(self, name, focus, exercises=None):
        self.name = name
        self.focus = focus
        self.exercises = exercises if exercises is not None else []


class Program:
    def __init__(self, goal, experience_level, days, client_name="Client", home_gym_only=False, days_list=None):
        self.goal = goal
        self.experience_level = experience_level
        self.days = days_list if days_list is not None else []
        self.client_name = client_name
        self.home_gym_only = home_gym_only
