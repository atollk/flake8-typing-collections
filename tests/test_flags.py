import dataclasses
import itertools
import re
import textwrap
from typing import List, Tuple

import pytest

CODE = """
from collections.abc import Iterable, Sized
from typing import Dict
def foo(a: Iterable, b: Sized, c: Dict):
    ... 
"""


@dataclasses.dataclass
class ReportedMessage:
    file: str
    line: int
    col: int
    code: str
    message: str

    @staticmethod
    def from_raw(report: str) -> "ReportedMessage":
        m = re.match(r"(.*?):(\d+):(\d+): ((?:\w|\d)+) (.*)", report)
        return ReportedMessage(m[1], int(m[2]), int(m[3]), m[4], m[5])


def run_flake8(flake8dir, flags: List[str], code: str) -> List[ReportedMessage]:
    flake8dir.make_example_py(textwrap.dedent(code))
    result = flake8dir.run_flake8(flags)
    all_errors = [
        ReportedMessage.from_raw(report) for report in result.out_lines
    ]
    return [err for err in all_errors if err.code.startswith("TYCO")]


def iff(a: bool, b: bool) -> bool:
    return (a and b) or (not a and not b)


@pytest.mark.parametrize(
    ["generic_alt", "alias_alt", "general_args"],
    [
        (True, False, False),
        (False, True, False),
        (False, False, True),
        (True, True, False),
        (True, False, True),
        (False, True, True),
        (True, True, True),
    ],
)
def test_flags(flake8dir, generic_alt, alias_alt, general_args):
    flags = []
    if generic_alt:
        flags.append("--tyco_generic_alt")
    if alias_alt:
        flags.append("--tyco_alias_alt")
    if general_args:
        flags.append("--tyco_general_args")

    errors = run_flake8(flake8dir, list(flags), CODE)
    assert iff(generic_alt, error_at(errors, "TYCO100", 3, 12))
    assert iff(alias_alt, error_at(errors, "TYCO105", 3, 25))
    assert iff(general_args, error_at(errors, "TYCO202", 3, 35))


def error_at(
    reported_errors: List[ReportedMessage],
    error_code: str,
    line: int,
    col: int,
) -> bool:
    return any(
        report.line == line and report.col == col and report.code == error_code
        for report in reported_errors
    )
