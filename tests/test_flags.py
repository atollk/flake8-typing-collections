from typing import List, Tuple

import pytest

from tests.util import BaseTest

CODE = """
from collections.abc import Iterable, Sized
from typing import Dict
def foo(a: Iterable, b: Sized, c: Dict):
    ... 
"""


class TestFlags_1(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyco_generic_alt"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert self.error_at(errors, "TYCO100", 3, 12)
        assert not self.error_at(errors, "TYCO105", 3, 25)
        assert not self.error_at(errors, "TYCO202", 3, 35)


class TestFlags_2(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyco_alias_alt"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert not self.error_at(errors, "TYCO100", 3, 12)
        assert self.error_at(errors, "TYCO105", 3, 25)
        assert not self.error_at(errors, "TYCO202", 3, 35)


class TestFlags_3(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyco_general_args"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert not self.error_at(errors, "TYCO100", 3, 12)
        assert not self.error_at(errors, "TYCO105", 3, 25)
        assert self.error_at(errors, "TYCO202", 3, 35)


class TestFlags_4(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyco_alias_alt", "--tyco_general_args"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert not self.error_at(errors, "TYCO100", 3, 12)
        assert self.error_at(errors, "TYCO105", 3, 25)
        assert self.error_at(errors, "TYCO202", 3, 35)


class TestFlags_5(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyco_generic_alt", "--tyco_general_args"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert self.error_at(errors, "TYCO100", 3, 12)
        assert not self.error_at(errors, "TYCO105", 3, 25)
        assert self.error_at(errors, "TYCO202", 3, 35)


class TestFlags_6(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyco_generic_alt", "--tyco_alias_alt"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert self.error_at(errors, "TYCO100", 3, 12)
        assert self.error_at(errors, "TYCO105", 3, 25)
        assert not self.error_at(errors, "TYCO202", 3, 35)


class TestFlags_7(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyco_generic_alt", "--tyco_alias_alt", "--tyco_general_args"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert self.error_at(errors, "TYCO100", 3, 12)
        assert self.error_at(errors, "TYCO105", 3, 25)
        assert self.error_at(errors, "TYCO202", 3, 35)
