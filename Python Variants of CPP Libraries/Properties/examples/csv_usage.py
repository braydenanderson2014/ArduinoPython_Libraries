"""CSV usage example."""

from __future__ import annotations

import _bootstrap  # noqa: F401

from Properties.formats.csv import CsvProperties


def main():
	props = CsvProperties()
	props.set_property("x", "10")
	props.set_property("y", "20")
	props.save("demo.csv")
	print(props.save_text())


if __name__ == "__main__":
	main()
