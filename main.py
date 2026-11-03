"""CodeWhiz - Coding Habit Monitor: menu-driven console controller."""
from data_store import load_data, save_data
import habit_manager as hm
import reports

MENU = """
========= CodeWhiz - Coding Habit Monitor =========
1. Add coding session
2. View all sessions
3. Update session
4. Delete session
5. Filter sessions
6. Show summary report
7. Save and exit
"""


def read_float(prompt, allow_blank=False):
    while True:
        raw = input(prompt).strip()
        if allow_blank and raw == "":
            return None
        try:
            value = float(raw)
            if value < 0:
                print("Enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def read_id(prompt):
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            return int(raw)
        print("Please enter a valid session ID.")


def add_session(data):
    lang = input("Language: ").strip() or "Unknown"
    print(f"Categories: {', '.join(hm.CATEGORIES)}")
    cat = input("Category: ").strip() or "Other"
    hours = read_float("Hours spent: ")
    notes = input("Notes: ").strip()
    entry = hm.add_entry(data, lang, cat, hours, notes)
    print(f"Session #{entry['id']} added.")


def update_session(data):
    entry_id = read_id("Session ID to update: ")
    if hm.get_entry(data, entry_id) is None:
        print("Session not found.")
        return
    print("Leave a field blank to keep its current value.")
    lang = input("New language: ").strip()
    cat = input("New category: ").strip()
    hours = read_float("New hours: ", allow_blank=True)
    notes = input("New notes: ").strip()
    hm.update_entry(data, entry_id, language=lang, category=cat, hours=hours, notes=notes)
    print(f"Session #{entry_id} updated.")


def delete_session(data):
    entry_id = read_id("Session ID to delete: ")
    if hm.delete_entry(data, entry_id):
        print(f"Session #{entry_id} deleted.")
    else:
        print("Session not found.")


def filter_sessions(data):
    print("1. By category   2. By language")
    choice = input("Choose filter: ").strip()
    if choice == "1":
        print(f"Categories: {', '.join(hm.CATEGORIES)}")
        cat = input("Category: ").strip()
        reports.print_table(hm.filter_entries(data, category=cat))
    elif choice == "2":
        lang = input("Language: ").strip()
        reports.print_table(hm.filter_entries(data, language=lang))
    else:
        print("Invalid filter option.")


def main():
    data = load_data()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_session(data)
        elif choice == "2":
            reports.print_table(data["entries"])
        elif choice == "3":
            update_session(data)
        elif choice == "4":
            delete_session(data)
        elif choice == "5":
            filter_sessions(data)
        elif choice == "6":
            reports.print_report(data["entries"])
        elif choice == "7":
            save_data(data)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
