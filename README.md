# Workout Program Generator (Home & Gym)

A Python command-line app that generates structured workout programs based on:

- Training goal (Fat Loss, Muscle Gain, Strength)
- Experience level (Beginner, Intermediate, Advanced)
- Days per week (3–6)
- Equipment access (Home gym only vs Full gym)

It uses a JSON exercise database, applies simple programming rules (splits, sets, reps), and lets you export the final program as a `.txt` file you can share with a client or keep for yourself.

---

## Features

- **Goal-based programming**
  - Fat Loss, Muscle Gain, Strength
  - Automatically adjusts sets and rep ranges per goal

- **Experience-aware**
  - Beginner, Intermediate, Advanced
  - Filters exercises by difficulty so beginners don’t get thrown into advanced work

- **Flexible training splits**
  - 3 days → Full Body x3  
  - 4 days → Upper / Lower x2  
  - 5 days → Push / Pull / Legs + extras  
  - 6 days → Push / Pull / Legs x2  

- **Home gym mode**
  - Option to generate a program using **only dumbbells/barbell–friendly exercises**
  - Skips machine-only / cable-only movements when “Home gym only” is selected

- **JSON-driven exercise database**
  - Exercises stored in `data/base_exercises.json`
  - Easy to extend with more exercises, muscle groups, or equipment tags

- **Clean CLI experience**
  - Simple menu:
    - Create new program
    - View current program
    - Save program to file
  - Input validated for common mistakes (bad menu choices, days outside 3–6)

- **Export to text file**
  - Saves the generated program as `program_<client_name>.txt`
  - Includes:
    - Client name
    - Goal
    - Experience level
    - Days/week
    - Gym mode (Home vs Full)
    - Exercises grouped by day

---

## Tech Stack

- **Language:** Python 3
- **Paradigm:** Object-Oriented (dataclasses)
- **Data storage:** JSON (`data/base_exercises.json`)
- **Interface:** Command Line Interface (CLI)
- **File output:** Plain text `.txt` files

---

## Project Structure

```text
Evies-Projects/
├── main.py                # CLI entrypoint (menu, printing, export)
├── generator.py           # Program generation logic
├── models.py              # Dataclasses: Exercise, WorkoutDay, Program
├── data/
│   └── base_exercises.json  # Exercise database
└── program_<name>.txt     # Example exported programs (generated)
