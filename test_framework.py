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
