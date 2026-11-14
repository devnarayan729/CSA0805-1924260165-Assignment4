# CSA0805 - 1924260165 - Assignment 4

This repository contains the solutions for Python Programming Assignment 4 on robust data processing with files, exceptions, modules, and packages.

## Student
- Name: Dev Narayan E
- Register Number: 1924260165
- Python Version: Python 3.12
- Libraries Used: Python standard library only

## Folder structure
- `TASK01`: Diagnoses and repairs a poor file-processing script for hostel mess bills.
- `TASK02`: Models biometric attendance data and processes monthly records.
- `TASK03`: Designs and demonstrates exception handling for the attendance processor.
- `TASK04`: Library return-log maintenance and forensic trace of data loss.
- `TASK05`: The same attendance utility organised as one script, a module, and a package.
- `TASK06`: Fest registration validation for duplicate entries and invalid email addresses.

## Requirements
`requirements.txt` contains no external dependencies; the programs use the Python standard library only.

## Run commands
```bash
python TASK01/mess_bill_repair.py
python TASK02/attendance_monthly.py
python TASK03/attendance_exceptions.py
python TASK04/returns_log.py
python TASK05/one_script.py
python TASK05/package_demo.py
python TASK06/fest_registration.py
```

## Summary of results
- `TASK01`: The messy report is repaired by using `with`, line-by-line reading, Decimal-based amount parsing, and a list of rejected lines.
- `TASK02`: Daily attendance files are accumulated in a dictionary and written to summary and below-75% reports.
- `TASK03`: A custom `InvalidRecord` exception is raised for bad data, and a `try/except/else/finally` flow handles errors safely.
- `TASK04`: Return entries are appended safely to a daily log, making file-handling defects easier to trace.
- `TASK05`: The attendance utility is organised in multiple ways to compare effort and structure.
- `TASK06`: Registration records are validated for duplicate IDs and malformed email entries.

## Notes
All programs are intended to be executed from the repository root with Python 3.x.
