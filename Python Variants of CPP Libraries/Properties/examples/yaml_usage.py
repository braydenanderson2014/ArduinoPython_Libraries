"""YAML usage example."""

from __future__ import annotations

import _bootstrap  # noqa: F401

from Properties.formats.yaml import YamlProperties


def main():
	props = YamlProperties()
	props.set_property("device.name", "SensorNode")
	props.set_property("enabled", "true")
	props.save("demo.yaml")
	print(props.save_text())


if __name__ == "__main__":
	main()
