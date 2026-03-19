"""
token_tracker.py
================
Track and analyse token usage from Cline and Kilo Code.

────────────────────────────────────────────────────────
QUICK START
────────────────────────────────────────────────────────

  Just run it — it will ask you everything it needs:

    python3 token_tracker.py

  The script will prompt you to:
    1. Choose which tool(s) to track  →  Cline / Kilo Code / Both
    2. Choose a time window           →  Today / Last 7 days / Custom

  Reports are saved as CSV + JSON in the current folder.

────────────────────────────────────────────────────────
OPTIONS
────────────────────────────────────────────────────────

  --output-dir <path>
      Where to save the output files. Defaults to current directory.

      Example:
        python3 token_tracker.py --output-dir ~/token-reports

  --files <file1> [file2] ...
      Load one or more previously exported files (JSON or CSV) and
      include them in the report alongside the live storage scan.
      You can pass multiple files at once.

      Accepted formats:
        *.json  →  raw export files  (*_raw_*.json)
        *.csv   →  daily summary files  (*.csv)

      Examples:
        python3 token_tracker.py --files march_export.json
        python3 token_tracker.py --files jan.json feb.csv march.json
        python3 token_tracker.py --files archive.json --output-dir ~/reports

────────────────────────────────────────────────────────
OUTPUT FILES
────────────────────────────────────────────────────────

  All filenames include the time window so runs never overwrite each other.

  When tracking Cline only:
    cline_<window>.csv            Daily token breakdown
    cline_raw_<window>.json       Full record-level detail

  When tracking Kilo Code only:
    kilo_<window>.csv
    kilo_raw_<window>.json

  When tracking Both:
    cline_<window>.csv / .json
    kilo_<window>.csv  / .json
    consolidated_<window>.csv     Both tools summed per day
    comparison_<window>.csv       Side-by-side with delta and % share
    consolidated_raw_<window>.json

  If input files contain records from other sources:
    imported_<window>.csv / .json

────────────────────────────────────────────────────────
AUTOMATION (cron)
────────────────────────────────────────────────────────

  To run automatically every day at 18:00 and log output:

    crontab -e

    # Add this line:
    0 18 * * * python3 /path/to/token_tracker.py --output-dir ~/token-reports >> ~/token-reports/tracker.log 2>&1
"""

import json
import csv
import sys
import argparse
from pathlib import Path
from datetime import datetime, date, timezone, timedelta
from collections import defaultdict

# ──────────────────────────────────────────────
# CONFIG — adjust paths if your setup is unusual
# ──────────────────────────────────────────────

HOME = Path.home()

CLINE_STORAGE_ROOTS = [
    HOME / ".config" / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "tasks",
    HOME / ".config" / "VSCodium" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "tasks",
    HOME / "snap" / "code" / "current" / ".config" / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "tasks",
]

KILO_STORAGE_ROOTS = [
    HOME / ".config" / "Code" / "User" / "globalStorage" / "kilocode.kilo-code" / "tasks",
    HOME / ".config" / "VSCodium" / "User" / "globalStorage" / "kilocode.kilo-code" / "tasks",
    HOME / "snap" / "code" / "current" / ".config" / "Code" / "User" / "globalStorage" / "kilocode.kilo-code" / "tasks",
]

# ──────────────────────────────────────────────
# PROMPT HELPERS
# ──────────────────────────────────────────────

def hr(char="─", width=55):
    return char * width

def banner(title: str):
    print(f"\n┌{hr()}┐")
    print(f"│  {title:<53}│")
    print(f"└{hr()}┘")

def prompt_choice(prompt: str, options: dict[str, str]) -> str:
    for key, label in options.items():
        print(f"  {key} — {label}")
    while True:
        choice = input(f"\n  {prompt}: ").strip()
        if choice in options:
            return choice
        print(f"  ✘ Invalid. Please enter one of: {', '.join(options.keys())}")

def prompt_datetime(label: str, default: datetime) -> datetime:
    formatted = default.strftime("%Y-%m-%d %H:%M")
    raw = input(f"  {label} [{formatted}]: ").strip()
    if not raw:
        return default
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(raw, fmt)
            if fmt == "%Y-%m-%d":
                dt = dt.replace(hour=0, minute=0)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    print(f"  ✘ Could not parse '{raw}'. Using default: {formatted}")
    return default

# ──────────────────────────────────────────────
# INTERACTIVE MENUS
# ──────────────────────────────────────────────

def prompt_tool_selection() -> str:
    banner("Token Usage Tracker")
    print(f"\n  Which tool(s) do you want to track?\n")
    return prompt_choice("Enter 1, 2 or 3", {
        "1": "Cline only",
        "2": "Kilo Code only",
        "3": "Both (+ comparison report)",
    })

def prompt_time_window() -> tuple[datetime, datetime]:
    now = datetime.now(tz=timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    banner("Time Window")
    print(f"\n  Which time window do you want to analyse?\n")
    window_choice = prompt_choice("Enter 1, 2 or 3", {
        "1": f"Today (from {today_start.strftime('%Y-%m-%d 00:00')} to now)  [default]",
        "2": "Last 7 days",
        "3": "Custom start & end",
    })

    if window_choice == "1":
        return today_start, now
    elif window_choice == "2":
        return now - timedelta(days=7), now
    else:
        print()
        start = prompt_datetime("Start (YYYY-MM-DD HH:MM or YYYY-MM-DD)", today_start)
        end   = prompt_datetime("End   (YYYY-MM-DD HH:MM or YYYY-MM-DD)", now)
        if start > end:
            print("  ✘ Start is after end — swapping them.")
            start, end = end, start
        return start, end

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def parse_timestamp(ts_raw, fallback: datetime) -> datetime:
    try:
        if isinstance(ts_raw, (int, float)):
            return datetime.fromtimestamp(ts_raw / 1000 if ts_raw > 1e10 else ts_raw, tz=timezone.utc)
        if isinstance(ts_raw, str):
            return datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
    except Exception:
        pass
    return fallback

def extract_usage(msg: dict) -> dict | None:
    usage = msg.get("usage") or msg.get("message", {}).get("usage")
    return usage if usage else None

def build_record(source: str, task_id: str, ts: datetime, msg: dict, usage: dict) -> dict:
    return {
        "source": source,
        "task_id": task_id,
        "timestamp": ts.isoformat(),
        "date": ts.date().isoformat(),
        "role": msg.get("role", "unknown"),
        "input_tokens": usage.get("input_tokens", 0) or 0,
        "output_tokens": usage.get("output_tokens", 0) or 0,
        "cache_creation_tokens": usage.get("cache_creation_input_tokens", 0) or 0,
        "cache_read_tokens": usage.get("cache_read_input_tokens", 0) or 0,
    }

def in_window(ts: datetime, start: datetime, end: datetime) -> bool:
    return start <= ts <= end

# ──────────────────────────────────────────────
# FILE INPUT PARSERS
# ──────────────────────────────────────────────

# Raw JSON records are lists of dicts already in build_record() format.
# Daily CSV summaries contain aggregated rows — we re-expand them into
# pseudo-records so they flow through the same aggregation pipeline.

RAW_JSON_FIELDS = {"source", "task_id", "timestamp", "date", "input_tokens", "output_tokens"}
DAILY_CSV_FIELDS = {"date", "source", "input_tokens", "output_tokens", "total_tokens", "requests"}

def _is_raw_json(records: list) -> bool:
    if not records or not isinstance(records[0], dict):
        return False
    return bool(RAW_JSON_FIELDS & set(records[0].keys()))

def _is_daily_csv_row(row: dict) -> bool:
    return bool(DAILY_CSV_FIELDS & set(row.keys()))

def load_json_file(path: Path, start: datetime, end: datetime) -> list[dict]:
    """Load a raw JSON export produced by this script."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ✘ Could not read {path.name}: {e}")
        return []

    if not isinstance(data, list):
        print(f"  ✘ {path.name}: expected a JSON array, skipping.")
        return []

    if not _is_raw_json(data):
        print(f"  ✘ {path.name}: does not look like a raw token export, skipping.")
        return []

    records = []
    fallback = datetime.now(tz=timezone.utc)
    for item in data:
        if not isinstance(item, dict):
            continue
        ts = parse_timestamp(item.get("timestamp"), fallback)
        if not in_window(ts, start, end):
            continue
        # Normalise — keep only known fields, fill missing ones with defaults
        records.append({
            "source":               item.get("source", "imported"),
            "task_id":              item.get("task_id", ""),
            "timestamp":            ts.isoformat(),
            "date":                 ts.date().isoformat(),
            "role":                 item.get("role", "unknown"),
            "input_tokens":         int(item.get("input_tokens", 0) or 0),
            "output_tokens":        int(item.get("output_tokens", 0) or 0),
            "cache_creation_tokens":int(item.get("cache_creation_tokens", 0) or 0),
            "cache_read_tokens":    int(item.get("cache_read_tokens", 0) or 0),
        })
    return records


def load_csv_file(path: Path, start: datetime, end: datetime) -> list[dict]:
    """
    Load a daily CSV export produced by this script.
    Each CSV row is a daily aggregate; we re-expand it into a single
    pseudo-record per row so it flows through aggregate_by_day() again.
    """
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except OSError as e:
        print(f"  ✘ Could not read {path.name}: {e}")
        return []

    if not rows:
        print(f"  [!] {path.name} is empty, skipping.")
        return []

    if not _is_daily_csv_row(rows[0]):
        print(f"  ✘ {path.name}: does not look like a daily CSV export, skipping.")
        return []

    records = []
    for row in rows:
        day_str = row.get("date", "")
        try:
            day = date.fromisoformat(day_str)
        except ValueError:
            continue

        # Use noon UTC as a representative timestamp for the day
        ts = datetime(day.year, day.month, day.day, 12, 0, tzinfo=timezone.utc)
        if not in_window(ts, start, end):
            continue

        records.append({
            "source":                row.get("source", "imported"),
            "task_id":               f"csv-import:{path.stem}",
            "timestamp":             ts.isoformat(),
            "date":                  day_str,
            "role":                  "unknown",
            "input_tokens":          int(row.get("input_tokens", 0) or 0),
            "output_tokens":         int(row.get("output_tokens", 0) or 0),
            "cache_creation_tokens": int(row.get("cache_creation_tokens", 0) or 0),
            "cache_read_tokens":     int(row.get("cache_read_tokens", 0) or 0),
        })
    return records


def load_input_files(paths: list[Path], start: datetime, end: datetime) -> list[dict]:
    """Dispatch each file to the right loader based on its extension."""
    all_records: list[dict] = []
    for path in paths:
        if not path.exists():
            print(f"  ✘ File not found: {path}")
            continue
        suffix = path.suffix.lower()
        if suffix == ".json":
            records = load_json_file(path, start, end)
            label = "raw JSON"
        elif suffix == ".csv":
            records = load_csv_file(path, start, end)
            label = "daily CSV"
        else:
            print(f"  ✘ Unsupported file type '{suffix}' for {path.name}, skipping.")
            continue
        print(f"  ✔ {path.name} ({label}): {len(records)} record(s) loaded")
        all_records.extend(records)
    return all_records

# ──────────────────────────────────────────────
# LIVE STORAGE PARSERS
# ──────────────────────────────────────────────

def parse_tasks(
    roots: list[Path],
    source: str,
    filenames: list[str],
    start: datetime,
    end: datetime,
) -> list[dict]:
    records = []
    for root in roots:
        if not root.exists():
            continue
        for task_dir in root.iterdir():
            if not task_dir.is_dir():
                continue
            task_id = task_dir.name
            folder_mtime = datetime.fromtimestamp(task_dir.stat().st_mtime, tz=timezone.utc)
            for filename in filenames:
                history_file = task_dir / filename
                if not history_file.exists():
                    continue
                try:
                    with open(history_file, encoding="utf-8") as f:
                        messages = json.load(f)
                except (json.JSONDecodeError, OSError):
                    continue
                if not isinstance(messages, list):
                    continue
                for msg in messages:
                    if not isinstance(msg, dict):
                        continue
                    usage = extract_usage(msg)
                    if not usage:
                        continue
                    ts = parse_timestamp(msg.get("ts") or msg.get("timestamp"), fallback=folder_mtime)
                    if not in_window(ts, start, end):
                        continue
                    records.append(build_record(source, task_id, ts, msg, usage))
    return records

# ──────────────────────────────────────────────
# AGGREGATION
# ──────────────────────────────────────────────

def aggregate_by_day(records: list[dict]) -> list[dict]:
    daily = defaultdict(lambda: {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_tokens": 0,
        "cache_read_tokens": 0,
        "requests": 0,
    })
    for r in records:
        d = daily[(r["date"], r["source"])]
        d["input_tokens"] += r["input_tokens"]
        d["output_tokens"] += r["output_tokens"]
        d["cache_creation_tokens"] += r["cache_creation_tokens"]
        d["cache_read_tokens"] += r["cache_read_tokens"]
        d["requests"] += 1

    rows = []
    for (day, source), totals in sorted(daily.items()):
        rows.append({
            "date": day,
            "source": source,
            "input_tokens": totals["input_tokens"],
            "output_tokens": totals["output_tokens"],
            "total_tokens": totals["input_tokens"] + totals["output_tokens"],
            "cache_creation_tokens": totals["cache_creation_tokens"],
            "cache_read_tokens": totals["cache_read_tokens"],
            "requests": totals["requests"],
        })
    return rows


def aggregate_consolidated(rows: list[dict]) -> list[dict]:
    daily = defaultdict(lambda: {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_tokens": 0,
        "cache_read_tokens": 0,
        "requests": 0,
    })
    for r in rows:
        d = daily[r["date"]]
        d["input_tokens"] += r["input_tokens"]
        d["output_tokens"] += r["output_tokens"]
        d["cache_creation_tokens"] += r["cache_creation_tokens"]
        d["cache_read_tokens"] += r["cache_read_tokens"]
        d["requests"] += r["requests"]

    return [
        {
            "date": day,
            "source": "cline + kilo",
            "input_tokens": totals["input_tokens"],
            "output_tokens": totals["output_tokens"],
            "total_tokens": totals["input_tokens"] + totals["output_tokens"],
            "cache_creation_tokens": totals["cache_creation_tokens"],
            "cache_read_tokens": totals["cache_read_tokens"],
            "requests": totals["requests"],
        }
        for day, totals in sorted(daily.items())
    ]


def build_comparison(cline_rows: list[dict], kilo_rows: list[dict]) -> list[dict]:
    def index(rows):
        return {r["date"]: r for r in rows}

    ci = index(cline_rows)
    ki = index(kilo_rows)
    all_dates = sorted(set(ci) | set(ki))

    comparison = []
    for day in all_dates:
        c = ci.get(day, {})
        k = ki.get(day, {})
        c_total  = c.get("total_tokens", 0)
        k_total  = k.get("total_tokens", 0)
        combined = c_total + k_total
        comparison.append({
            "date":               day,
            "cline_input_tokens": c.get("input_tokens", 0),
            "cline_output_tokens":c.get("output_tokens", 0),
            "cline_total_tokens": c_total,
            "cline_requests":     c.get("requests", 0),
            "kilo_input_tokens":  k.get("input_tokens", 0),
            "kilo_output_tokens": k.get("output_tokens", 0),
            "kilo_total_tokens":  k_total,
            "kilo_requests":      k.get("requests", 0),
            "delta_total_tokens": c_total - k_total,
            "delta_requests":     c.get("requests", 0) - k.get("requests", 0),
            "cline_share_pct":    round(c_total / combined * 100, 1) if combined else 0,
            "kilo_share_pct":     round(k_total / combined * 100, 1) if combined else 0,
        })
    return comparison

# ──────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────

def write_csv(rows: list[dict], path: Path, label: str):
    if not rows:
        print(f"  [!] No data to write to {label} CSV.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  ✔ {label} CSV  → {path}")

def write_json(records: list[dict], path: Path, label: str):
    if not records:
        print(f"  [!] No data to write to {label} JSON.")
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"  ✔ {label} JSON → {path}")

def print_summary(rows: list[dict], title: str):
    print(f"\n  ▸ {title}")
    if not rows:
        print("    No token data found in this window.")
        return
    col_source = max(len(r["source"]) for r in rows) + 2
    print(f"  {'DATE':<12} {'SOURCE':<{col_source}} {'INPUT':>10} {'OUTPUT':>10} {'TOTAL':>10} {'REQUESTS':>9}")
    print(f"  {hr('─', 12 + col_source + 44)}")
    for r in rows:
        print(f"  {r['date']:<12} {r['source']:<{col_source}} {r['input_tokens']:>10,} {r['output_tokens']:>10,} {r['total_tokens']:>10,} {r['requests']:>9,}")
    total_in  = sum(r["input_tokens"]  for r in rows)
    total_out = sum(r["output_tokens"] for r in rows)
    print(f"\n  TOTAL  input: {total_in:,}  output: {total_out:,}  combined: {total_in + total_out:,}")

def print_comparison(rows: list[dict]):
    print(f"\n  ▸ Cline vs Kilo Code — side by side")
    if not rows:
        print("    No data to compare.")
        return
    print(f"  {'DATE':<12} {'C.INPUT':>9} {'C.OUTPUT':>9} {'C.TOTAL':>9} {'K.INPUT':>9} {'K.OUTPUT':>9} {'K.TOTAL':>9} {'DELTA':>8} {'C%':>5} {'K%':>5}")
    print(f"  {hr('─', 92)}")
    for r in rows:
        print(
            f"  {r['date']:<12}"
            f" {r['cline_input_tokens']:>9,}"
            f" {r['cline_output_tokens']:>9,}"
            f" {r['cline_total_tokens']:>9,}"
            f" {r['kilo_input_tokens']:>9,}"
            f" {r['kilo_output_tokens']:>9,}"
            f" {r['kilo_total_tokens']:>9,}"
            f" {r['delta_total_tokens']:>+8,}"
            f" {r['cline_share_pct']:>4}%"
            f" {r['kilo_share_pct']:>4}%"
        )
    total_c  = sum(r["cline_total_tokens"] for r in rows)
    total_k  = sum(r["kilo_total_tokens"]  for r in rows)
    combined = total_c + total_k
    c_pct = round(total_c / combined * 100, 1) if combined else 0
    k_pct = round(total_k / combined * 100, 1) if combined else 0
    print(f"\n  TOTAL  Cline: {total_c:,} ({c_pct}%)   Kilo: {total_k:,} ({k_pct}%)")

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

HELP_TEXT = """
Token Usage Tracker — Cline & Kilo Code
════════════════════════════════════════

Just run it — it will ask you everything interactively:

  python3 token_tracker.py

The script will prompt you to:
  1. Choose which tool(s) to track  →  Cline / Kilo Code / Both
  2. Choose a time window           →  Today / Last 7 days / Custom range

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  --output-dir <path>
      Where to save the output files.
      Defaults to the current directory.

      Example:
        python3 token_tracker.py --output-dir ~/token-reports

  --files <file1> [file2] ...
      Load one or more previously exported files and merge them
      into the report alongside the live storage scan.

      Accepted formats:
        *.json   raw export files produced by this script (*_raw_*.json)
        *.csv    daily summary files produced by this script (*.csv)

      Examples:
        python3 token_tracker.py --files march_export.json
        python3 token_tracker.py --files jan.json feb.csv march.json
        python3 token_tracker.py --files archive.json --output-dir ~/reports

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  All filenames include the time window so runs never overwrite each other.

  Cline only:
    cline_<window>.csv              Daily token breakdown
    cline_raw_<window>.json         Full record-level detail

  Kilo Code only:
    kilo_<window>.csv
    kilo_raw_<window>.json

  Both:
    cline_<window>.csv / .json
    kilo_<window>.csv  / .json
    consolidated_<window>.csv       Both tools summed per day
    comparison_<window>.csv         Side-by-side with delta and % share
    consolidated_raw_<window>.json

  If input files contain records from other sources:
    imported_<window>.csv / .json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOMATION (cron)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Run automatically every day at 18:00 and log output:

    crontab -e

    # Add this line:
    0 18 * * * python3 /path/to/token_tracker.py --output-dir ~/token-reports >> ~/token-reports/tracker.log 2>&1
"""


def main():
    parser = argparse.ArgumentParser(
        prog="token_tracker.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=HELP_TEXT,
        add_help=True,
    )
    parser.add_argument(
        "--files", nargs="+", metavar="FILE",
        help="One or more exported JSON or CSV files to merge into the report"
    )
    parser.add_argument(
        "--output-dir", default=".", metavar="PATH",
        help="Directory to write output files (default: current dir)"
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── interactive prompts ──
    tool_choice = prompt_tool_selection()
    start, end  = prompt_time_window()

    track_cline = tool_choice in ("1", "3")
    track_kilo  = tool_choice in ("2", "3")

    window_label = f"{start.strftime('%Y%m%d-%H%M')}_to_{end.strftime('%Y%m%d-%H%M')}"
    print(f"\n  Window: {start.strftime('%Y-%m-%d %H:%M')} → {end.strftime('%Y-%m-%d %H:%M')} UTC")

    # ── load input files if provided ──
    file_records: list[dict] = []
    if args.files:
        banner("Input Files")
        print()
        file_records = load_input_files([Path(p) for p in args.files], start, end)
        print(f"\n  Total from files: {len(file_records)} record(s)")

    cline_records, cline_daily = [], []
    kilo_records,  kilo_daily  = [], []

    # ── scan live storage ──
    if track_cline:
        print("\n🔍 Scanning Cline storage...")
        live = parse_tasks(CLINE_STORAGE_ROOTS, source="cline",
                           filenames=["api_conversation_history.json"],
                           start=start, end=end)
        print(f"   Found {len(live)} usage entries")
        # Merge file records that belong to cline
        file_cline = [r for r in file_records if r.get("source") == "cline"]
        cline_records = live + file_cline
        if file_cline:
            print(f"   + {len(file_cline)} record(s) from input files")
        cline_daily = aggregate_by_day(cline_records)
        print_summary(cline_daily, "Cline")
        write_csv(cline_daily,    output_dir / f"cline_{window_label}.csv",      "Cline")
        write_json(cline_records, output_dir / f"cline_raw_{window_label}.json", "Cline")

    if track_kilo:
        print("\n🔍 Scanning Kilo Code storage...")
        live = parse_tasks(KILO_STORAGE_ROOTS, source="kilo",
                           filenames=["api_conversation_history.json", "ui_messages.json"],
                           start=start, end=end)
        print(f"   Found {len(live)} usage entries")
        file_kilo = [r for r in file_records if r.get("source") == "kilo"]
        kilo_records = live + file_kilo
        if file_kilo:
            print(f"   + {len(file_kilo)} record(s) from input files")
        kilo_daily = aggregate_by_day(kilo_records)
        print_summary(kilo_daily, "Kilo Code")
        write_csv(kilo_daily,    output_dir / f"kilo_{window_label}.csv",      "Kilo Code")
        write_json(kilo_records, output_dir / f"kilo_raw_{window_label}.json", "Kilo Code")

    # ── handle file records with unrecognised source when not tracking both ──
    other_file_records = [
        r for r in file_records
        if r.get("source") not in ("cline", "kilo")
    ]
    if other_file_records:
        other_daily = aggregate_by_day(other_file_records)
        print_summary(other_daily, "Imported (other sources)")
        write_csv(other_daily,       output_dir / f"imported_{window_label}.csv",      "Imported")
        write_json(other_file_records, output_dir / f"imported_raw_{window_label}.json", "Imported")

    # ── combined reports when tracking both ──
    if track_cline and track_kilo:
        all_daily    = cline_daily + kilo_daily
        consolidated = aggregate_consolidated(all_daily)
        comparison   = build_comparison(cline_daily, kilo_daily)

        print()
        banner("Combined Reports")
        print_summary(consolidated, "Consolidated (Cline + Kilo Code)")
        print_comparison(comparison)

        write_csv(consolidated,  output_dir / f"consolidated_{window_label}.csv", "Consolidated")
        write_csv(comparison,    output_dir / f"comparison_{window_label}.csv",   "Comparison")
        write_json(cline_records + kilo_records,
                   output_dir / f"consolidated_raw_{window_label}.json",           "Consolidated")

    print(f"\n  Done. Reports saved to: {output_dir}\n")


if __name__ == "__main__":
    main()
