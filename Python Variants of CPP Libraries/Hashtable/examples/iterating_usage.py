"""Iteration helper example."""

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
	from Hashtable.iterating import IteratingHashtable
except ImportError:
	from iterating import IteratingHashtable  # type: ignore[no-redef]


def main() -> None:
	table = IteratingHashtable()
	table.put("a", 1)
	table.put("b", 2)
	table.put("c", 3)

	print("keys:", list(table.keys()))
	print("values:", list(table.values()))
	print("items:", list(table.items()))


if __name__ == "__main__":
	main()
