"""Shared helpers for format-specific Properties modules."""

from __future__ import annotations


def stringify(value):
	return "" if value is None else str(value)


def strip_quotes(value):
	text = value.strip()
	if len(text) >= 2 and ((text[0] == '"' and text[-1] == '"') or (text[0] == "'" and text[-1] == "'")):
		return text[1:-1]
	return text


def split_simple_line(line, separators=("=", ":")):
	for separator in separators:
		index = line.find(separator)
		if index > 0:
			return line[:index].strip(), line[index + len(separator):].strip()
	return None, None


def parse_flat_text(text, separators=("=", ":"), comment_prefixes=("#", ";"), value_transform=None):
	mapping = {}
	for raw_line in text.splitlines():
		line = raw_line.strip()
		if not line:
			continue
		if line[0] in comment_prefixes:
			continue
		key, value = split_simple_line(line, separators=separators)
		if key is None:
			continue
		if value_transform is not None:
			value = value_transform(value)
		mapping[key] = stringify(value)
	return mapping


def serialize_flat_text(mapping, separator="=", comments=None, comment_prefix="#"):
	lines = []
	if comments:
		for comment_line in str(comments).splitlines():
			lines.append(comment_prefix + " " + comment_line if comment_line else comment_prefix)
	for key in mapping:
		lines.append(stringify(key) + separator + stringify(mapping[key]))
	return "\n".join(lines) + ("\n" if lines else "")
