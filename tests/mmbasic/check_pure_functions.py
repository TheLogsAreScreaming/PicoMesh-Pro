#!/usr/bin/env python3
"""Run pure helper functions from meshcore.bas under MMB4L and check the output.

MMB4L is MMBasic for Linux, not PicoMite firmware. This executes real MMBasic
for code that does not touch the UART or files; it says nothing about hardware.
Usage: check_pure_functions.py /path/to/mmbasic
"""
import calendar
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = (ROOT / "meshcore.bas").read_text(encoding="utf-8").replace("\r\n", "\n")
FUNCTIONS = ["U32ToLE$", "U32LEVal", "IsWholeNumber", "IsDecimalNumber", "IsLoraBandwidth", "DateTimeToUnix", "UnixToDate$"]


def extract(name):
    match = re.search(r"^Function " + re.escape(name) + r"\(.*?^End Function$", SOURCE, re.M | re.S)
    if not match:
        sys.exit(f"function not found: {name}")
    return match.group(0)


def epoch(*parts):
    return calendar.timegm(parts + (0, 0, 0))


CASES = [
    ('Asc(Mid$(U32ToLE$(305419896), 1, 1))', 0x78),
    ('Asc(Mid$(U32ToLE$(305419896), 4, 1))', 0x12),
    ('U32LEVal(U32ToLE$(4294967295), 1)', 4294967295),
    ('U32LEVal("x" + U32ToLE$(1704067200), 2)', 1704067200),
    ('IsWholeNumber("123456")', 1),
    ('IsWholeNumber("1234567")', 0),
    ('IsWholeNumber("1a")', 0),
    ('IsWholeNumber("")', 0),
    ('IsDecimalNumber("869.525")', 1),
    ('IsDecimalNumber("1.2.3")', 0),
    ('IsDecimalNumber("-1")', 0),
    ('IsLoraBandwidth(62500)', 1),
    ('IsLoraBandwidth(7800)', 1),
    ('IsLoraBandwidth(100000)', 0),
    ('DateTimeToUnix("01-01-2024", "00:00:00")', epoch(2024, 1, 1)),
    ('DateTimeToUnix("29-02-2024", "12:34:56")', epoch(2024, 2, 29) + 12 * 3600 + 34 * 60 + 56),
    ('DateTimeToUnix("31-12-2099", "23:59:59")', epoch(2099, 12, 31) + 86399),
]


def main():
    lines = [f'Print "R{i}="; Str$({expr})' for i, (expr, _) in enumerate(CASES)]
    lines.append('Print "D="; UnixToDate$(1709210096)')
    lines.append('Print "DONE"')
    program = "Option Explicit\n" + "\n".join(lines) + "\nEnd\n\n" + "\n\n".join(extract(n) for n in FUNCTIONS) + "\n"
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "checks.bas"
        path.write_text(program, encoding="utf-8")
        result = subprocess.run([sys.argv[1], str(path)], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=60)
    output = result.stdout + result.stderr
    print(output)
    failures = 0
    for i, (expr, expected) in enumerate(CASES):
        match = re.search(rf"R{i}=\s*(-?[\d.eE+]+)", output)
        if not match or float(match.group(1)) != expected:
            failures += 1
            print(f"FAIL {expr}: expected {expected}, got {match.group(1) if match else 'no output'}")
    date = re.search(r"D=(.*)", output)
    if not date or "2024" not in date.group(1) or "29" not in date.group(1):
        failures += 1
        print("FAIL UnixToDate$")
    if "DONE" not in output:
        failures += 1
        print("FAIL program did not finish")
    print(f"{len(CASES) + 2} checks, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
