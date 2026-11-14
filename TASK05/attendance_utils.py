def read_attendance(path):
    rows = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(tuple(line.split(",")))
    return rows


def compute_counts(rows):
    stats = {}
    for reg_no, _, status in rows:
        stats.setdefault(reg_no, {"present": 0, "absent": 0})
        if status == "P":
            stats[reg_no]["present"] += 1
        elif status == "A":
            stats[reg_no]["absent"] += 1
    return stats
