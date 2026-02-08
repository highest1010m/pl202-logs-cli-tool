"""
PL202 — Day 2 (45 min) — Log Filter CLI Tool (Individual)
"""

import argparse
from pathlib import Path

LOG_FILE = Path("logs.txt")
DEFAULT_OUT = "filtered_logs.txt"
ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}


def parse_line(line: str):
    line = line.strip()
    if not line:
        return None

    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 4:
        return None

    timestamp, level, service, message = parts
    return timestamp, level, service, message


def is_valid_level(level: str) -> bool:
    return level.upper() in ALLOWED_LEVELS


def matches_filters(level: str, service: str, level_filter, service_filter) -> bool:
    if level_filter and level != level_filter:
        return False
    if service_filter and service != service_filter:
        return False
    return True


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Filter cloud logs by level and/or service.")
    parser.add_argument("--level", help="Log level (INFO, WARN, ERROR)")
    parser.add_argument("--service", help="Service name")
    parser.add_argument("--out", default=DEFAULT_OUT, help="Output file name")
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    level_filter = args.level.upper() if args.level else None
    service_filter = args.service if args.service else None
    out_path = Path(args.out)

    if not LOG_FILE.exists():
        print(f"ERROR: Cannot find {LOG_FILE}. Put logs.txt in the same folder as this file.")
        return

    total_valid_scanned = 0
    lines_written = 0
    output_lines = []

    with LOG_FILE.open("r") as file:
        for line in file:
            parsed = parse_line(line)
            if parsed is None:
                continue

            timestamp, level, service, message = parsed
            level = level.upper()

            if not is_valid_level(level):
                continue

            total_valid_scanned += 1

            if matches_filters(level, service, level_filter, service_filter):
                output_lines.append(f"{timestamp} | {level} | {service} | {message}")
                lines_written += 1

    with out_path.open("w") as out:
        for line in output_lines:
            out.write(line + "\n")

    print(f"Valid lines scanned: {total_valid_scanned}")
    print(f"Lines written: {lines_written}")
    print(f"Output file: {out_path.name}")


if __name__ == "__main__":
    main()
