from tests.util import BaseTest


class Test_TYC105(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyc_alias_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Sized):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections.abc
        def foo(x: collections.abc.Sized):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC105", 2, 12)

    def test_fail_2(self):
        code = """
        from collections.abc import Sized
        def foo(x) -> Sized:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC105", 2, 15)
