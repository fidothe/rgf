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
    @before
    def b(w):
        w.suite = ExampleSuite()

    @it('can collect many ExampleGroups')
    def spec(w):
        example_group = w.suite.add_example_group('ExampleGroup description')
        assert type(example_group) is ExampleGroup
        assert example_group in w.suite.example_groups

    @it('returns itself as the current ExampleGroup if there is none')
    def spec(w):
        assert w.suite.get_current_example_group() is w.suite

    @it('allows the current ExampleGroup to be set')
    def spec(w):
        example_group = w.suite.add_example_group('ExampleGroup description')
        w.suite.set_current_example_group(example_group)
        assert w.suite.get_current_example_group() is example_group

    @it('allows the current ExampleGroup to be popped off')
    def spec(w):
        example_group = w.suite.add_example_group('ExampleGroup description')
        w.suite.set_current_example_group(example_group)
        w.suite.pop_current_example_group()
        assert w.suite.get_current_example_group() is w.suite

    @it('can create and return a single instance of itself')
    def spec(w):
        assert type(ExampleSuite.get_suite()) is ExampleSuite
        assert ExampleSuite.get_suite() is ExampleSuite.get_suite()

    @it('can set the ExampleSuite instance to be returned by get_suite()')
    def f(w):
        ExampleSuite.set_suite(w.suite)
        assert ExampleSuite.get_suite() is w.suite

    @it('can run run all its ExampleGroups')
    def spec(w):
        w.suite.add_example_group('eg for explicit passing to it decorator')
        example_group = w.suite.add_example_group('happy example group')
        @example_group.it('succeeds')
        def f(world):
            world.has_been_run = True

        w.suite.run(MockReporter())
        assert example_group.examples[0].has_been_run

    @it('tells the Reporter when the run has finished')
    def spec(w):
        reporter = MockReporter()
        w.suite.run(reporter)
        assert reporter.run_finished_was_called

    @it('returns True from run() if there were no failures')
    def f(w):
        example_group = w.suite.add_example_group('happy example group')
        @example_group.it('succeeds')
        def f(w):
            pass
        assert w.suite.run(MockReporter()) is True

