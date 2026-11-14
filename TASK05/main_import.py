from pathlib import Path
from attendance_utils import compute_counts, read_attendance


def main():
    rows = read_attendance(Path(__file__).with_name("attendance_sample.txt"))
    stats = compute_counts(rows)
    for reg_no in sorted(stats):
        present = stats[reg_no]["present"]
        absent = stats[reg_no]["absent"]
        total = present + absent
        pct = (present / total) * 100 if total else 0.0
        print(f"{reg_no}: {present} present, {absent} absent, {pct:.2f}%")


if __name__ == "__main__":
    main()
