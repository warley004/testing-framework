"""Testes do framework construídos com o próprio framework."""

from test_framework import TestCase, TestResult


class TestStub(TestCase):
    def test_success(self):
        assert True

    def test_failure(self):
        assert False

    def test_error(self):
        raise Exception


class TestSpy(TestCase):
    def __init__(self, name):
        super().__init__(name)
        self.was_run = False
        self.was_set_up = False
        self.was_tear_down = False
        self.log = ""

    def set_up(self):
        self.was_set_up = True
        self.log += "set_up "

    def test_method(self):
        self.was_run = True
        self.log += "test_method "

    def tear_down(self):
        self.was_tear_down = True
        self.log += "tear_down"


class TestCaseTest(TestCase):
    def set_up(self):
        self.result = TestResult()

    def test_result_success_run(self):
        TestStub("test_success").run(self.result)
        assert self.result.summary() == "1 run, 0 failed, 0 error"

    def test_result_failure_run(self):
        TestStub("test_failure").run(self.result)
        assert self.result.summary() == "1 run, 1 failed, 0 error"

    def test_result_error_run(self):
        TestStub("test_error").run(self.result)
        assert self.result.summary() == "1 run, 0 failed, 1 error"

    def test_result_multiple_run(self):
        for test_name in ("test_success", "test_failure", "test_error"):
            TestStub(test_name).run(self.result)
        assert self.result.summary() == "3 run, 1 failed, 1 error"

    def test_was_set_up(self):
        spy = TestSpy("test_method")
        spy.run(self.result)
        assert spy.was_set_up

    def test_was_run(self):
        spy = TestSpy("test_method")
        spy.run(self.result)
        assert spy.was_run

    def test_was_tear_down(self):
        spy = TestSpy("test_method")
        spy.run(self.result)
        assert spy.was_tear_down

    def test_template_method(self):
        spy = TestSpy("test_method")
        spy.run(self.result)
        assert spy.log == "set_up test_method tear_down"


if __name__ == "__main__":
    result = TestResult()
    for test_name in (
        "test_result_success_run",
        "test_result_failure_run",
        "test_result_error_run",
        "test_result_multiple_run",
        "test_was_set_up",
        "test_was_run",
        "test_was_tear_down",
        "test_template_method",
    ):
        TestCaseTest(test_name).run(result)
    print(result.summary())
