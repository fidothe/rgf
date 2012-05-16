from .example_group import ExampleGroup

try:
    # Python 3k
    from functools import reduce
except ImportError:
    # Built in function in Python 2
    pass

class ExampleSuite(object):
    @classmethod
    def get_suite(cls):
        if hasattr(cls, 'example_suite'): return cls.example_suite
        cls.example_suite = ExampleSuite()
        return cls.example_suite

    @classmethod
    def set_suite(cls, suite):
        cls.example_suite = suite

    def __init__(self):
        self.example_groups = []
        self.current_example_group_stack = [self]

    def add_example_group(self, description):
        example_group = ExampleGroup(self, description)
        self.example_groups.append(example_group)
        return example_group

    def set_current_example_group(self, example_group):
        self.current_example_group_stack.append(example_group)

    def get_current_example_group(self):
        return self.current_example_group_stack[-1]

    def pop_current_example_group(self):
        self.current_example_group_stack.pop()

    def run(self, reporter):
        results = [example_group.run(reporter) for example_group in self.example_groups]
        reporter.run_finished()
        def all_succeeded(start_state, current_state):
            return start_state and current_state
        return reduce(all_succeeded, results, True)

    def run_before_each(self, example):
        pass
