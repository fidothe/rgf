from rgf.dsl import describe, it, before

from rgf.core.examples import ExampleGroup, ExampleSuite, Example

class MockExampleSuite(object):
    pass

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
