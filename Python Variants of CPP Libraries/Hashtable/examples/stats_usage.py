"""Stats and convenience helper example."""

from __future__ import annotations

import os
import sys


SCRIPT_DIR = os.path.dirname(__file__)
TABLE_DIR = os.path.dirname(SCRIPT_DIR)
ROOT_DIR = os.path.dirname(TABLE_DIR)

for path in (ROOT_DIR, TABLE_DIR):
	if path not in sys.path:
		sys.path.insert(0, path)

try:
	from Hashtable.stats import StatsHashtable
except ImportError:
	from stats import StatsHashtable  # type: ignore[no-redef]


def main() -> None:
	table = StatsHashtable(capacity=4, mode="dynamic")
	table["x"] = 10
	table["y"] = 20

	print("stats:", table.stats())
	print("length:", len(table))
	print("contains x:", "x" in table)
	print("x value:", table["x"])


if __name__ == "__main__":
	main()
