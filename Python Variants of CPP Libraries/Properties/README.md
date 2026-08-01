# Properties for Arduino-Style Python Projects

This folder contains a lightweight Python Properties implementation designed for Arduino-style and MicroPython-style workflows.

The package is split into a small core plus optional format modules so you can import only what you need.
The format modules focus on common key/value subsets of each format, which keeps the code compact and memory-friendly.

## Goals

- Keep the core key/value store small.
- Back the store with the Hashtable library.
- Support common key/value file formats.
- Let memory-sensitive users import only a single format module.

## Structure

- `core.py` - core in-memory properties store plus generic `.properties` handling
- `formats/` - optional format-specific modules
- `examples/` - small runnable usage samples

## Supported File Types

The current Python variant is designed around these common key/value file types:

- `.properties`
- `.yml`
- `.yaml`
- `.ini`
- `.json`
- `.csv`
- `.toml`
- `.xml`
- `.msgpack`
- `.mpk`

MessagePack support is optional and only available when a `msgpack` package exists in the runtime.

## Core Module

Use `Properties.core.Properties` when you want the smallest import surface.

Core features:

- in-memory key/value storage
- `set_property()` / `get_property()`
- `remove_property()` / `contains_key()`
- `load_text()` / `save_text()` for `.properties`-style data
- `load()` / `save()` for `.properties` files
- `get_optional()` for optional-style access
- `supported_file_types()` for the file types supported by the current class

### Example

```python
from Properties.core import Properties

props = Properties()
props.set_property("app.name", "Demo")
props.set_property("version", "1.0")
props.save("config.properties")
```

## Format Modules

Import only the format module you need.

### YAML

```python
from Properties.formats.yaml import YamlProperties
```

### JSON

```python
from Properties.formats.json import JsonProperties
```

### INI

```python
from Properties.formats.ini import IniProperties
```

### CSV

```python
from Properties.formats.csv import CsvProperties
```

### TOML

```python
from Properties.formats.toml import TomlProperties
```

### XML

```python
from Properties.formats.xml import XmlProperties
```

### MessagePack

```python
from Properties.formats.msgpack import MsgPackProperties
```

## Notes on Memory Use

- Import `core.py` only if you only need a simple key/value store.
- Import a specific format module only when you need that file type.
- MessagePack is optional and may require an external `msgpack` package in some environments.

## File Type Mapping

- `.properties` -> core
- `.yml` / `.yaml` -> `formats/yaml.py`
- `.ini` -> `formats/ini.py`
- `.json` -> `formats/json.py`
- `.csv` -> `formats/csv.py`
- `.toml` -> `formats/toml.py`
- `.xml` -> `formats/xml.py`
- `.msgpack` / `.mpk` -> `formats/msgpack.py`

## Examples

See the `examples/` folder for small runnable scripts.
