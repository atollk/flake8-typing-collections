from tests.util import BaseTest


class Test_TYC127(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyc_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.AsyncContextManager):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import contextlib
        def foo(x: contextlib.AbstractAsyncContextManager):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC127", 3, 12)

    def test_fail_2(self):
        code = """
        from contextlib import AbstractAsyncContextManager
        def foo(x) -> AbstractAsyncContextManager:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC127", 3, 15)
