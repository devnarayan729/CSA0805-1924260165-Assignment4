from pathlib import Path


def save_returns(books, log_path="returns_log.txt"):
    """Append each returned book to the daily library log."""
    with open(log_path, "a", encoding="utf-8") as log_file:
        for title in books:
            log_file.write(f"{title}\n")


def main():
    sample_books = [
        "Python Basics",
        "Data Structures",
        "Operating Systems",
        "Algorithms",
    ]

    log_path = Path(__file__).with_name("returns_log.txt")
    save_returns(sample_books, log_path)
    print(f"Saved {len(sample_books)} returned books to {log_path.name}")

    print("\nCurrent log contents:")
    if log_path.exists():
        print(log_path.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
