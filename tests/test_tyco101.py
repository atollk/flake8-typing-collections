
from tests.util import BaseTest

class Test_TYCO101(BaseTest):
    def error_code(self) -> str:
        return "TYCO101"

    def activate_flag(self) -> str:
        return "--tyco_generic_alt"

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Iterator):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections.abc
        def foo(x: collections.abc.Iterator):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO101", 2, 12)


    def test_fail_2(self):
        code = """
        from collections.abc import Iterator
        def foo(x) -> Iterator:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO101", 2, 15)
