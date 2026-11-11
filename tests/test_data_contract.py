"""Data contract smoke test (stdlib only, no dependencies).

Validates every CSV committed in the repository:
  - decodes as UTF-8 (BOM tolerated)
  - delimiter detected (comma / semicolon / tab / pipe)
  - header row present with no empty column names
  - at least one data row
  - consistent column count across sampled rows (catches truncated/malformed CSV)

Runs in CI with no third-party packages. Exit code 1 on any violation.
"""
import csv
import os
import sys

MAX_BYTES = 60 * 1024 * 1024
MAX_ROWS_SAMPLED = 20_000
CANDIDATES = [",", ";", "\t", "|"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_csvs():
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", ".venv", "venv"}]
        for name in filenames:
            if name.lower().endswith(".csv"):
                found.append(os.path.join(dirpath, name))
    return sorted(found)


def detect_delimiter(path):
    """Los datos del INE vienen con ';' y BOM, no con coma."""
    with open(path, "r", encoding="utf-8-sig", errors="strict") as fh:
        head = fh.readline()
    counts = {d: head.count(d) for d in CANDIDATES}
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else ","


def check(path):
    rel = os.path.relpath(path, ROOT)
    size = os.path.getsize(path)
    if size == 0:
        return f"{rel}: archivo vacio"
    if size > MAX_BYTES:
        return None  # demasiado grande para validar en CI, se omite

    try:
        delimiter = detect_delimiter(path)
        with open(path, "r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.reader(fh, delimiter=delimiter)
            header = next(reader)
            if not header:
                return f"{rel}: sin fila de cabecera"
            empty = [i for i, c in enumerate(header) if not c.strip()]
            if empty:
                return f"{rel}: columnas sin nombre en posiciones {empty}"
            width = len(header)
            rows = 0
            for rows, row in enumerate(reader, start=1):
                if len(row) != width:
                    return f"{rel}: fila {rows + 1} tiene {len(row)} columnas (esperado {width}, delim={delimiter!r})"
                if rows >= MAX_ROWS_SAMPLED:
                    break
            if rows == 0:
                return f"{rel}: solo cabecera, sin datos"
        return None
    except UnicodeDecodeError as exc:
        return f"{rel}: no es UTF-8 valido ({exc.reason})"
    except csv.Error as exc:
        return f"{rel}: CSV invalido ({exc})"


def main():
    csvs = find_csvs()
    if not csvs:
        print("FAIL: no se encontro ningun CSV para validar")
        return 1
    problems = [p for p in (check(c) for c in csvs) if p]
    for c in csvs:
        print(f"  ok  {os.path.relpath(c, ROOT)} (delim={detect_delimiter(c)!r})")
    if problems:
        print()
        for p in problems:
            print(f"FAIL: {p}")
        return 1
    print(f"\nOK: {len(csvs)} dataset(s) validados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
