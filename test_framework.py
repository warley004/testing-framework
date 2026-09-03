"""Implementação incremental de um framework de testes no estilo xUnit."""


class TestCase:
    """Classe-base para um único método de teste."""

    def __init__(self, test_method_name):
        self.test_method_name = test_method_name

    def run(self, result):
        result.test_started()
        self.set_up()
        try:
            test_method = getattr(self, self.test_method_name)
            test_method()
        except AssertionError:
            result.add_failure(self.test_method_name)
        except Exception:
            result.add_error(self.test_method_name)
        self.tear_down()

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def assert_equal(self, first, second):
        if first != second:
            raise AssertionError(f"{first} != {second}")

    def assert_true(self, expr):
        if not expr:
            raise AssertionError(f"{expr} is not true")

    def assert_false(self, expr):
        if expr:
            raise AssertionError(f"{expr} is not false")

    def assert_in(self, member, container):
        if member not in container:
            raise AssertionError(f"{member} not found in {container}")


class TestResult:
    """Sumariza a execução de uma coleção de testes."""

    RUN_MSG = "run"
    FAILURE_MSG = "failed"
    ERROR_MSG = "error"

    def __init__(self, suite_name=None):
        self.run_count = 0
        self.failures = []
        self.errors = []

    def test_started(self):
        self.run_count += 1

    def add_failure(self, test):
        self.failures.append(test)

    def add_error(self, test):
        self.errors.append(test)

    def summary(self):
        return (
            f"{self.run_count} {self.RUN_MSG}, "
            f"{len(self.failures)} {self.FAILURE_MSG}, "
            f"{len(self.errors)} {self.ERROR_MSG}"
        )


class TestSuite:
    """Coleção de casos de teste que possui a mesma interface de execução."""

    def __init__(self):
        self.tests = []

    def add_test(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class TestLoader:
    """Descobre métodos de teste e cria suítes para uma classe de teste."""

    TEST_METHOD_PREFIX = "test"

    def get_test_case_names(self, test_case_class):
        methods = dir(test_case_class)
        return [
            method
            for method in methods
            if method.startswith(self.TEST_METHOD_PREFIX)
        ]

    def make_suite(self, test_case_class):
        suite = TestSuite()
        for test_method_name in self.get_test_case_names(test_case_class):
            suite.add_test(test_case_class(test_method_name))
        return suite


class TestRunner:
    """Orquestra a execução de um caso ou suíte de testes."""

    def __init__(self):
        self.result = TestResult()

    def run(self, test):
        test.run(self.result)
        print(self.result.summary())
        return self.result
