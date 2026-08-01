"""JSON usage example."""

from __future__ import annotations

import _bootstrap  # noqa: F401

from Properties.formats.json import JsonProperties


def main():
	props = JsonProperties()
	props.set_property("name", "WeatherStation")
	props.set_property("port", "8080")
	props.save("demo.json")
	print(props.save_text())


if __name__ == "__main__":
	main()
