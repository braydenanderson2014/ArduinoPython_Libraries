"""TOML usage example."""

from __future__ import annotations

import _bootstrap  # noqa: F401

from Properties.formats.toml import TomlProperties


def main():
	props = TomlProperties()
	props.set_property("app.name", "Demo")
	props.set_property("app.mode", "debug")
	props.save("demo.toml")
	print(props.save_text())


if __name__ == "__main__":
	main()
