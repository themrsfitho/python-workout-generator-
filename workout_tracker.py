import os

workout_plan = []

print("=== Workout Plan Tracker ===")

def add_exercise():
    exercise = input("Enter an exercise (e.g., Leg Extensions 3x10): ")
    workout_plan.append(exercise)
    print("Exercise added!")

def remove_exercise():
    exercise = input("Enter the exact exercise to remove: ")
    if exercise in workout_plan:
        workout_plan.remove(exercise)
        print("Exercise removed!")
    else:
        print("That exercise is not in your plan.")

def save_plan():
    if not workout_plan:
        print("Workout plan is empty, nothing to save.")
        return
    with open("workout_plan.txt", "w", encoding="utf-8") as f:
        for exercise in workout_plan:
            f.write(exercise + "\n")
    print("Workout plan saved to workout_plan.txt")

def load_plan():
    if not os.path.exists("workout_plan.txt"):
        print("No saved workout plan found.")
        return 

    workout_plan.clear()

    with open("workout_plan.txt", "r", encoding="utf-8") as f:
        for line in f:
            exercise = line.strip()
            if exercise:
                workout_plan.append(exercise)

    print("Workout plan loaded!")

while True:
    print("\nChoose an option:")
    print("1. Add exercise")
    print("2. View workout plan")
    print("3. Remove exercise")
    print("4. Save workout plan")
    print("5. Load workout plan")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_exercise()
    elif choice == "2":
        print("\nYour workout plan:")
        if not workout_plan:
            print("- (empty)")
        else:
            for exercise in workout_plan:
                print("-", exercise)
    elif choice == "3":
        remove_exercise()
    elif choice == "4":
        save_plan()
    elif choice == "5":
        load_plan()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid option, try again.")
