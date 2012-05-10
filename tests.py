import StringIO, sys, os.path
from rgf.core.examples import Example, ExampleGroup, ExampleSuite, ExampleResult
from rgf.core.runner import ProgressFormatter, Reporter, Collector
from rgf.dsl import describe, it, before

class MockExampleGroup(object):
    def run_before_each(self, example):
        def before(eg):
            eg.before_was_run = True
        before(example)

class MockExampleSuite(object):
    pass

class MockExample(object):
    pass

class MockReporter(object):
    def example_ran(self, *args):
        pass

    def run_finished(self):
        self.run_finished_was_called = True


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

def before_func(world):
    world.before_was_run = True

with describe('Example'):
    @it('can be run')
    def spec(world):
        first_example = Example("can be run", first_test_function)
        first_example.run(MockExampleGroup())
        assert first_example.has_been_run

    @it('is run with before func from context')
    def spec(world):
        second_example = Example("runs before method from context", first_test_function)
        second_example.run(MockExampleGroup())
        assert second_example.before_was_run

    @it('example reports its success Successful')
    def spec(world):
        third_example = Example("reports success", first_test_function)
        result = third_example.run(MockExampleGroup())
        assert type(result) == ExampleResult
        assert result.kind == 1
        assert result.traceback is None

    @it('example reports its error if it exploded')
    def spec(world):
        an_error = StandardError("An Error")
        def bad_test_function(self):
            raise an_error

        third_example = Example("reports error", bad_test_function)
        result = third_example.run(MockExampleGroup())
        assert type(result) == ExampleResult
        assert result.exception is an_error
        assert result.traceback is not None
        assert result.kind == 3

    @it('reports its error on failure')
    def spec(world):
        def failed_test_function(self):
            assert False

        fourth_example = Example("reports failure", failed_test_function)
        result = fourth_example.run(MockExampleGroup())
        assert type(result) == ExampleResult
        assert type(result.exception) is AssertionError
        assert result.traceback is not None
        assert result.kind == 2

with describe('ExampleGroup'):
    @it('can be created and described')
    def spec(world):
        eg = ExampleGroup(MockExampleSuite(), "A group of Examples")
        assert eg.description == "A group of Examples"

        # Examples can be grouped and run together
        eg = ExampleGroup(MockExampleSuite(), "")
        eg.add_example(Example('All good', first_test_function))
        eg.add_example(Example('Still good', first_test_function))
        eg.run(MockReporter())

        assert eg.examples[0].has_been_run
        assert eg.examples[1].has_been_run

    @it('can have setup code to be run before examples added')
    def spec(world):
        eg = ExampleGroup(MockExampleSuite(), '')
        eg.add_example(Example('All good', first_test_function))
        eg.add_example(Example('Still good', first_test_function))
        eg.before(before_func)
        eg.run(MockReporter())

        assert eg.examples[0].before_was_run
        assert eg.examples[1].before_was_run

with describe('ExampleSuite'):
    @it('can collect many ExampleGroups')
    def spec(world):
        suite = ExampleSuite()
        example_group = suite.add_example_group('ExampleGroup description')
        assert type(example_group) is ExampleGroup
        assert example_group in suite.example_groups

    @it('returns itself as the current ExampleGroup if there is none')
    def spec(world):
        suite = ExampleSuite()
        assert suite.get_current_example_group() is suite

    @it('allows the current ExampleGroup to be set')
    def spec(world):
        suite = ExampleSuite()
        example_group = suite.add_example_group('ExampleGroup description')
        suite.set_current_example_group(example_group)
        assert suite.get_current_example_group() is example_group

    @it('allows the current ExampleGroup to be popped off')
    def spec(world):
        suite = ExampleSuite()
        example_group = suite.add_example_group('ExampleGroup description')
        suite.set_current_example_group(example_group)
        suite.pop_current_example_group()
        assert suite.get_current_example_group() is suite

    @it('can create and return a single instance of itself')
    def spec(world):
        assert type(ExampleSuite.get_suite()) is ExampleSuite
        assert ExampleSuite.get_suite() is ExampleSuite.get_suite()

    @it('can run run all its ExampleGroups')
    def spec(world):
        example_suite = ExampleSuite()
        example_group = example_suite.add_example_group('eg for explicit passing to it decorator')
        example_group.print_run = True
        @it('has explicit ExampleGroup', example_group = example_group)
        def f(world):
            world.has_been_run = True

        example_suite.run(MockReporter())
        assert example_group.examples[0].has_been_run

    @it('tells the Reporter when the run has finished')
    def spec(world):
        example_suite = ExampleSuite()
        reporter = MockReporter()
        example_suite.run(reporter)
        assert reporter.run_finished_was_called

with describe('ExampleGroup context manager API'):
    @it('sets itself as the current example group in the suite on __enter__()')
    def spec(world):
        example_suite = ExampleSuite()
        example_group = ExampleGroup(example_suite, '__enter__ group')
        assert example_group.__enter__() is example_group
        assert example_suite.get_current_example_group() is example_group

    @it('removes itself as the current example group on __exit__()')
    def spec(world):
        example_suite = ExampleSuite()
        example_group = ExampleGroup(example_suite, '__exit__ group')
        example_suite.set_current_example_group(example_group)
        example_group.__exit__(None, None, None)
        assert example_suite.get_current_example_group() is example_suite

with describe('DSL'):
    @it('provides describe helper context to create and set current ExampleGroup')
    def spec(world):
        eg = describe('This Example Group')
        assert type(eg) is ExampleGroup

    @it('provides it() decorator creator. The decorator creates Examples on the current ExampleGroup')
    def spec(world):
        with describe('Example Group with examples added by it()') as eg:
            decorator = it('Example description created by it()')
            example = decorator(first_test_function)
            assert example.description == 'Example description created by it()'
            assert eg.examples == [example]

    @it("provides before() decorator creator. The decorator adds a function to the current ExampleGroup's before runner")
    def spec(world):
        with describe('Example Group with before function') as eg:
            before(before_func)
            assert eg.before_function is before_func

    @it('describe allows the parent of the ExampleGroup to be specified')
    def spec(world):
        example_suite = ExampleSuite()
        with describe('ExampleGroup with hard-wired parent', parent = example_suite) as eg:
            assert eg.parent is example_suite

    @it('allows the ExampleGroup to be explicitly passed to the the it decorator')
    def spec(world):
        example_suite = ExampleSuite()
        example_group = ExampleGroup(example_suite, 'eg for explicit passing to it() decorator')
        decorator = it('has explicit ExampleGroup', example_group = example_group)
        example = decorator(first_test_function)
        assert example_group.examples == [example]

with describe('ProgressFormatter'):
    @it('can log a success to an IO-like object')
    def spec(world):
        io = StringIO.StringIO()
        pf = ProgressFormatter(io)
        pf.success(MockExample(), (1, None))
        assert io.getvalue() == '.'

    @it('can log a failure to an IO-like object')
    def spec(world):
        io = StringIO.StringIO()
        pf = ProgressFormatter(io)
        pf.failure(MockExample(), (2, None))
        assert io.getvalue() == 'F'

    @it('can log an error to an IO-like object')
    def spec(world):
        io = StringIO.StringIO()
        pf = ProgressFormatter(io)
        pf.error(MockExample(), (3, None))
        assert io.getvalue() == 'E'

    @it('can summarise the results of running all examples')
    def spec(world):
        io = StringIO.StringIO()
        pf = ProgressFormatter(io)
        pf.summarise_results(total = 3, successes = 1, failures = 1, errors = 1)
        assert io.getvalue() == 'Ran 3 examples: 1 success, 1 failure, 1 error\n'

with describe('ProgressFormatter summarising Failures and Errors'):
    @before
    def b(world):
        def failed_test_function(self):
            assert False
        world.failing_example = Example("reports failure", failed_test_function)

        def error_test_function(self):
            raise KeyError('grrr')
        world.error_example = Example("reports error", error_test_function)

    @it('can summarise failures')
    def spec(world):
        result = world.failing_example.run(MockExampleGroup())
        io = StringIO.StringIO()
        pf = ProgressFormatter(io)
        pf.summarise_failures([(world.failing_example, result)])
        assert io.getvalue() != '' # there must be a better test than this which isn't terrifyingly brittle

    @it('can summarise errors')
    def spec(world):
        result = world.failing_example.run(MockExampleGroup())
        io = StringIO.StringIO()
        pf = ProgressFormatter(io)
        pf.summarise_errors([(world.error_example, result)])
        assert io.getvalue() != '' # there must be a better test than this which isn't terrifyingly brittle

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
        io = StringIO.StringIO()
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

with describe('Collector'):
    @it('can find spec files in a directory hierarchy')
    def f(w):
        actual = Collector(os.path.abspath('spec/fixtures/sample_spec_dir')).found_spec_files()
        expected = ['a_spec.py', 'b/b_spec.py', 'c/d/d_spec.py']
        expected = [os.path.abspath('spec/fixtures/sample_spec_dir/%s' % x) for x in expected]
        actual.sort()
        expected.sort()
        assert actual == expected

    @it('can import a spec file and collect its ExampleGroups')
    def f(w):
        spec_file_path = os.path.abspath('spec/fixtures/sample_spec_dir/b/b_spec.py')
        spec_root_path = os.path.abspath('spec/fixtures/sample_spec_dir')
        collector = Collector('/path/to/spec')
        mod = collector.import_spec_file(spec_file_path, root = spec_root_path)
        assert mod.__name__ == 'spec.b.b_spec'
        assert mod.__file__.index(spec_file_path) == 0

    @it('can import multiple spec files')
    def f(w):
        spec_root_path = os.path.abspath('spec/fixtures/sample_spec_dir')
        collector = Collector(spec_root_path)
        imported_files = []
        def mock_import_file_func(path, root):
            imported_files.append(path)
        collector.import_spec_file = mock_import_file_func
        collector.import_specs()
        expected = ['a_spec.py', 'b/b_spec.py', 'c/d/d_spec.py']
        expected = [os.path.abspath('spec/fixtures/sample_spec_dir/%s' % x) for x in expected]
        assert imported_files == expected

formatter = ProgressFormatter(sys.stdout)
reporter = Reporter(formatter)
ExampleSuite.get_suite().run(reporter)

# from future, import...
# Runner can collect and run spec files through a Reporter
# rgf script can create and run a runner
# --> At this point we can start to break up the tests into multiple files :-)
# Actually work out the language issues
# rgf script returns non-zero exit status if any specs failed
# --> At this point we can be used by a CI bot :-)
# ExampleGroups can be properly nested
# before-functions are properly dealt with in nested contexts
# ProgressFormatter can output coloured dots if asked
# DocumentationFormatter can output something like Rspec's specdoc format
# formatter can be chosen by passing an arg to rgf
# config can be extracted to a .rgf project file
# --> At this point we're probably useful
