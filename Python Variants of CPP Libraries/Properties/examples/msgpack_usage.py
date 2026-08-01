"""MessagePack usage example."""

from __future__ import annotations

import _bootstrap  # noqa: F401

from Properties.formats.msgpack import MsgPackProperties


def main():
	props = MsgPackProperties()
	props.set_property("device", "uno")
	props.set_property("channel", "A1")
	try:
		props.save("demo.msgpack")
		print("saved messagepack")
	except ImportError as exc:
		print(exc)


if __name__ == "__main__":
	main()
