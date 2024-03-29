from tests.util import BaseTest


class Test_TYC106(BaseTest):
    def error_code(self) -> str:
        return "TYC106"

    @classmethod
    def flags(cls):
        return ["--tyc_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Collection):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections.abc
        def foo(x: collections.abc.Collection):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC106", 3, 12)

    def test_fail_2(self):
        code = """
        from collections.abc import Collection
        def foo(x) -> Collection:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC106", 3, 15)
