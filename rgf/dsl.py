from rgf.core.examples import ExampleSuite, ExampleGroup, Example

__all__ = ['describe', 'subject', 'context', 'concern', 'it', 'before']

def _get_current_example_group():
    return ExampleSuite.get_suite().get_current_example_group()

def subject(description):
    parent = _get_current_example_group()
    new_example_group = parent.add_example_group(description)
    return new_example_group

describe = subject
context = subject
concern = subject

def it(description):
    example_group = _get_current_example_group()
    return example_group.it(description)

def before(before_function):
    example_group = _get_current_example_group()
    example_group.before(before_function)
