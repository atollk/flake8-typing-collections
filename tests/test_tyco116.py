from tests.util import BaseTest


class Test_TYC116(BaseTest):
    @classmethod
    def flags(cls):
        return ["--tyc_generic_alt"]

    def test_pass_1(self):
        code = """
        import typing
        def foo(x: typing.Set):
            ...
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        def foo(x: set):
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC116", 2, 12)

    def test_fail_2(self):
        code = """
        def foo(x) -> set:
            ...
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "TYC116", 2, 15)
