"""Shared path bootstrap for Properties examples."""

from __future__ import annotations

import os
import sys


SCRIPT_DIR = os.path.dirname(__file__)
PROPERTIES_DIR = os.path.dirname(SCRIPT_DIR)
ROOT_DIR = os.path.dirname(PROPERTIES_DIR)

for path in (ROOT_DIR, PROPERTIES_DIR):
	if path not in sys.path:
		sys.path.insert(0, path)
