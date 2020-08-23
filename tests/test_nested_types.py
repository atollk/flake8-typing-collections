from tests.util import BaseTest

CODE_NESTED_OUTER = """
def foo(x: list[int]):
    ...
"""

CODE_NESTED_INNER = """
import typing
def foo(x: typing.Collection[list]):
    ...
"""

CODE_NESTED_2XX = """
import typing
def foo(x: typing.List[int]):
    ...
def bar(x: typing.Optional[typing.List]):
    ...
"""


class TestNestedTypes(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyco_generic_alt", "--tyco_alias_alt", "--tyco_general_args"]

    def test_nested_outer(self):
        errors = self.run_flake8(CODE_NESTED_OUTER)
        self.assert_error_at(errors, "TYCO115", 1, 12)

    def test_nested_inner(self):
        errors = self.run_flake8(CODE_NESTED_INNER)
        self.assert_error_at(errors, "TYCO115", 2, 30)

    def test_nested_2xx(self):
        errors = self.run_flake8(CODE_NESTED_2XX)
        self.assert_error_at(errors, "TYCO200", 2, 12)
        assert len(errors) == 1, str(errors)
