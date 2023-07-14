from tests.util import BaseTest


class Test_TYC103(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyc_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Container):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections.abc
        def foo(x: collections.abc.Container):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC103", 3, 12)

    def test_fail_2(self):
        code = """
        from collections.abc import Container
        def foo(x) -> Container:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC103", 3, 15)
