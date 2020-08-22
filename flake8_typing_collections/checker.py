import argparse
import ast
import dataclasses
import itertools
from typing import Iterable, Tuple, Optional
from flake8_typing_collections import ast_import_decode

import flake8.options.manager

try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata


@dataclasses.dataclass
class Flags:
    generic_alt: bool
    alias_alt: bool
    general_args: bool


DEFAULT_FLAGS = Flags(generic_alt=True, alias_alt=False, general_args=True)

BETTER_ALTERNATIVES = {
    100: {"collections.abc.Iterable", "typing.Iterable"},
    101: {"collections.abc.Iterator", "typing.Iterator"},
    102: {"collections.abc.Reversible", "typing.Reversible"},
    103: {"collections.abc.Container", "typing.Container"},
    104: {"collections.abc.Hashable", "typing.Hashable"},
    105: {"collections.abc.Sized", "typing.Sized"},
    106: {"collections.abc.Collection", "typing.Collection"},
    107: {"collections.abc.Set", "typing.AbstractSet"},
    108: {"collections.abc.MutableSet", "typing.MutableSet"},
    109: {"collections.abc.Mapping", "typing.Mapping"},
    110: {"collections.abc.MutableMapping", "typing.MutableMapping"},
    111: {"collections.abc.Sequence", "typing.Sequence"},
    112: {"collections.abc.MutableSequence", "typing.MutableSequence"},
    113: {"bytes", "typing.ByteString"},
    114: {"collections.Deque", "typing.Deque"},
    115: {"list", "typing.List"},
    116: {"set", "typing.Set"},
    117: {"frozenset", "typing.FrozenSet"},
    118: {"collections.abc.MappingView", "typing.MappingView"},
    119: {"collections.abc.KeysView", "typing.KeysView"},
    120: {"collections.abc.ItemsView", "typing.ItemsView"},
    121: {"collections.abc.ValuesView", "typing.ValuesView"},
    122: {"collections.abc.Awaitable", "typing.Awaitable"},
    123: {"collections.abc.Coroutine", "typing.Coroutine"},
    124: {"collections.abc.AsyncIterable", "typing.AsyncIterable"},
    125: {"collections.abc.AsyncIterator", "typing.AsyncIterator"},
    126: {"contextlib.AbstractContextManager", "typing.ContextManager"},
    127: {
        "contextlib.AbstractAsyncContextManager",
        "typing.AsyncContextManager",
    },
    128: {"dict", "typing.Dict"},
    129: {"collections.defaultdict", "typing.DefaultDict"},
    130: {"collections.OrderedDict", "typing.OrderedDict"},
    131: {"collections.Counter", "typing.Counter"},
    132: {"collections.ChainMap", "typing.ChainMap"},
    200: {},
    201: {},
    203: {},
}


class Checker:
    """
    A flake8 plugin that checks the use of type alternatives from
    the `typing` module over actual run time types, especially from
    the `collections` module.
    """

    name = "flake8-typing-collections"
    version = metadata.version(name)
    flags = Flags(False, False, False)

    def __init__(self, tree: ast.AST):
        self.tree = tree

    @staticmethod
    def add_options(option_manager: flake8.options.manager.OptionManager):
        option_manager.add_option(
            "--tyco_generic_alt",
            action="store_true",
            help="Activate errors about generic type versions. See README.md for details.",
        )
        option_manager.add_option(
            "--tyco_alias_alt",
            action="store_true",
            help="Activate errors about alias type versions. See README.md for details.",
        )
        option_manager.add_option(
            "--tyco_general_args",
            action="store_true",
            help="Activate errors about more general types in function parameters. See README.md for details.",
        )

    @classmethod
    def parse_options(
        cls,
        option_manager: flake8.options.manager.OptionManager,
        options: argparse.Namespace,
        extra_args,
    ):
        cls.flags.generic_alt = options.tyco_generic_alt
        cls.flags.alias_alt = options.tyco_alias_alt
        cls.flags.general_args = options.tyco_general_args
        if not any(dataclasses.asdict(cls.flags).values()):
            cls.flags = DEFAULT_FLAGS

    def run(self) -> Iterable[Tuple[int, int, str, type]]:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.AnnAssign):
                yield from self._check_1xx(node.annotation)
            elif isinstance(node, ast.FunctionDef):
                yield from self._check_1xx(node.returns)
                args = node.args
                for arg in itertools.chain(
                    args.args,
                    args.posonlyargs,
                    args.kwonlyargs,
                    [args.vararg, args.kwarg],
                ):
                    yield from self._check_1xx(arg.annotation)
                    yield from self._check_2xx(arg.annotation)

    def _check_1xx(
        self, type_hint: Optional[ast.expr]
    ) -> Iterable[Tuple[int, int, str, type]]:
        if type_hint is None or any(
            type_hint.lineno == type_ignore.lineno
            for type_ignore in self.tree.type_ignores
        ):
            return []
        for error_code in range(100, 133):
            for ancestor in ast.walk(type_hint):
                yield from self._use_better_alternative(ancestor, error_code)

    def _check_2xx(
        self, type_hint: Optional[ast.expr]
    ) -> Iterable[Tuple[int, int, str, type]]:
        if type_hint is None or any(
            type_hint.lineno == type_ignore.lineno
            for type_ignore in self.tree.type_ignores
        ):
            return []
        yield from self._use_better_alternative(type_hint, 200)
        yield from self._use_better_alternative(type_hint, 201)
        yield from self._use_better_alternative(type_hint, 202)

    def _use_better_alternative(
        self, type_hint: ast.AST, error_code: int
    ) -> Iterable[Tuple[int, int, str, type]]:
        if isinstance(type_hint, ast.Name):
            if (
                ast_import_decode.decode(self.tree, type_hint)
                in BETTER_ALTERNATIVES
            ):
                yield (
                    type_hint.lineno,
                    type_hint.col_offset,
                    f"TYCO{error_code} " + ERROR_MESSAGES[error_code],
                    Checker,
                )


ERROR_MESSAGES = {
    100: "Use typing.Iterable instead of collections.abc.Iterable.",
    101: "Use typing.Iterator instead of collections.abc.Iterator.",
    102: "Use typing.Reversible instead of collections.abc.Reversible.",
    103: "Use typing.Container instead of collections.abc.Container.",
    104: "Use typing.Hashable instead of collections.abc.Hashable.",
    105: "Use typing.Sized instead of collections.abc.Sized.",
    106: "Use typing.Collection instead of collections.abc.Collection.",
    107: "Use typing.AbstractSet instead of collections.abc.Set.",
    108: "Use typing.MutableSet instead of collections.abc.MutableSet.",
    109: "Use typing.Mapping instead of collections.abc.Mapping.",
    110: "Use typing.MutableMapping instead of collections.abc.MutableMapping.",
    111: "Use typing.Sequence instead of collections.abc.Sequence.",
    112: "Use typing.MutableSequence instead of collections.abc.MutableSequence.",
    113: "Use typing.ByteString instead of bytes.",
    114: "Use typing.Deque instead of collections.Deque.",
    115: "Use typing.List instead of list.",
    116: "Use typing.Set instead of set.",
    117: "Use typing.FrozenSet instead of frozenset.",
    118: "Use typing.MappingView instead of collections.abc.MappingView.",
    119: "Use typing.KeysView instead of collections.abc.KeysView.",
    120: "Use typing.ItemsView instead of collections.abc.ItemsView.",
    121: "Use typing.ValuesView instead of collections.abc.ValuesView.",
    122: "Use typing.Awaitable instead of collections.abc.Awaitable.",
    123: "Use typing.Coroutine instead of collections.abc.Coroutine.",
    124: "Use typing.AsyncIterable instead of collections.abc.AsyncIterable.",
    125: "Use typing.AsyncIterator instead of collections.abc.AsyncIterator.",
    126: "Use typing.ContextManager instead of contextlib.AbstractContextManager.",
    127: "Use typing.AsyncContextManager instead of contextlib.AbstractAsyncContextManager.",
    128: "Use typing.Dict instead of dict.",
    129: "Use typing.DefaultDict instead of collections.defaultdict.",
    130: "Use typing.OrderedDict instead of collections.OrderedDict.",
    131: "Use typing.Counter instead of collections.Counter.",
    132: "Use typing.ChainMap instead of collections.ChainMap.",
    200: "TODO",
    201: "TODO",
    202: "TODO",
}
