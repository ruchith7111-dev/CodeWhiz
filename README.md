# CodeWhiz - Coding Habit Monitor

A Python console application to record, track and review daily coding practice.
Each coding session stores its date, language, category, hours and notes. Data persists in a JSON file across runs.

## Features

- Add, view, update and delete coding sessions
- Filter sessions by category or programming language
- Summary report with total hours and category-wise effort
- Persistent storage in `codewhiz_data.json`
- Graceful handling of missing or corrupted data files and invalid input

## Project Structure

```
CodeWhiz/
├── main.py                 # Menu controller (entry point)
├── habit_manager.py        # Core operations: add, update, delete, filter
├── data_store.py           # JSON load/save layer
├── reports.py              # Table and summary reports
├── test_habit_manager.py   # Unit tests
└── README.md
```

## Requirements

- Python 3.11 or higher
- Standard library only (no external packages)

## Usage

```bash
python main.py
```

Choose an option from the menu. Data is saved when you select option 7 (Save and exit).

## Running Tests

```bash
python -m unittest -v
```

## Categories

`DSA`, `Web`, `AI/ML`, `Debugging`, `Projects`, `Other` (defined in `habit_manager.py`).

## Future Scope

- Tkinter GUI or Flask web dashboard
- Weekly goals and progress charts
- Migration from JSON to SQLite
