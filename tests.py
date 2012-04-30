from rgf import Example

# Example can be run
def first_test_function(self):
    self.has_been_run = True

first_example = Example("can be run", first_test_function)
first_example.run()
assert first_example.has_been_run
