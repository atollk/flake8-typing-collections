from tests.util import BaseTest


class Test_TYCO108(BaseTest):
    def error_code(self) -> str:
        return "TYCO108"

    def activate_flag(self) -> str:
        return "--tyco_generic_alt"

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.MutableSet):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections.abc
        def foo(x: collections.abc.MutableSet):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO108", 2, 12)

    def test_fail_2(self):
        code = """
        from collections.abc import MutableSet
        def foo(x) -> MutableSet:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO108", 2, 15)
