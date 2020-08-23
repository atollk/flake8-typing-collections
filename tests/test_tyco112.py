from tests.util import BaseTest


class Test_TYCO112(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyco_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.MutableSequence):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections.abc
        def foo(x: collections.abc.MutableSequence):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO112", 2, 12)

    def test_fail_2(self):
        code = """
        from collections.abc import MutableSequence
        def foo(x) -> MutableSequence:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO112", 2, 15)
