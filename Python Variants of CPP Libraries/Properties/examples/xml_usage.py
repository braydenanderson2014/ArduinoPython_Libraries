"""XML usage example."""

from __future__ import annotations

import _bootstrap  # noqa: F401

from Properties.formats.xml import XmlProperties


def main():
	props = XmlProperties()
	props.set_property("alpha", "1")
	props.set_property("beta", "2")
	props.save("demo.xml")
	print(props.save_text())


if __name__ == "__main__":
	main()
