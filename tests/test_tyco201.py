from tests.util import BaseTest


class Test_TYCO201(BaseTest):
    def error_code(self) -> str:
        return "TYCO201"

    def activate_flag(self) -> str:
        return "--tyco_general_args"

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.AbstractSet):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        import typing
        def foo(x) -> typing.Set:
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import typing
        def foo(x: typing.Set):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO201", 2, 12)
