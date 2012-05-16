from rgf.dsl import describe, it, before

from rgf.core.examples.example import Example
from rgf.core.examples.example_result import ExampleResult

class MockExampleGroup(object):
    def run_before_each(self, world):
        world.before_was_run = True

class MockExampleContext(object):
    pass

def passing_spec_function(world):
    world.has_been_run = True

def return_world(world):
    def returner():
        return world
    return returner

with describe('Example'):
    @before
    def b(w):
        w.mock_world = MockExampleContext()

    @it('can be run with an isolated context')
    def spec(w):
        example = Example("can be run", passing_spec_function)
        example.run(MockExampleGroup(), return_world(w.mock_world))
        assert w.mock_world.has_been_run

    @it('is run with before func from context')
    def spec(w):
        example = Example("runs before method from context", passing_spec_function)
        example.run(MockExampleGroup(), return_world(w.mock_world))
        assert w.mock_world.before_was_run

    @it('example reports its success Successful')
    def spec(w):
        example = Example("reports success", passing_spec_function)
        result = example.run(MockExampleGroup(), return_world(w.mock_world))
        assert type(result) == ExampleResult
        assert result.kind == 1
        assert result.traceback is None

    @it('example reports its error if it exploded')
    def spec(w):
        an_error = Exception("An Error")
        def bad_test_function(self):
            raise an_error

        example = Example("reports error", bad_test_function)
        result = example.run(MockExampleGroup(), return_world(w.mock_world))
        assert type(result) == ExampleResult
        assert result.exception is an_error
        assert result.traceback is not None
        assert result.kind == 3

    @it('reports its error on failure')
    def spec(w):
        def failed_test_function(self):
            assert False

        example = Example("reports failure", failed_test_function)
        result = example.run(MockExampleGroup(), return_world(w.mock_world))
        assert type(result) == ExampleResult
        assert type(result.exception) is AssertionError
        assert result.traceback is not None
        assert result.kind == 2
