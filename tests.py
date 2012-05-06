from rgf import Example, ExampleGroup, ExampleSuite, describe, it, before

class MockExampleGroup(object):
    def run_before_each(self, example):
        def before(eg):
            eg.before_was_run = True
        before(example)

class MockExampleSuite(object):
    pass

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
assert (1, None) == third_example.run(MockExampleGroup())

# Exploded example reports its error
an_error = StandardError("An Error")
def bad_test_function(self):
    raise an_error

third_example = Example("reports error", bad_test_function)
assert (3, an_error) == third_example.run(MockExampleGroup())

# Failed example reports its error
def failed_test_function(self):
    assert False

fourth_example = Example("reports failure", failed_test_function)
result = fourth_example.run(MockExampleGroup())
assert result[0] == 2
assert type(result[-1]) == AssertionError

# ExampleGroups can be created and described
eg = ExampleGroup(MockExampleSuite(), "A group of Examples")
assert eg.description == "A group of Examples"

# Examples can be grouped and run together
eg = ExampleGroup(MockExampleSuite(), "")
eg.add_example(Example('All good', first_test_function))
eg.add_example(Example('Still good', first_test_function))
eg.run()

assert eg.examples[0].has_been_run
assert eg.examples[1].has_been_run

# ExampleGroups can have setup code to be run before examples added
def before_func(world):
    world.before_was_run = True

eg = ExampleGroup(MockExampleSuite(), '')
eg.add_example(Example('All good', first_test_function))
eg.add_example(Example('Still good', first_test_function))
eg.add_before(before_func)
eg.run()

assert eg.examples[0].before_was_run
assert eg.examples[1].before_was_run

# ExampleGroup class provides a naive way to register an ExampleGroup instance as the 'current' example group
eg = ExampleGroup(MockExampleSuite(), '')
ExampleGroup.set_current_example_group(eg)

assert ExampleGroup.get_current_example_group() is eg

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
