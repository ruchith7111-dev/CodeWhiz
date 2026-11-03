"""Display and summary reports for coding session records."""


def summary(entries):
    total = sum(e["hours"] for e in entries)
    per_category = {}
    for e in entries:
        per_category[e["category"]] = per_category.get(e["category"], 0) + e["hours"]
    return total, per_category


def print_report(entries):
    total, per_category = summary(entries)
    print(f"Total sessions : {len(entries)}")
    print(f"Total hours    : {total:.2f}")
    for cat, hrs in sorted(per_category.items(), key=lambda x: -x[1]):
        print(f"  {cat:<12} {hrs:>6.2f} h")


def print_table(entries):
    if not entries:
        print("No sessions recorded.")
        return
    print(f"{'ID':<5}{'Date':<12}{'Language':<12}{'Category':<12}{'Hours':>6}  Notes")
    for e in entries:
        print(f"{e['id']:<5}{e['date']:<12}{e['language']:<12}"
              f"{e['category']:<12}{e['hours']:>6.2f}  {e['notes']}")
