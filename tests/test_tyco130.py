from tests.util import BaseTest


class Test_TYCO130(BaseTest):
    def error_code(self) -> str:
        return "TYCO130"

    def activate_flag(self) -> str:
        return "--tyco_generic_alt"

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.OrderedDict):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections
        def foo(x: collections.OrderedDict):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO130", 2, 12)

    def test_fail_2(self):
        code = """
        from collections import OrderedDict
        def foo(x) -> OrderedDict:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO130", 2, 15)
