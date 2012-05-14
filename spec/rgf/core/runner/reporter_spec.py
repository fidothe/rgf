from rgf.dsl import describe, it, before

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

def first_test_function(world):
    world.has_been_run = True

with describe('Reporter'):
    @before
    def b(world):
        def failing_test_function(self):
            assert False
        def error_test_function(self):
            raise KeyError('grrr')
        example_suite = ExampleSuite()
        example_group = ExampleGroup(example_suite, 'reports')
        world.ex1 = Example('All good', first_test_function)
        world.ex2 = Example('Fail', failing_test_function)
        world.ex3 = Example('Error', error_test_function)
        example_group.add_example(world.ex1)
        example_group.add_example(world.ex2)
        example_group.add_example(world.ex3)
        io = StringIO()
        world.mock_formatter = MockFormatter()
        world.reporter = Reporter(world.mock_formatter)
        example_group.run(world.reporter)

    @it('ExampleGroup.run reports its result')
    def spec(world):
        assert world.mock_formatter.successes == [world.ex1]
        assert world.mock_formatter.failures == [world.ex2]
        assert world.mock_formatter.errors == [world.ex3]

    @it('can report statistics')
    def spec(world):
        assert world.reporter.total_number_of_examples() == 3
        assert world.reporter.number_of_successes() == 1
        assert world.reporter.number_of_failures() == 1
        assert world.reporter.number_of_errors() == 1

    @it('uses its formatter to report status, summary and tracebacks for a run')
    def spec(world):
        world.reporter.run_finished()
        assert world.mock_formatter.summarise_results_called_with == (3, 1, 1, 1)
        assert len(world.mock_formatter.summarise_failures_called_with) == 1
        assert world.mock_formatter.summarise_failures_called_with[0][0] == world.ex2
        assert type(world.mock_formatter.summarise_failures_called_with[0][1]) == ExampleResult
        assert len(world.mock_formatter.summarise_errors_called_with) == 1
        assert world.mock_formatter.summarise_errors_called_with[0][0] == world.ex3
        assert type(world.mock_formatter.summarise_errors_called_with[0][1]) == ExampleResult
