from rgf import Example

class MockExampleGroup(object):
    def run_before_each(self, example):
        def before(eg):
            eg.before_was_run = True
        before(example)

# Example can be run
def first_test_function(self):
    self.has_been_run = True

first_example = Example("can be run", first_test_function, MockExampleGroup())
first_example.run()
assert first_example.has_been_run

# Example is run with before func from context
second_example = Example("runs before method from context", first_test_function, MockExampleGroup())
second_example.run()
assert second_example.before_was_run
