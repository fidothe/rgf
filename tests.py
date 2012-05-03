from rgf import Example, ExampleGroup

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

# Successful example reports its success
third_example = Example("reports success", first_test_function, MockExampleGroup())
assert (1, None) == third_example.run()

# Exploded example reports its error
an_error = StandardError("An Error")
def bad_test_function(self):
    raise an_error

third_example = Example("reports error", bad_test_function, MockExampleGroup())
assert (3, an_error) == third_example.run()

# Failed example reports its error
def failed_test_function(self):
    assert False

fourth_example = Example("reports failure", failed_test_function, MockExampleGroup())
result = fourth_example.run()
assert result[0] == 2
assert type(result[-1]) == AssertionError

# Examples can be grouped and run together
eg = ExampleGroup()
eg.add_example(Example('All good', first_test_function, eg))
eg.add_example(Example('Still good', first_test_function, eg))
eg.run()

assert eg.examples[0].has_been_run
assert eg.examples[1].has_been_run
