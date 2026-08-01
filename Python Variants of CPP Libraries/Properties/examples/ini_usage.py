"""INI usage example."""

from __future__ import annotations

import _bootstrap  # noqa: F401

from Properties.formats.ini import IniProperties


def main():
	props = IniProperties()
	props.set_property("network.ssid", "MyWiFi")
	props.set_property("network.password", "secret")
	props.save("demo.ini")
	print(props.save_text())


if __name__ == "__main__":
	main()
