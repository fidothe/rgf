from rgf.dsl import *

try:
    from StringIO import BytesIO as StringIO
except ImportError:
    from io import StringIO

from rgf.core.examples import ExampleSuite, ExampleGroup, Example, ExampleResult
from rgf.core.runner import Reporter

class MockFormatter(object):
    def __init__(self):
        self.successes = []
        self.failures = []
        self.errors = []

    def success(self, example, result):
        self.successes.append(example)

    def failure(self, example, result):
        self.failures.append(example)

    def error(self, example, result):
        self.errors.append(example)

    def summarise_results(self, *args):
        self.summarise_results_called_with = args

    def summarise_failures(self, failures):
        self.summarise_failures_called_with = failures

    def summarise_errors(self, errors):
        self.summarise_errors_called_with = errors

def first_test_function(w):
    w.has_been_run = True

with subject('Reporter'):
    @before
    def b(w):
        def failing_test_function(self):
            assert False
        def error_test_function(self):
            raise KeyError('grrr')
        example_suite = ExampleSuite()
        example_group = ExampleGroup(example_suite, 'reports')
        w.ex1 = Example('All good', first_test_function)
        w.ex2 = Example('Fail', failing_test_function)
        w.ex3 = Example('Error', error_test_function)
        example_group.add_example(w.ex1)
        example_group.add_example(w.ex2)
        example_group.add_example(w.ex3)
        io = StringIO()
        w.mock_formatter = MockFormatter()
        w.reporter = Reporter(w.mock_formatter)
        example_group.run(w.reporter)

    @it('ExampleGroup.run reports its result')
    def s(w):
        assert w.mock_formatter.successes == [w.ex1]
        assert w.mock_formatter.failures == [w.ex2]
        assert w.mock_formatter.errors == [w.ex3]

    @it('can report statistics')
    def s(w):
        assert w.reporter.total_number_of_examples() == 3
        assert w.reporter.number_of_successes() == 1
        assert w.reporter.number_of_failures() == 1
        assert w.reporter.number_of_errors() == 1

    @it('uses its formatter to report status, summary and tracebacks for a run')
    def s(w):
        w.reporter.run_finished()
        assert w.mock_formatter.summarise_results_called_with == (3, 1, 1, 1)
        assert len(w.mock_formatter.summarise_failures_called_with) == 1
        assert w.mock_formatter.summarise_failures_called_with[0][0] == w.ex2
        assert type(w.mock_formatter.summarise_failures_called_with[0][1]) == ExampleResult
        assert len(w.mock_formatter.summarise_errors_called_with) == 1
        assert w.mock_formatter.summarise_errors_called_with[0][0] == w.ex3
        assert type(w.mock_formatter.summarise_errors_called_with[0][1]) == ExampleResult
