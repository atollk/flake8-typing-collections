from tests.util import BaseTest


class Test_TYC132(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyc_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.ChainMap):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import collections
        def foo(x: collections.ChainMap):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC132", 2, 12)

    def test_fail_2(self):
        code = """
        from collections import ChainMap
        def foo(x) -> ChainMap:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC132", 2, 15)
