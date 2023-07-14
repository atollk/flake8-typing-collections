from tests.util import BaseTest


class Test_TYC129(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyc_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.DefaultDict):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections
        def foo(x: collections.defaultdict):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC129", 3, 12)

    def test_fail_2(self):
        code = """
        from collections import defaultdict
        def foo(x) -> defaultdict:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC129", 3, 15)
