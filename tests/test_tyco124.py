from tests.util import BaseTest


class Test_TYCO124(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyco_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.AsyncIterable):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections.abc
        def foo(x: collections.abc.AsyncIterable):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO124", 2, 12)

    def test_fail_2(self):
        code = """
        from collections.abc import AsyncIterable
        def foo(x) -> AsyncIterable:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO124", 2, 15)
