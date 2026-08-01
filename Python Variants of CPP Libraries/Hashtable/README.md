# Hashtable for Arduino-Style Python Projects

This folder contains a small hashtable implementation designed for Arduino-style Python projects, including MicroPython-style environments where memory matters.

The design is split into a lean core plus optional helper modules. That lets users import only what they need.

## Goals

- Keep the core hashtable small and predictable.
- Support both fixed-size and dynamic-size behavior.
- Offer optional helper modules for people who want more convenience.
- Allow imports that match both normal Python and constrained environments.

## What Is in the Core

Use `core.py` when you only want the minimum features required to store and retrieve values.

Core features:

- `ArduinoHashTable`
- `TableMode`
- `OptionalValue` fallback for optional-style access
- `put()`
- `get()`
- `get_optional()`
- `remove()`
- `contains()`
- `clear()`
- `resize()`
- fixed mode and dynamic mode switching

### Core Modes

- `fixed` mode keeps the bucket count stable unless you explicitly resize.
- `dynamic` mode grows automatically when the load factor is exceeded.

### Optional Access

The table can return an `OptionalValue` instead of a raw `None` when you want explicit empty-state handling.

Example:

```python
value_opt = table.get_optional("sensor")
if value_opt.has_value():
    print(value_opt.get_value())
```

## Optional Helper Modules

Helper modules are split by concern so you can import only what you need.

### `iterating.py`

Adds iteration helpers:

- `keys()`
- `values()`
- `items()`

### `sorting.py`

Adds sorted views:

- `sorted_keys()`
- `sorted_values()`
- `sorted_items()`

### `stats.py`

Adds inspection and convenience operators:

- `stats()`
- `len(table)`
- `key in table`
- `table[key]`
- `table[key] = value`
- `del table[key]`
- readable `repr()`

### `extras.py`

This is a compatibility bundle that combines the optional helper areas. It exists for people who want the old single import style, but you do not need it if you prefer importing specific modules.

## Import Patterns

### Minimal core only

```python
from Hashtable.core import ArduinoHashTable

table = ArduinoHashTable(capacity=8, mode="dynamic")
```

### Core plus a specific helper module

```python
from Hashtable.core import ArduinoHashTable
from Hashtable.iterating import IteratingHashtable
```

### Full convenience mode

```python
from Hashtable.extras import ArduinoHashTableExtras
```

## Quick Examples

### Fixed-size table

```python
from Hashtable.core import ArduinoHashTable

table = ArduinoHashTable(capacity=4, mode="fixed", max_entries=4)
table.put("a", 1)
table.put("b", 2)
```

### Dynamic table

```python
from Hashtable.core import ArduinoHashTable

table = ArduinoHashTable(capacity=4, mode="dynamic")
for index in range(10):
    table.put(f"key{index}", index)
```

### Optional value handling

```python
from Hashtable.core import ArduinoHashTable

table = ArduinoHashTable()
result = table.get_optional("missing")
print(result.or_else(-1))
```

### Iteration helpers

```python
from Hashtable.iterating import IteratingHashtable

table = IteratingHashtable()
table.put("a", 1)
table.put("b", 2)

for key in table.keys():
    print(key)
```

### Sorted views

```python
from Hashtable.sorting import SortingHashtable

table = SortingHashtable()
table.put("b", 2)
table.put("a", 1)
print(table.sorted_keys())
```

### Stats and indexing helpers

```python
from Hashtable.stats import StatsHashtable

table = StatsHashtable()
table["x"] = 10
print(table.stats())
print(table["x"])
```

## Suggested Module Map

- Use `core.py` for embedded or memory-sensitive code.
- Use `iterating.py` when you only need key/value iteration.
- Use `sorting.py` when you only need sorted views.
- Use `stats.py` when you only need convenience access and diagnostics.
- Use `extras.py` only when you want all helper areas in one import.

## Notes for MicroPython

- Keep imports narrow when memory matters.
- Prefer `core.py` if you do not need the helper modules.
- Use `OptionalValue` when you want explicit empty-state handling instead of raw `None`.

## Example Files

See the `examples` folder for small runnable demonstrations of each module.
