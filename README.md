# flake8-typing-collections
A flake8 plugin that checks the use of type alternatives from
the `typing` module over actual run time types, especially from
the `collections` module.

## Options

The plugin offers the following flags to select which errors to enable.
All errors that are not explicitly enabled, are not reported.

* `--tyco_generic_alt`: Enables `TYCO101`, `TYCO102`, `TYCO103`, `TYCO106`, 
`TYCO107`, `TYCO108`, `TYCO109`, `TYCO110`, `TYCO111`, `TYCO112`, `TYCO114`, 
`TYCO115`, `TYCO116`, `TYCO117`, `TYCO118`, `TYCO119`, `TYCO120`, `TYCO121`, 
`TYCO122`, `TYCO123`, `TYCO124`, `TYCO125`, `TYCO126`, `TYCO127`, `TYCO128`,
`TYCO129`, `TYCO130`, `TYCO131`, and `TYCO132`. 
* `--tyco_alias_alt`: Enables `TYCO104`, `TYCO105`, and `TYCO113`.
* `--tyco_general_args`: Enables `TYCO200`, `TYCO201`, and `TYCO202`.

If none of these flags is given, the default selection is used instead,
which is `--tyco_generic_alt` and `--tyco_general_args`.

## Error Codes

## TYCO1xx class

The `typing` module defines several generic versions of built-in
classes, such as `typing.List[T]` instead of `list`. Their usage
is preferred.

```python
# Good
def sum_list(x: List[SupportsFloat]) -> float:
    ...

# Bad
def sum_list(x: list) -> float:
    ...
```

### TYCO100

Use `typing.Iterable` instead of `collections.abc.Iterable` for type annotations.


### TYCO101

Use `typing.Iterator` instead of `collections.abc.Iterator` for type annotations.


### TYCO102

Use `typing.Reversible` instead of `collections.abc.Reversible` for type annotations.


### TYCO103

Use `typing.Container` instead of `collections.abc.Container` for type annotations.


### TYCO104

Use `typing.Hashable` instead of `collections.abc.Hashable` for type annotations.


### TYCO105

Use `typing.Sized` instead of `collections.abc.Sized` for type annotations.


### TYCO106

Use `typing.Collection` instead of `collections.abc.Collection` for type annotations.


### TYCO107

Use `typing.AbstractSet` instead of `collections.abc.Set` for type annotations.


### TYCO108

Use `typing.MutableSet` instead of `collections.abc.MutableSet` for type annotations.


### TYCO109

Use `typing.Mapping` instead of `collections.abc.Mapping` for type annotations.


### TYCO110

Use `typing.MutableMapping` instead of `collections.abc.MutableMapping` for type annotations.


### TYCO111

Use `typing.Sequence` instead of `collections.abc.Sequence` for type annotations.


### TYCO112

Use `typing.MutableSequence` instead of `collections.abc.MutableSequence` for type annotations.


### TYCO113

Use `typing.ByteString` instead of `bytes` for type annotations.


### TYCO114

Use `typing.Deque` instead of `collections.Deque` for type annotations.


### TYCO115

Use `typing.List` instead of `list` for type annotations.


### TYCO116

Use `typing.Set` instead of `set` for type annotations.


### TYCO117

Use `typing.FrozenSet` instead of `frozenset` for type annotations.


### TYCO118

Use `typing.MappingView` instead of `collections.abc.MappingView` for type annotations.


### TYCO119

Use `typing.KeysView` instead of `collections.abc.KeysView` for type annotations.


### TYCO120

Use `typing.ItemsView` instead of `collections.abc.ItemsView` for type annotations.


### TYCO121

Use `typing.ValuesView` instead of `collections.abc.ValuesView` for type annotations.


### TYCO122

Use `typing.Awaitable` instead of `collections.abc.Awaitable` for type annotations.


### TYCO123

Use `typing.Coroutine` instead of `collections.abc.Coroutine` for type annotations.


### TYCO124

Use `typing.AsyncIterable` instead of `collections.abc.AsyncIterable` for type annotations.


### TYCO125

Use `typing.AsyncIterator` instead of `collections.abc.AsyncIterator` for type annotations.


### TYCO126

Use `typing.ContextManager` instead of `contextlib.AbstractContextManager` for type annotations.


### TYCO127

Use `typing.AsyncContextManager` instead of `contextlib.AbstractAsyncContextManager` for type annotations.


### TYCO128

Use `typing.Dict` instead of `dict` for type annotations.


### TYCO129

Use `typing.DefaultDict` instead of `collections.defaultdict` for type annotations.


### TYCO130

Use `typing.OrderedDict` instead of `collections.OrderedDict` for type annotations.


### TYCO131

Use `typing.Counter` instead of `collections.Counter` for type annotations.


### TYCO132

Use `typing.ChainMap` instead of `collections.ChainMap` for type annotations.






## TYCO2xx class

The documentation of the `typing` module recommends to use
more general types such as `typing.Sequence` over specialized
types such as `typing.List` in function parameters.

```python
# Good
def sum_list(x: Sequence[int]) -> int:
    ...

# Bad
def sum_list(x: List[int]) -> int:
    ...
```

### TYCO200

Use `typing.Sequence` or `typing.MutableSequence`
instead of `typing.List` in function arguments.

### TYCO201

Use `typing.AbstractSet` or `typing.MutableSet`
instead of `typing.Set` in function arguments.

### TYCO201

Use `typing.Mapping` or `typing.MutableMapping`
instead of `typing.Dict` in function arguments.
