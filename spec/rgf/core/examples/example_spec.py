from rgf.dsl import describe, it, before

from rgf.core.examples import Example, ExampleResult

class MockExampleGroup(object):
    def run_before_each(self, example):
        def before(eg):
            eg.before_was_run = True
        before(example)

def first_test_function(world):
    world.has_been_run = True

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
        an_error = Exception("An Error")
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
