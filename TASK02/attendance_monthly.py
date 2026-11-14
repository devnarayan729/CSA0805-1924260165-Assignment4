from pathlib import Path


def parse_attendance_line(line, file_name, line_number):
    """Return (register_number, date, status) for a valid record or raise ValueError."""
    parts = [part.strip() for part in line.split(",")]
    if len(parts) != 3:
        raise ValueError(f"Expected 3 comma-separated fields, got {len(parts)}")

    reg_number, date_value, status = parts
    if not reg_number or not date_value or not status:
        raise ValueError("Register number, date, or status is missing.")
    if status.upper() not in {"P", "A"}:
        raise ValueError(f"Status must be P or A, got {status!r}.")

    return reg_number, date_value, status.upper()


def process_monthly_attendance(folder):
    """Read all daily files in a folder and accumulate attendance statistics."""
    stats = {}
    damaged_lines = []

    for file_path in sorted(Path(folder).glob("attendance_*.txt")):
        with open(file_path, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    reg_number, date_value, status = parse_attendance_line(line, file_path.name, line_number)
                except ValueError as exc:
                    damaged_lines.append((file_path.name, line_number, str(exc), line))
                    continue

                student = stats.setdefault(reg_number, {"present": 0, "absent": 0})
                if status == "P":
                    student["present"] += 1
                else:
                    student["absent"] += 1

    summary_lines = ["Register Number,Present,Absent,Total,Percentage"]
    below_75 = []
    for reg_number in sorted(stats):
        present = stats[reg_number]["present"]
        absent = stats[reg_number]["absent"]
        total = present + absent
        percentage = (present / total) * 100 if total else 0.0
        summary_lines.append(f"{reg_number},{present},{absent},{total},{percentage:.2f}%")
        if percentage < 75:
            below_75.append(f"{reg_number},{percentage:.2f}%")

    summary_path = Path(folder) / "monthly_attendance_summary.txt"
    below_75_path = Path(folder) / "students_below_75.txt"
    damaged_path = Path(folder) / "damaged_lines.log"

    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    below_75_path.write_text("Register Number,Percentage\n" + ("\n".join(below_75) if below_75 else "") + ("\n" if below_75 else ""), encoding="utf-8")
    damaged_path.write_text(
        "File Name,Line Number,Reason,Record\n" + "\n".join(
            f"{file_name},{line_number},{reason},{record}" for file_name, line_number, reason, record in damaged_lines
        ) + ("\n" if damaged_lines else ""),
        encoding="utf-8",
    )

    return stats, damaged_lines


def main():
    data_folder = Path(__file__).resolve().parent
    stats, damaged_lines = process_monthly_attendance(data_folder)

    print("Task 2: Monthly attendance summary")
    print("\nSummary of processed students:")
    for reg_number in sorted(stats):
        present = stats[reg_number]["present"]
        absent = stats[reg_number]["absent"]
        total = present + absent
        percentage = (present / total) * 100 if total else 0.0
        print(f"{reg_number}: present={present}, absent={absent}, total={total}, percentage={percentage:.2f}%")

    print("\nDamaged records:")
    if damaged_lines:
        for file_name, line_number, reason, record in damaged_lines:
            print(f"{file_name}:{line_number} -> {reason} | {record}")
    else:
        print("No damaged records found.")


if __name__ == "__main__":
    main()
