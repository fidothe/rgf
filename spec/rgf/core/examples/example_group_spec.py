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

def failing_test_function(world):
    assert False

def before_func(world):
    world.before_was_run = True

with describe('ExampleGroup'):
    @before
    def b(w):
        w.eg = ExampleGroup(MockExampleSuite(), "A group of Examples")
        w.eg.add_example(Example('All good', first_test_function))
        w.eg.add_example(Example('Still good', first_test_function))

    @it('can be created and described')
    def spec(w):
        assert w.eg.description == "A group of Examples"

    @it('can group Examples and run them together')
    def spec(w):
        w.eg.run(MockReporter())

        assert w.eg.examples[0].has_been_run
        assert w.eg.examples[1].has_been_run

    @it('can have setup code to be run before examples added')
    def spec(w):
        w.eg.before(before_func)
        w.eg.run(MockReporter())

        assert w.eg.examples[0].before_was_run
        assert w.eg.examples[1].before_was_run

    @it('returns True if all Examples success')
    def spec(w):
        assert w.eg.run(MockReporter()) is True

    @it('returns False if any Examples fail')
    def spec(w):
        w.eg.add_example(Example('Not good', failing_test_function))
        assert w.eg.run(MockReporter()) is False

    @it('can generate a decorator around a new Example')
    def s(w):
        decorator = w.eg.it('Example description created by it()')
        example = decorator(first_test_function)
        assert example.description == 'Example description created by it()'
        assert example in w.eg.examples

with describe('ExampleGroup context manager API'):
    @before
    def b(w):
        w.example_suite = ExampleSuite()

    @it('sets itself as the current example group in the suite on __enter__()')
    def s(w):
        example_group = ExampleGroup(w.example_suite, '__enter__ group')
        assert example_group.__enter__() is example_group
        assert w.example_suite.get_current_example_group() is example_group

    @it('removes itself as the current example group on __exit__()')
    def s(w):
        example_group = ExampleGroup(w.example_suite, '__exit__ group')
        w.example_suite.set_current_example_group(example_group)
        example_group.__exit__(None, None, None)
        assert w.example_suite.get_current_example_group() is w.example_suite
