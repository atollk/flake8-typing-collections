import abc
import dataclasses
import re
import textwrap
from typing import List

import pytest


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


class BaseTest(abc.ABC):
    @classmethod
    def flags(cls) -> List[str]:
        return []

    @pytest.fixture(autouse=True)
    def _flake8dir(self, flake8_path):
        self.flake8_path = flake8_path

    def run_flake8(self, code: str) -> List[ReportedMessage]:
        (self.flake8_path / "example.py").write_text(textwrap.dedent(code))
        args = self.flags()
        result = self.flake8_path.run_flake8(args)
        all_errors = [
            ReportedMessage.from_raw(report) for report in result.out_lines
        ]
        return [err for err in all_errors if err.code.startswith("TYC")]

    def assert_error_at(
        self,
        reported_errors: List[ReportedMessage],
        error_code: str,
        line: int,
        col: int,
    ) -> None:
        assert self.error_at(
            reported_errors, error_code, line, col
        ), f"No error with code {error_code} at {line}:{col} found. Reported errors are: {reported_errors}"

    def error_at(
        self,
        reported_errors: List[ReportedMessage],
        error_code: str,
        line: int,
        col: int,
    ) -> bool:
        return any(
            report.line == line
            and report.col == col
            and report.code == error_code
            for report in reported_errors
        )
