import argparse
import ast
import dataclasses
import itertools
from typing import Iterable, Optional, Tuple

import flake8.options.manager

from flake8_typing_collections import ast_import_decode

try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata


@dataclasses.dataclass
class Flags:
    generic_alt: bool
    alias_alt: bool
    general_args: bool


ERROR_CODES_GENERIC_ALT = {
    100,
    101,
    102,
    103,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    114,
    115,
    116,
    117,
    118,
    119,
    120,
    121,
    122,
    123,
    124,
    125,
    126,
    127,
    128,
    129,
    130,
    131,
    132,
}
ERROR_CODES_ALIAS_ALT = {104, 105, 113}
ERROR_CODES_GENERAL_ARGS = {200, 201, 202}


DEFAULT_FLAGS = Flags(generic_alt=True, alias_alt=False, general_args=True)

BETTER_ALTERNATIVES = {
    100: ["collections.abc.Iterable"],
    101: ["collections.abc.Iterator"],
    102: ["collections.abc.Reversible"],
    103: ["collections.abc.Container"],
    104: ["collections.abc.Hashable"],
    105: ["collections.abc.Sized"],
    106: ["collections.abc.Collection"],
    107: ["collections.abc.Set"],
    108: ["collections.abc.MutableSet"],
    109: ["collections.abc.Mapping"],
    110: ["collections.abc.MutableMapping"],
    111: ["collections.abc.Sequence"],
    112: ["collections.abc.MutableSequence"],
    113: ["bytes"],
    114: ["collections.Deque"],
    115: ["list"],
    116: ["set"],
    117: ["frozenset"],
    118: ["collections.abc.MappingView"],
    119: ["collections.abc.KeysView"],
    120: ["collections.abc.ItemsView"],
    121: ["collections.abc.ValuesView"],
    122: ["collections.abc.Awaitable"],
    123: ["collections.abc.Coroutine"],
    124: ["collections.abc.AsyncIterable"],
    125: ["collections.abc.AsyncIterator"],
    126: ["contextlib.AbstractContextManager"],
    127: ["contextlib.AbstractAsyncContextManager"],
    128: ["dict"],
    129: ["collections.defaultdict"],
    130: ["collections.OrderedDict"],
    131: ["collections.Counter"],
    132: ["collections.ChainMap"],
    200: ["typing.List"],
    201: ["typing.Set"],
    202: ["typing.Dict"],
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
            "--tyc_generic_alt",
            action="store_true",
            help="Activate errors about generic type versions. See README.md for details.",
        )
        option_manager.add_option(
            "--tyc_alias_alt",
            action="store_true",
            help="Activate errors about alias type versions. See README.md for details.",
        )
        option_manager.add_option(
            "--tyc_general_args",
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
        cls.flags.generic_alt = options.tyc_generic_alt
        cls.flags.alias_alt = options.tyc_alias_alt
        cls.flags.general_args = options.tyc_general_args
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
                    if arg is not None:
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
        if error_code in ERROR_CODES_GENERIC_ALT and not self.flags.generic_alt:
            return []
        if error_code in ERROR_CODES_ALIAS_ALT and not self.flags.alias_alt:
            return []
        if error_code in ERROR_CODES_GENERAL_ARGS and not self.flags.general_args:
            return []

        while isinstance(type_hint, ast.Subscript):
            type_hint = type_hint.value

        if isinstance(type_hint, ast.Name) or isinstance(type_hint, ast.Attribute):
            if (
                ast_import_decode.decode(self.tree, type_hint)
                in BETTER_ALTERNATIVES[error_code]
            ):
                yield (
                    type_hint.lineno,
                    type_hint.col_offset,
                    f"TYC{error_code} " + ERROR_MESSAGES[error_code],
                    Checker,
                )


ERROR_MESSAGES = {
    100: "Use typing.Iterable instead of collections.abc.Iterable in type annotations.",
    101: "Use typing.Iterator instead of collections.abc.Iterator in type annotations.",
    102: "Use typing.Reversible instead of collections.abc.Reversible in type annotations.",
    103: "Use typing.Container instead of collections.abc.Container in type annotations.",
    104: "Use typing.Hashable instead of collections.abc.Hashable in type annotations.",
    105: "Use typing.Sized instead of collections.abc.Sized in type annotations.",
    106: "Use typing.Collection instead of collections.abc.Collection in type annotations.",
    107: "Use typing.AbstractSet instead of collections.abc.Set in type annotations.",
    108: "Use typing.MutableSet instead of collections.abc.MutableSet in type annotations.",
    109: "Use typing.Mapping instead of collections.abc.Mapping in type annotations.",
    110: "Use typing.MutableMapping instead of collections.abc.MutableMapping in type annotations.",
    111: "Use typing.Sequence instead of collections.abc.Sequence in type annotations.",
    112: "Use typing.MutableSequence instead of collections.abc.MutableSequence in type annotations.",
    113: "Use typing.ByteString instead of bytes in type annotations.",
    114: "Use typing.Deque instead of collections.Deque in type annotations.",
    115: "Use typing.List instead of list in type annotations.",
    116: "Use typing.Set instead of set in type annotations.",
    117: "Use typing.FrozenSet instead of frozenset in type annotations.",
    118: "Use typing.MappingView instead of collections.abc.MappingView in type annotations.",
    119: "Use typing.KeysView instead of collections.abc.KeysView in type annotations.",
    120: "Use typing.ItemsView instead of collections.abc.ItemsView in type annotations.",
    121: "Use typing.ValuesView instead of collections.abc.ValuesView in type annotations.",
    122: "Use typing.Awaitable instead of collections.abc.Awaitable in type annotations.",
    123: "Use typing.Coroutine instead of collections.abc.Coroutine in type annotations.",
    124: "Use typing.AsyncIterable instead of collections.abc.AsyncIterable in type annotations.",
    125: "Use typing.AsyncIterator instead of collections.abc.AsyncIterator in type annotations.",
    126: "Use typing.ContextManager instead of contextlib.AbstractContextManager in type annotations.",
    127: "Use typing.AsyncContextManager instead of contextlib.AbstractAsyncContextManager in type annotations.",
    128: "Use typing.Dict instead of dict in type annotations.",
    129: "Use typing.DefaultDict instead of collections.defaultdict in type annotations.",
    130: "Use typing.OrderedDict instead of collections.OrderedDict in type annotations.",
    131: "Use typing.Counter instead of collections.Counter in type annotations.",
    132: "Use typing.ChainMap instead of collections.ChainMap in type annotations.",
    200: "Use typing.Sequence or typing.MutableSequence instead of typing.List in function arguments.",
    201: "Use typing.AbstractSet or typing.MutableSet instead of typing.Set in function arguments.",
    202: "Use typing.Mapping or typing.MutableMapping instead of typing.Dict in function arguments.",
}
