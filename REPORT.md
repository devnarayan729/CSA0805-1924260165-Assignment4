# Assignment 4 Report

## TASK 1 — File-processing design review

### 1.1 Diagnose the script
The original script has several design deficiencies:
1. Hard-coded file path: the script is tied to one machine and folder, so it fails on another computer or server.
2. File never closed: the open file stays open after reading, which can leak resources and lock the file.
3. Whole-file read into memory: `f.read()` loads the entire file at once, which is costly for a large file of 50,000 lines.
4. Bare `except:` hides all problems: a missing field, conversion error or even a keyboard interrupt may be silently ignored.
5. Amounts with paise are not handled: `int()` truncates decimals like `1250.50` to `1250` and loses the paisa value.
6. Repeated string concatenation: `report = report + ...` is inefficient and expensive for long files.
7. Empty final line: a trailing newline or blank line may be processed and cause `parts[2]` errors.
8. Rejected data is not logged: the office cannot audit which records were skipped or why.

For the hostel office, these weaknesses can cause incorrect totals, lost bills, silent data loss, and no trace of which student records were rejected.

### 1.2 Repair the design
The corrected design uses:
- `with open(...)` so the file is always closed.
- line-by-line iteration instead of reading the full file.
- `Decimal` for accurate money values.
- explicit exceptions such as `ValueError` and `InvalidOperation`.
- a `rejected` list that records the invalid line number and reason.
- a function `repair_mess_file(file_name)` to keep the logic reusable.

### 1.3 Why this is safer for 50,000 lines
The improved version processes one line at a time, so memory usage stays proportional to one record instead of the entire file. It also logs rejected lines with reasons, which makes it easier to find and fix bad input. The strict `try/except` handling prevents silent corruption and preserves the correct total.

### Alternative concept and complexity
If the entire file were read using `f.read()` or `f.readlines()`, the approach would still work, but it would use more memory. Time complexity remains O(n), because each line is still visited once. Space complexity changes from O(1) extra working memory plus the output list, to O(file size) when the entire file is held in memory.

---

## TASK 2 — From requirement to file-processing design

### 2.1 Model the data
Input format: each attendance line is of the form `register_number,date,status`, such as `192311001,2026-10-08,P`.

Data structures:
- `student_stats[reg_no] = {"present": count, "absent": count}`
- `damaged_lines` stores `(file_name, line_number, reason, line_text)`

Outputs:
1. `monthly_attendance_summary.txt`: each student with total days, present count, absent count, and percentage.
2. `students_below_75.txt`: students whose percentage is below 75%.
3. `damaged_lines.log`: every damaged line encountered with the file name and line number.

### 2.2 File operations
The design uses:
- mode `r` for reading daily files
- mode `w` for creating the report files
- `encoding='utf-8'` to support standard text data reliably
- iteration over the file object (`for line in handle`) so each line is processed without loading the entire file.

This is appropriate because we want to stream the file and avoid holding the full month’s data in memory beyond the dictionary counts.

### 2.3 Processing pseudocode
```
BEGIN
    initialise student_stats as empty dictionary
    initialise damaged_lines as empty list

    files = list all .txt files in the month directory
    FOR each file in files DO
        OPEN file in read mode
        FOR each line with its line number DO
            IF line is blank THEN
                CONTINUE
            ENDIF

            TRY
                split line into exactly 3 parts
                validate status is P or A
                register, date, status = parts
            CATCH invalid data DO
                append (file name, line number, error message, line) to damaged_lines
                CONTINUE
            END TRY

            IF status = P THEN
                student_stats[register].present += 1
            ELSE
                student_stats[register].absent += 1
            ENDIF
        ENDFOR
        CLOSE file
    ENDFOR

    write monthly attendance summary to summary file
    write students below 75% to warning file
    write damaged lines log to damaged log file
END
```

### 2.4 Trace example
Taken from a small file:
```
192311001,2026-10-08,P
192311002,2026-10-08,A
192311003,2026-10-08
```
Processing:
- line 1 is valid; register 192311001 gets one present attendance.
- line 2 is valid; register 192311002 gets one absent attendance.
- line 3 is damaged because it has only two fields; it is logged as damaged with the file name and line number.

### Alternative concept and complexity
If the solution re-read all the daily files for each student, the time would be O(s × f × l) because every student lookup would rescan all files. The dictionary approach processes each file once and updates counts directly, giving O(f × l). The space used is O(s) for the accumulated statistics plus the log list, while re-reading by student would not necessarily reduce the space but would multiply the time cost.

---

## TASK 3 — Design the error handling

### 3.1 Identify the failures
Possible failures and exceptions include:
- missing folder: `FileNotFoundError`
- missing file: `FileNotFoundError`
- permission denied: `PermissionError`
- wrong encoding: `UnicodeDecodeError`
- damaged line: `ValueError`, `IndexError`, or a custom `InvalidRecord`
- empty file: `StopIteration` is not a typical exception when reading, but the program should handle it as an empty dataset gracefully

### 3.2 Custom exception
`InvalidRecord` is raised when a line does not contain exactly three comma-separated values or when the status is neither `P` nor `A`.

The exception is raised in `parse_line()` and handled in `summarise()`, where the program records the error and continues processing the remaining lines.

### 3.3 Complete `try` statement
The code uses:
- `try` to open and read the file
- `except (FileNotFoundError, PermissionError, UnicodeDecodeError)` to catch file-level errors
- `except InvalidRecord` to catch data issues per line
- `else` to report successful processing
- `finally` to say the operation is complete
- `raise ... from ...` when re-raising a higher-level error to keep the original cause

### 3.4 Misuse experiment
If the code were changed to `except Exception: pass`, then mis-typed variable names, invalid logic, or other unexpected errors would be swallowed silently. The user would see no helpful message, and debugging would become difficult because the root cause is hidden. This is why specific exceptions are preferred.

---

## Complexity summary
- File processing line by line: time O(n), space O(1) working memory per line + output data.
- Whole-file read approach: time O(n), space O(file size) because the entire file is kept in memory.
- Monthly attendance dictionary approach: time O(f × l), space O(s) for the student counters plus log data.
- Re-reading files per student: time O(s × f × l), which is much slower for large data sets.

---

## TASK 4 — File and exception forensics

The library log task is handled by a function that appends each returned book to a log file using `with open(..., "a")`. This keeps each addition independent and avoids overwriting the previous days' records. The sample script also records the current log contents so the trace of the day's returns can be verified.

## TASK 5 — Same utility organised four ways

The attendance utility is shown in four forms:
1. one script that contains all logic in one file
2. separate input and processing functions in a module
3. a main file that imports helpers from the same directory
4. a small package using separate reader, stats, and writer modules

This comparison highlights the trade-off between minimal setup and cleaner organisation.

## TASK 6 — Design challenge

The college fest registration program validates each record for the correct number of fields, duplicate registration IDs, and valid email addresses. Rejected items are collected in a list so the output remains useful while the valid registrations are processed and printed clearly.

