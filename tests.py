import StringIO
from rgf import Example, ExampleGroup, ExampleSuite, describe, it, before, ProgressFormatter, ExampleResult, Reporter

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

# Example can be run
def first_test_function(self):
    self.has_been_run = True

first_example = Example("can be run", first_test_function)
first_example.run(MockExampleGroup())
assert first_example.has_been_run

# Example is run with before func from context
second_example = Example("runs before method from context", first_test_function)
second_example.run(MockExampleGroup())
assert second_example.before_was_run

# Successful example reports its success
third_example = Example("reports success", first_test_function)
result = third_example.run(MockExampleGroup())
assert type(result) == ExampleResult
assert result.kind == 1
assert result.traceback is None

# Exploded example reports its error
an_error = StandardError("An Error")
def bad_test_function(self):
    raise an_error

third_example = Example("reports error", bad_test_function)
result = third_example.run(MockExampleGroup())
assert type(result) == ExampleResult
assert result.exception is an_error
assert result.traceback is not None
assert result.kind == 3

# Failed example reports its error
def failed_test_function(self):
    assert False

fourth_example = Example("reports failure", failed_test_function)
result = fourth_example.run(MockExampleGroup())
assert type(result) == ExampleResult
assert type(result.exception) is AssertionError
assert result.traceback is not None
assert result.kind == 2

# ExampleGroups can be created and described
eg = ExampleGroup(MockExampleSuite(), "A group of Examples")
assert eg.description == "A group of Examples"

# Examples can be grouped and run together
eg = ExampleGroup(MockExampleSuite(), "")
eg.add_example(Example('All good', first_test_function))
eg.add_example(Example('Still good', first_test_function))
eg.run(MockReporter())

assert eg.examples[0].has_been_run
assert eg.examples[1].has_been_run

# ExampleGroups can have setup code to be run before examples added
def before_func(world):
    world.before_was_run = True

eg = ExampleGroup(MockExampleSuite(), '')
eg.add_example(Example('All good', first_test_function))
eg.add_example(Example('Still good', first_test_function))
eg.add_before(before_func)
eg.run(MockReporter())

assert eg.examples[0].before_was_run
assert eg.examples[1].before_was_run

# ExampleSuite can collect many ExampleGroups
suite = ExampleSuite()
example_group = suite.add_example_group('ExampleGroup description')
assert type(example_group) is ExampleGroup
assert example_group in suite.example_groups

# ExampleSuite returns itself as the current ExampleGroup if there is none.
suite = ExampleSuite()
assert suite.get_current_example_group() is suite

# ExampleSuite allows the current ExampleGroup to be set
suite = ExampleSuite()
example_group = suite.add_example_group('ExampleGroup description')
suite.set_current_example_group(example_group)
assert suite.get_current_example_group() is example_group

# ExampleSuite allows the current ExampleGroup to be popped off
suite = ExampleSuite()
example_group = suite.add_example_group('ExampleGroup description')
suite.set_current_example_group(example_group)
suite.pop_current_example_group()
assert suite.get_current_example_group() is suite

# ExampleSuite can create and return a single instance of itself
assert type(ExampleSuite.get_suite()) is ExampleSuite
assert ExampleSuite.get_suite() is ExampleSuite.get_suite()

# An ExampleGroup responds to the context mangaer __enter__ API call and sets itself as the current example group in the suite
example_suite = ExampleSuite()
example_group = ExampleGroup(example_suite, '__enter__ group')
assert example_group.__enter__() is example_group
assert example_suite.get_current_example_group() is example_group

# An ExampleGroup responds to the context manage __exit__ API call and removes itself as the current example group
example_suite = ExampleSuite()
example_group = ExampleGroup(example_suite, '__exit__ group')
example_suite.set_current_example_group(example_group)
example_group.__exit__(None, None, None)
assert example_suite.get_current_example_group() is example_suite

# provide describe helper context to create and set current ExampleGroup
eg = describe('This Example Group')
assert type(eg) is ExampleGroup

# provide it() decorator creator. The decorator creates Examples on the current ExampleGroup
with describe('Example Group with examples added by it()') as eg:
    decorator = it('Example description created by it()')
    example = decorator(first_test_function)
    assert example.description == 'Example description created by it()'
    assert eg.examples == [example]

# provide before() decorator creator. The decorator adds a function to the current ExampleGroup's before runner
with describe('Example Group with before function') as eg:
    decorator = before()
    decorator(before_func)
    assert eg.before_function is before_func

# describe decorator allows the parent of the ExampleGroup to be specified
example_suite = ExampleSuite()
with describe('ExampleGroup with hard-wired parent', parent = example_suite) as eg:
    assert eg.parent is example_suite

# it decorator allows the ExampleGroup to be specified
example_suite = ExampleSuite()
example_group = ExampleGroup(example_suite, 'eg for explicit passing to it() decorator')
decorator = it('has explicit ExampleGroup', example_group = example_group)
example = decorator(first_test_function)
assert example_group.examples == [example]

# before decorator allows the ExampleGroup to be set
example_suite = ExampleSuite()
example_group = ExampleGroup(example_suite, 'eg for explicit passing to before() decorator')
decorator = before(example_group = example_group)
decorator(before_func)
assert example_group.before_function is before_func

# ExampleSuite.run() runs all its ExampleGroups
example_suite = ExampleSuite()
example_group = example_suite.add_example_group('eg for explicit passing to it decorator')
example_group.print_run = True
@it('has explicit ExampleGroup', example_group = example_group)
def f(world):
    world.has_been_run = True

example_suite.run(MockReporter())
assert example_group.examples[0].has_been_run

# ProgressFormatter can log a success to an IO-like object
io = StringIO.StringIO()
pf = ProgressFormatter(io)
pf.success(MockExample(), (1, None))
assert io.getvalue() == '.'

# ProgressFormatter can log a failure to an IO-like object
io = StringIO.StringIO()
pf = ProgressFormatter(io)
pf.failure(MockExample(), (2, None))
assert io.getvalue() == 'F'

# ProgressFormatter can log an error to an IO-like object
io = StringIO.StringIO()
pf = ProgressFormatter(io)
pf.error(MockExample(), (3, None))
assert io.getvalue() == 'E'

# ProgressFormatter can summarise the results of running all examples
io = StringIO.StringIO()
pf = ProgressFormatter(io)
pf.summarise_results(total = 3, successes = 1, failures = 1, errors = 1)
assert io.getvalue() == 'Ran 3 examples: 1 success, 1 failure, 1 error\n'

# ProgressFormatter can summarise failures
def failed_test_function(self):
    assert False
failing_example = Example("reports failure", failed_test_function)
result = failing_example.run(MockExampleGroup())
io = StringIO.StringIO()
pf = ProgressFormatter(io)
pf.summarise_failures([(failing_example, result)])
assert io.getvalue() != '' # there must be a better test than this which isn't terrifyingly brittle

# ProgressFormatter can summarise errors
def error_test_function(self):
    raise KeyError('grrr')
error_example = Example("reports error", error_test_function)
result = failing_example.run(MockExampleGroup())
io = StringIO.StringIO()
pf = ProgressFormatter(io)
pf.summarise_errors([(error_example, result)])
assert io.getvalue() != '' # there must be a better test than this which isn't terrifyingly brittle

# ExampleGroup.run reports its result
example_suite = ExampleSuite()
example_group = ExampleGroup(example_suite, 'reports')
ex1 = Example('All good', first_test_function)
ex2 = Example('Fail', failed_test_function)
ex3 = Example('Error', error_test_function)
example_group.add_example(ex1)
example_group.add_example(ex2)
example_group.add_example(ex3)
io = StringIO.StringIO()
formatter = MockFormatter()
reporter = Reporter(formatter)
example_group.run(reporter)

assert formatter.successes == [ex1]
assert formatter.failures == [ex2]
assert formatter.errors == [ex3]

# Reporter can report statistics
assert reporter.total_number_of_examples() == 3
assert reporter.number_of_successes() == 1
assert reporter.number_of_failures() == 1
assert reporter.number_of_errors() == 1

# Reporter uses its formatter to report status, summary and tracebacks for a run

# Once we get to this point we can self-host our single-file test run :-)
