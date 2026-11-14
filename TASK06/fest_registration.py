import re
from pathlib import Path

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def parse_registrations(file_path):
    seen = set()
    valid = []
    rejected = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line:
                continue

            parts = [part.strip() for part in line.split(",")]
            if len(parts) != 5:
                rejected.append((line_number, "Wrong field count", line))
                continue

            reg_no, name, department, email, chosen_events = parts
            if reg_no in seen:
                rejected.append((line_number, "Duplicate registration", line))
                continue
            if not EMAIL_RE.fullmatch(email):
                rejected.append((line_number, " Invalid email address", line))
                continue

            seen.add(reg_no)
            valid.append((reg_no, name, department, email, chosen_events))

    return valid, rejected


def main():
    file_path = Path(__file__).with_name("fest_registrations.txt")
    valid, rejected = parse_registrations(file_path)

    print("Valid registrations:")
    for item in valid:
        print(item)

    print("\nRejected registrations:")
    for line_no, reason, record in rejected:
        print(f"Line {line_no}: {reason} | {record}")


if __name__ == "__main__":
    main()
