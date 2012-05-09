from rgf.core.examples import ExampleSuite, ExampleGroup, Example

def _get_current_example_group():
    return ExampleSuite.get_suite().get_current_example_group()

def describe(description, parent = None):
    if parent is None:
        parent = _get_current_example_group()
    new_example_group = parent.add_example_group(description)
    return new_example_group

def it(description, example_group = None):
    if example_group is None:
        example_group = _get_current_example_group()
    def example_creator(spec_function):
        example = Example(description, spec_function)
        example_group.add_example(example)
        return example
    return example_creator

def before(before_function):
    example_group = _get_current_example_group()
    example_group.before(before_function)
