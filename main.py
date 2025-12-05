from typing import Optional
from pathlib import Path

from generator import generate_program
from models import Program

# Track current program + whether it's home-gym-only
current_program: Optional[Program] = None
current_home_gym_only: bool = False


# ---------------------------
# FORMATTING HELPERS
# ---------------------------

def program_to_text(program: Program, home_gym_only: bool = False) -> str:
    """Return a nicely formatted string representation of a Program."""
    lines: list[str] = []

    gym_mode = "Home gym only (no machines)" if home_gym_only else "Full gym (machines allowed)"

    lines.append("=" * 40)
    lines.append(f"Program for: {program.client_name}")
    lines.append(f"Goal       : {program.goal}")
    lines.append(f"Level      : {program.experience_level}")
    lines.append(f"Days/week  : {program.days_per_week}")
    lines.append(f"Gym mode   : {gym_mode}")
    lines.append("=" * 40)

    for day in program.days:
        lines.append("")
        lines.append(f"=== {day.name} ({day.focus}) ===")

        if not day.exercises:
            lines.append("  No exercises generated for this day.")
            continue

        for idx, ex in enumerate(day.exercises, start=1):
            lines.append(f"    {idx}. {ex.name}")
            lines.append(f"       Muscle group : {ex.muscle_group}")
            lines.append(f"       Equipment    : {ex.equipment}")
            lines.append(f"       Sets x Reps  : {ex.sets} x {ex.reps}")
            lines.append("")

    return "\n".join(lines)


def print_program(program: Program, home_gym_only: bool) -> None:
    """Print the program to the console."""
    print("\n" + program_to_text(program, home_gym_only) + "\n")


def export_program_to_txt(program: Program, home_gym_only: bool, filename: Optional[str] = None) -> Path:
    """
    Save the program to a .txt file and return the path.
    If filename is not given, create one from the client name.
    """
    if not filename:
        safe_name = program.client_name.strip().replace(" ", "_")
        if not safe_name:
            safe_name = "client"
        filename = f"program_{safe_name}.txt"

    path = Path(filename)
    content = program_to_text(program, home_gym_only)
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------
# INPUT HELPERS
# ---------------------------

def ask_goal() -> str:
    options = ["Fat Loss", "Muscle Gain", "Strength"]
    print("\nChoose goal:")
    for i, g in enumerate(options, start=1):
        print(f"{i}. {g}")
    while True:
        choice = input("> ").strip()
        if choice in {"1", "2", "3"}:
            return options[int(choice) - 1]
        print("Please enter 1, 2, or 3.")


def ask_experience() -> str:
    options = ["Beginner", "Intermediate", "Advanced"]
    print("\nChoose experience level:")
    for i, lvl in enumerate(options, start=1):
        print(f"{i}. {lvl}")
    while True:
        choice = input("> ").strip()
        if choice in {"1", "2", "3"}:
            return options[int(choice) - 1]
        print("Please enter 1, 2, or 3.")


def ask_days_per_week() -> int:
    print("\nHow many days per week? (3–6)")
    while True:
        text = input("> ").strip()
        if text.isdigit():
            n = int(text)
            if 3 <= n <= 6:
                return n
        print("Please enter a number between 3 and 6.")


def ask_home_gym_only() -> bool:
    print("\nIs this for a home gym only? (no commercial machines)")
    print("1. Yes - home gym only")
    print("2. No  - full gym access")
    while True:
        choice = input("> ").strip()
        if choice == "1":
            return True
        if choice == "2":
            return False
        print("Please enter 1 or 2.")


# ---------------------------
# MAIN MENU
# ---------------------------

def main() -> None:
    global current_program, current_home_gym_only

    while True:
        print("\n=== Workout Program Generator ===")
        print("1. Create new program")
        print("2. View current program")
        print("3. Save current program to file")
        print("4. Exit")

        choice = input("> ").strip()

        if choice == "1":
            client_name = input("\nClient name: ").strip() or "Client"
            goal = ask_goal()
            level = ask_experience()
            days = ask_days_per_week()
            home_gym_only = ask_home_gym_only()

            try:
                current_program = generate_program(
                    goal=goal,
                    experience_level=level,
                    days_per_week=days,
                    client_name=client_name,
                    home_gym_only=home_gym_only,
                )
                current_home_gym_only = home_gym_only
                print("\n✅ New program generated!")
            except FileNotFoundError as e:
                print("\n❌ Error: could not load base exercises.")
                print(f"Details: {e}")
                current_program = None

        elif choice == "2":
            if current_program is None:
                print("\nNo program generated yet. Choose option 1 first.")
            else:
                print_program(current_program, current_home_gym_only)

        elif choice == "3":
            if current_program is None:
                print("\nNo program generated yet. Choose option 1 first.")
            else:
                path = export_program_to_txt(current_program, current_home_gym_only)
                print(f"\n💾 Program saved to: {path}")

        elif choice == "4":
            print("\nGoodbye!")
            break

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
