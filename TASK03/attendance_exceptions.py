class InvalidRecord(Exception):
    """Raised when a line of the attendance file is not in the expected format."""


def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
    parts = [part.strip() for part in line.strip().split(",")]
    if len(parts) != 3:
        raise InvalidRecord(f"Expected 3 values, found {len(parts)}: {line!r}")

    register_id, date_value, status = parts
    if status not in {"P", "A"}:
        raise InvalidRecord(f"Invalid status {status!r} for register {register_id!r}")

    return register_id, date_value, status


def summarise(path):
    present, absent, errors = 0, 0, []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as exc:
                    errors.append((line_number, str(exc)))
                    continue

                if status == "P":
                    present += 1
                else:
                    absent += 1
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Attendance file not found: {path}") from exc
    except PermissionError as exc:
        raise PermissionError(f"Permission denied when opening: {path}") from exc
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError("utf-8", b"", 0, 1, "Unable to decode attendance file in UTF-8 format") from exc
    else:
        print("Attendance summary generated successfully.")
    finally:
        print("Processing complete for attendance file.")

    return present, absent, errors


def misuse_experiment():
    """Illustrates why blind except Exception: pass hides real problems."""
    try:
        print("This will fail on purpose:")
        print(unknown_variable)
    except Exception:
        pass
    print("The program continues silently and does not show the real cause.")


def main():
    print("Task 3: Exception handling in the attendance processor")
    sample_path = "TASK03/attendance_sample.txt"
    try:
        present, absent, errors = summarise(sample_path)
        print(f"Present = {present}, Absent = {absent}")
        if errors:
            print("Invalid records:")
            for line_no, message in errors:
                print(f"Line {line_no}: {message}")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as exc:
        print(f"File-level error: {exc}")

    print("\nMisuse experiment with except Exception: pass")
    misuse_experiment()


if __name__ == "__main__":
    main()
