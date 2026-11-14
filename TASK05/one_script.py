from pathlib import Path


def read_attendance(path):
    rows = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            reg_no, date_value, status = line.split(",")
            rows.append((reg_no, date_value, status))
    return rows


def compute_counts(rows):
    stats = {}
    for reg_no, _, status in rows:
        if reg_no not in stats:
            stats[reg_no] = {"present": 0, "absent": 0}
        if status == "P":
            stats[reg_no]["present"] += 1
        elif status == "A":
            stats[reg_no]["absent"] += 1
    return stats


def write_report(stats, out_path):
    lines = ["Register Number,Present,Absent,Percentage"]
    for reg_no in sorted(stats):
        present = stats[reg_no]["present"]
        absent = stats[reg_no]["absent"]
        total = present + absent
        pct = (present / total) * 100 if total else 0.0
        lines.append(f"{reg_no},{present},{absent},{pct:.2f}%")
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    input_path = Path(__file__).with_name("attendance_sample.txt")
    output_path = Path(__file__).with_name("attendance_summary.txt")
    rows = read_attendance(input_path)
    stats = compute_counts(rows)
    write_report(stats, output_path)
    print(f"Processed {len(rows)} attendance records.")
    print(output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
