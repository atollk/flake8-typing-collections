from tests.util import BaseTest


class Test_TYCO126(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyco_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.ContextManager):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import contextlib
        def foo(x: contextlib.AbstractContextManager):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO126", 2, 12)

    def test_fail_2(self):
        code = """
        from contextlib import AbstractContextManager
        def foo(x) -> AbstractContextManager:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO126", 2, 15)
