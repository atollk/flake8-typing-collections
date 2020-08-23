from tests.util import BaseTest


class Test_TYCO115(BaseTest):
    def error_code(self) -> str:
        return "TYCO115"

    def activate_flag(self) -> str:
        return "--tyco_generic_alt"

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.List):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        def foo(x: list):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO115", 1, 12)

    def test_fail_2(self):
        code = """
        def foo(x) -> list:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO115", 1, 15)
