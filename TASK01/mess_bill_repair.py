from decimal import Decimal, InvalidOperation
from pathlib import Path


def diagnose_issues():
    return [
        "Hard-coded file path prevents the script from running on other computers or folders.",
        "The file is never closed after reading, leaving the handle open and leaking resources.",
        "Reading the whole file into memory uses too much memory for large files.",
        "A bare except hides every error and makes debugging impossible.",
        "Using int() discards paise values such as 1250.50.",
        "Repeated string concatenation in a loop is inefficient for large reports.",
        "A blank final line may be processed and create invalid data.",
        "Rejected lines are not recorded, so the office cannot trace what was skipped."
    ]


def repair_mess_file(file_name):
    """Read a mess-bill file, sum valid amounts, and log rejected lines."""
    total = Decimal("0.00")
    report_lines = []
    rejected = []

    with open(file_name, "r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line:
                continue

            try:
                parts = [part.strip() for part in line.split(",")]
                if len(parts) != 3:
                    raise ValueError("Expected 3 comma-separated fields.")

                register_number, student_name, amount_text = parts
                if not register_number or not student_name:
                    raise ValueError("Register number or name is missing.")

                amount = Decimal(amount_text)
                if amount < 0:
                    raise ValueError("Amount cannot be negative.")
            except (ValueError, InvalidOperation) as exc:
                reason = "Invalid numeric value." if isinstance(exc, InvalidOperation) else str(exc)
                rejected.append((line_number, raw_line.rstrip("\n"), reason))
                continue

            total += amount
            report_lines.append(f"{register_number},{student_name},{amount.quantize(Decimal('0.01'))}")

    return report_lines, total, rejected


def main():
    print("Task 1: Diagnosing and repairing the poor script")
    print("\nDesign deficiencies:")
    for index, issue in enumerate(diagnose_issues(), start=1):
        print(f"{index}. {issue}")

    sample_file = Path(__file__).with_name("mess_oct.txt")
    report_lines, total, rejected = repair_mess_file(sample_file)

    print("\nMess bill report:")
    for row in report_lines:
        print(row)

    print(f"\nTotal mess bill: {total.quantize(Decimal('0.01'))}")

    if rejected:
        print("\nRejected lines:")
        for line_number, raw_line, reason in rejected:
            print(f"Line {line_number}: {raw_line} -> {reason}")
    else:
        print("\nNo rejected lines.")


if __name__ == "__main__":
    main()
