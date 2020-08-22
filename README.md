# flake8-typing-suggestions
A flake8 plugin that checks the use of suggestions made by the official documentation of the "typing" module.

## Options

The plugin offers one flag, `--select_tysu`, accepting a list of error
codes (see below) to be enabled. By default, the enabled errors
are TODO

## Error Codes

## TYSU1xx class

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

### TYSU100

Use `typing.Iterable` instead of `collections.abc.Iterable` for type annotations.


### TYSU101

Use `typing.Iterator` instead of `collections.abc.Iterator` for type annotations.


### TYSU102

Use `typing.Reversible` instead of `collections.abc.Reversible` for type annotations.


### TYSU103

Use `typing.Container` instead of `collections.abc.Container` for type annotations.


### TYSU104

Use `typing.Hashable` instead of `collections.abc.Hashable` for type annotations.


### TYSU105

Use `typing.Sized` instead of `collections.abc.Sized` for type annotations.


### TYSU106

Use `typing.Collection` instead of `collections.abc.Collection` for type annotations.


### TYSU107

Use `typing.AbstractSet` instead of `collections.abc.Set` for type annotations.


### TYSU108

Use `typing.MutableSet` instead of `collections.abc.MutableSet` for type annotations.


### TYSU109

Use `typing.Mapping` instead of `collections.abc.Mapping` for type annotations.


### TYSU110

Use `typing.MutableMapping` instead of `collections.abc.MutableMapping` for type annotations.


### TYSU111

Use `typing.Sequence` instead of `collections.abc.Sequence` for type annotations.


### TYSU112

Use `typing.MutableSequence` instead of `collections.abc.MutableSequence` for type annotations.


### TYSU113

Use `typing.ByteString` instead of `bytes` for type annotations.


### TYSU114

Use `typing.Deque` instead of `collections.Deque` for type annotations.


### TYSU115

Use `typing.List` instead of `list` for type annotations.


### TYSU116

Use `typing.Set` instead of `set` for type annotations.


### TYSU117

Use `typing.FrozenSet` instead of `frozenset` for type annotations.


### TYSU118

Use `typing.MappingView` instead of `collections.abc.MappingView` for type annotations.


### TYSU119

Use `typing.KeysView` instead of `collections.abc.KeysView` for type annotations.


### TYSU120

Use `typing.ItemsView` instead of `collections.abc.ItemsView` for type annotations.


### TYSU121

Use `typing.ValuesView` instead of `collections.abc.ValuesView` for type annotations.


### TYSU122

Use `typing.Awaitable` instead of `collections.abc.Awaitable` for type annotations.


### TYSU123

Use `typing.Coroutine` instead of `collections.abc.Coroutine` for type annotations.


### TYSU124

Use `typing.AsyncIterable` instead of `collections.abc.AsyncIterable` for type annotations.


### TYSU125

Use `typing.AsyncIterator` instead of `collections.abc.AsyncIterator` for type annotations.


### TYSU126

Use `typing.ContextManager` instead of `contextlib.AbstractContextManager` for type annotations.


### TYSU127

Use `typing.AsyncContextManager` instead of `contextlib.AbstractAsyncContextManager` for type annotations.


### TYSU128

Use `typing.Dict` instead of `dict` for type annotations.


### TYSU129

Use `typing.DefaultDict` instead of `collections.defaultdict` for type annotations.


### TYSU130

Use `typing.OrderedDict` instead of `collections.OrderedDict` for type annotations.


### TYSU131

Use `typing.Counter` instead of `collections.Counter` for type annotations.


### TYSU132

Use `typing.ChainMap` instead of `collections.ChainMap` for type annotations.






## TYSU2xx class

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

### TYSU200

Use `typing.Sequence` or `typing.MutableSequence`
instead of `typing.List` in function arguments.

### TYSU201

Use `typing.AbstractSet` or `typing.MutableSet`
instead of `typing.Set` in function arguments.

### TYSU201

Use `typing.Mapping` or `typing.MutableMapping`
instead of `typing.Dict` in function arguments.
