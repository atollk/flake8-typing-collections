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
        return ["--tyc_generic_alt"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert self.error_at(errors, "TYC100", 4, 12)
        assert not self.error_at(errors, "TYC105", 4, 25)
        assert not self.error_at(errors, "TYC202", 4, 35)


class TestFlags_2(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyc_alias_alt"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert not self.error_at(errors, "TYC100", 4, 12)
        assert self.error_at(errors, "TYC105", 4, 25)
        assert not self.error_at(errors, "TYC202", 4, 35)


class TestFlags_3(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyc_general_args"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert not self.error_at(errors, "TYC100", 4, 12)
        assert not self.error_at(errors, "TYC105", 4, 25)
        assert self.error_at(errors, "TYC202", 4, 35)


class TestFlags_4(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyc_alias_alt", "--tyc_general_args"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert not self.error_at(errors, "TYC100", 4, 12)
        assert self.error_at(errors, "TYC105", 4, 25)
        assert self.error_at(errors, "TYC202", 4, 35)


class TestFlags_5(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyc_generic_alt", "--tyc_general_args"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert self.error_at(errors, "TYC100", 4, 12)
        assert not self.error_at(errors, "TYC105", 4, 25)
        assert self.error_at(errors, "TYC202", 4, 35)


class TestFlags_6(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyc_generic_alt", "--tyc_alias_alt"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert self.error_at(errors, "TYC100", 4, 12)
        assert self.error_at(errors, "TYC105", 4, 25)
        assert not self.error_at(errors, "TYC202", 4, 35)


class TestFlags_7(BaseTest):
    @classmethod
    def flags(cls) -> List[str]:
        return ["--tyc_generic_alt", "--tyc_alias_alt", "--tyc_general_args"]

    def test_flags(self):
        errors = self.run_flake8(CODE)
        assert self.error_at(errors, "TYC100", 4, 12)
        assert self.error_at(errors, "TYC105", 4, 25)
        assert self.error_at(errors, "TYC202", 4, 35)
