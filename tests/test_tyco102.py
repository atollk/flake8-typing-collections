from tests.util import BaseTest


class Test_TYC102(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyc_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Reversible):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections.abc
        def foo(x: collections.abc.Reversible):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC102", 2, 12)

    def test_fail_2(self):
        code = """
        from collections.abc import Reversible
        def foo(x) -> Reversible:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC102", 2, 15)
