from tests.util import BaseTest


class Test_TYC200(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyc_general_args"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Sequence):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        import typing
        def foo(x) -> typing.List:
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import typing
        def foo(x: typing.List):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC200", 3, 12)
