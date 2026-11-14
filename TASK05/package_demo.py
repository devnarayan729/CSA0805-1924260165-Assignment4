from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from package import read_attendance, compute_counts, write_report


def main():
    input_path = Path(__file__).with_name("attendance_sample.txt")
    output_path = Path(__file__).with_name("attendance_package_summary.txt")
    rows = read_attendance(input_path)
    stats = compute_counts(rows)
    write_report(stats, output_path)
    print(output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
