def compute_counts(rows):
    stats = {}
    for reg_no, _, status in rows:
        stats.setdefault(reg_no, {"present": 0, "absent": 0})
        if status == "P":
            stats[reg_no]["present"] += 1
        elif status == "A":
            stats[reg_no]["absent"] += 1
    return stats
