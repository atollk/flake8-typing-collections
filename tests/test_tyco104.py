from tests.util import BaseTest


class Test_TYCO104(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyco_alias_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Hashable):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections.abc
        def foo(x: collections.abc.Hashable):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO104", 2, 12)

    def test_fail_2(self):
        code = """
        from collections.abc import Hashable
        def foo(x) -> Hashable:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO104", 2, 15)
