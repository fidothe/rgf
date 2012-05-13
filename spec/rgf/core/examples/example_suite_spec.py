from rgf.dsl import describe, it, before

from rgf.core.examples import ExampleGroup, ExampleSuite

class MockReporter(object):
    def __init__(self):
        self.examples_ran= []

    def example_ran(self, *args):
        self.examples_ran.append(args)

    def run_finished(self):
        self.run_finished_was_called = True

def first_test_function(world):
    world.has_been_run = True

def before_func(world):
    world.before_was_run = True

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

    @it('can set the ExampleSuite instance to be returned by get_suite()')
    def f(w):
        temp_suite = ExampleSuite()
        ExampleSuite.set_suite(temp_suite)
        assert ExampleSuite.get_suite() is temp_suite

    @it('can run run all its ExampleGroups')
    def spec(world):
        example_suite = ExampleSuite()
        example_group = example_suite.add_example_group('eg for explicit passing to it decorator')
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
