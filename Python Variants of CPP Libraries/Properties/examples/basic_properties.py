"""Core .properties usage example."""

from __future__ import annotations

import _bootstrap  # noqa: F401

from Properties.core import Properties


def main():
	props = Properties()
	props.set_property("app.name", "DemoApp")
	props.set_property("app.version", "1.0.0")
	props.save("demo.properties")

	props.clear()
	props.load("demo.properties")
	print(props.get_property("app.name"))
	print(props.get_property("app.version"))
	print(props.get_optional("missing").or_else("not found"))


if __name__ == "__main__":
	main()
