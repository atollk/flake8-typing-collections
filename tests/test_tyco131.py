
from tests.util import BaseTest

class Test_TYCO131(BaseTest):
    def error_code(self) -> str:
        return "TYCO131"

    def activate_flag(self) -> str:
        return "--tyco_generic_alt"

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Counter):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections
        def foo(x: collections.Counter):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO131", 2, 12)


    def test_fail_2(self):
        code = """
        from collections import Counter
        def foo(x) -> Counter:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO131", 2, 15)
