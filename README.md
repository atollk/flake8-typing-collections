# flake8-typing-collections
A flake8 plugin that checks the use of type alternatives from
the `typing` module over actual run time types, especially from
the `collections` module.

## Options

The plugin offers the following flags to select which errors to enable.
All errors that are not explicitly enabled, are not reported.

* `--tyc_generic_alt`: Enables `TYC101`, `TYC102`, `TYC103`, `TYC106`, 
`TYC107`, `TYC108`, `TYC109`, `TYC110`, `TYC111`, `TYC112`, `TYC114`, 
`TYC115`, `TYC116`, `TYC117`, `TYC118`, `TYC119`, `TYC120`, `TYC121`, 
`TYC122`, `TYC123`, `TYC124`, `TYC125`, `TYC126`, `TYC127`, `TYC128`,
`TYC129`, `TYC130`, `TYC131`, and `TYC132`. 
* `--tyc_alias_alt`: Enables `TYC104`, `TYC105`, and `TYC113`.
* `--tyc_general_args`: Enables `TYC200`, `TYC201`, and `TYC202`.

If none of these flags is given, the default selection is used instead,
which is `--tyc_generic_alt` and `--tyc_general_args`.

## Error Codes

## TYC1xx class

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

### TYC100

Use `typing.Iterable` instead of `collections.abc.Iterable` for type annotations.


### TYC101

Use `typing.Iterator` instead of `collections.abc.Iterator` for type annotations.


### TYC102

Use `typing.Reversible` instead of `collections.abc.Reversible` for type annotations.


### TYC103

Use `typing.Container` instead of `collections.abc.Container` for type annotations.


### TYC104

Use `typing.Hashable` instead of `collections.abc.Hashable` for type annotations.


### TYC105

Use `typing.Sized` instead of `collections.abc.Sized` for type annotations.


### TYC106

Use `typing.Collection` instead of `collections.abc.Collection` for type annotations.


### TYC107

Use `typing.AbstractSet` instead of `collections.abc.Set` for type annotations.


### TYC108

Use `typing.MutableSet` instead of `collections.abc.MutableSet` for type annotations.


### TYC109

Use `typing.Mapping` instead of `collections.abc.Mapping` for type annotations.


### TYC110

Use `typing.MutableMapping` instead of `collections.abc.MutableMapping` for type annotations.


### TYC111

Use `typing.Sequence` instead of `collections.abc.Sequence` for type annotations.


### TYC112

Use `typing.MutableSequence` instead of `collections.abc.MutableSequence` for type annotations.


### TYC113

Use `typing.ByteString` instead of `bytes` for type annotations.


### TYC114

Use `typing.Deque` instead of `collections.Deque` for type annotations.


### TYC115

Use `typing.List` instead of `list` for type annotations.


### TYC116

Use `typing.Set` instead of `set` for type annotations.


### TYC117

Use `typing.FrozenSet` instead of `frozenset` for type annotations.


### TYC118

Use `typing.MappingView` instead of `collections.abc.MappingView` for type annotations.


### TYC119

Use `typing.KeysView` instead of `collections.abc.KeysView` for type annotations.


### TYC120

Use `typing.ItemsView` instead of `collections.abc.ItemsView` for type annotations.


### TYC121

Use `typing.ValuesView` instead of `collections.abc.ValuesView` for type annotations.


### TYC122

Use `typing.Awaitable` instead of `collections.abc.Awaitable` for type annotations.


### TYC123

Use `typing.Coroutine` instead of `collections.abc.Coroutine` for type annotations.


### TYC124

Use `typing.AsyncIterable` instead of `collections.abc.AsyncIterable` for type annotations.


### TYC125

Use `typing.AsyncIterator` instead of `collections.abc.AsyncIterator` for type annotations.


### TYC126

Use `typing.ContextManager` instead of `contextlib.AbstractContextManager` for type annotations.


### TYC127

Use `typing.AsyncContextManager` instead of `contextlib.AbstractAsyncContextManager` for type annotations.


### TYC128

Use `typing.Dict` instead of `dict` for type annotations.


### TYC129

Use `typing.DefaultDict` instead of `collections.defaultdict` for type annotations.


### TYC130

Use `typing.OrderedDict` instead of `collections.OrderedDict` for type annotations.


### TYC131

Use `typing.Counter` instead of `collections.Counter` for type annotations.


### TYC132

Use `typing.ChainMap` instead of `collections.ChainMap` for type annotations.






## TYC2xx class

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

### TYC200

Use `typing.Sequence` or `typing.MutableSequence`
instead of `typing.List` in function arguments.

### TYC201

Use `typing.AbstractSet` or `typing.MutableSet`
instead of `typing.Set` in function arguments.

### TYC201

Use `typing.Mapping` or `typing.MutableMapping`
instead of `typing.Dict` in function arguments.
