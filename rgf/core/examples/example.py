import sys

from .example_result import ExampleResult

class Example(object):
    def __init__(self, description, spec_function):
        self.spec_function = spec_function
        self.description = description

    def run(self, example_group, world_factory):
        world = world_factory()
        example_group.run_before_each(world)
        try:
            self.spec_function(world)
            return ExampleResult.as_success()
        except AssertionError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            return ExampleResult.as_failure(exc_value, exc_traceback)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            return ExampleResult.as_error(exc_value, exc_traceback)
