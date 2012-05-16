import sys

from .example import Example

class ExampleContext(object):
    pass

class ExampleGroup(object):
    def __init__(self, parent, description):
        self.parent = parent
        self.examples = []
        self.example_groups = []
        self.description = description
        self.world_factory = ExampleContext
        self.before_function = None

    def add_example(self, example):
        self.examples.append(example)

    def add_example_group(self, description):
        example_group = ExampleGroup(self, description)
        self.example_groups.append(example_group)
        return example_group

    def before(self, before_function):
        self.before_function = before_function

    def run(self, reporter):
        all_examples_succeeded = True
        for example in self.examples:
            result = example.run(self, self.world_factory)
            if result.is_not_success(): all_examples_succeeded = False
            reporter.example_ran(example, result)

        for child in self.example_groups:
            if not child.run(reporter): all_examples_succeeded = False

        return all_examples_succeeded

    def run_before_each(self, example):
        self.parent.run_before_each(example)
        if self.before_function:
            self.before_function(example)

    def set_current_example_group(self, example_group):
        self.parent.set_current_example_group(example_group)

    def pop_current_example_group(self):
        self.parent.pop_current_example_group()

    def __enter__(self):
        self.parent.set_current_example_group(self)
        return self

    def __exit__(self, cls, value, traceback):
        self.parent.pop_current_example_group()

    def it(self, description):
        def example_creator(spec_function):
            example = Example(description, spec_function)
            self.add_example(example)
            return example
        return example_creator
