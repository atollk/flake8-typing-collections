from tests.util import BaseTest


class Test_TYCO202(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyco_general_args"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Mapping):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        import typing
        def foo(x) -> typing.Dict:
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import typing
        def foo(x: typing.Dict):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYCO202", 2, 12)
