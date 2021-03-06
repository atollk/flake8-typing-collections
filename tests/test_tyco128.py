from tests.util import BaseTest


class Test_TYCO128(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyco_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Dict):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        def foo(x: dict):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO128", 1, 12)

    def test_fail_2(self):
        code = """
        def foo(x) -> dict:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO128", 1, 15)
