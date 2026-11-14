from pathlib import Path


def write_report(stats, out_path):
    lines = ["Register Number,Present,Absent,Percentage"]
    for reg_no in sorted(stats):
        present = stats[reg_no]["present"]
        absent = stats[reg_no]["absent"]
        total = present + absent
        pct = (present / total) * 100 if total else 0.0
        lines.append(f"{reg_no},{present},{absent},{pct:.2f}%")
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
