"""Recalculate the workbook's headline comparisons from daily PortWatch counts."""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

DATA = Path(__file__).resolve().parents[1] / "data"
START = "2026-01-01"
BREAK = "2026-02-28"

def load(name):
    with (DATA / name).open() as source:
        rows = list(csv.DictReader(source))
    keys = {(row["portid"], row["date"]) for row in rows}
    if len(keys) != len(rows):
        raise ValueError(f"Duplicate location and date in {name}")
    return rows

def compare(rows, field, end):
    before = mean(int(r[field]) for r in rows if START <= r["date"] < BREAK)
    after = mean(int(r[field]) for r in rows if BREAK <= r["date"] <= end)
    return before, after, 100 * (after / before - 1)

if __name__ == "__main__":
    crossings = load("crossings.csv")
    visits = load("port_visits.csv")
    print(f"{len(crossings):,} chokepoint-days and {len(visits):,} port-days")
    hormuz = [r for r in crossings if r["portid"] == "chokepoint6"]
    before, after, change = compare(hormuz, "n_total", "2026-11-15")
    print(f"Hormuz crossings per day: {before:.1f} → {after:.1f} ({change:+.1f}%)")
    ports = defaultdict(list)
    for row in visits:
        ports[row["portname"]].append(row)
    for name, rows in sorted(ports.items()):
        before, after, change = compare(rows, "portcalls", "2026-11-13")
        print(f"{name}: {before:.2f} → {after:.2f} visits per day ({change:+.1f}%)")
