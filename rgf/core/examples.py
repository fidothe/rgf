import sys

class Example(object):
    def __init__(self, description, spec_function):
        self.spec_function = spec_function
        self.description = description

    def run(self, example_group):
        example_group.run_before_each(self)
        try:
            self.spec_function(self)
            return ExampleResult.as_success()
        except AssertionError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            return ExampleResult.as_failure(exc_value, exc_traceback)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            return ExampleResult.as_error(exc_value, exc_traceback)

class ExampleGroup(object):
    def __init__(self, parent, description):
        self.parent = parent
        self.examples = []
        self.description = description
        self.before_function = None

    def add_example(self, example):
        self.examples.append(example)

    def before(self, before_function):
        self.before_function = before_function

    def run(self, reporter):
        for example in self.examples:
            result = example.run(self)
            reporter.example_ran(example, result)

    def run_before_each(self, example):
        if self.before_function:
            self.before_function(example)

    def __enter__(self):
        self.parent.set_current_example_group(self)
        return self

    def __exit__(self, cls, value, traceback):
        self.parent.pop_current_example_group()

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
        [example_group.run(reporter) for example_group in self.example_groups]
        reporter.run_finished()

class ExampleResult(object):
    SUCCESS = 1
    FAILURE = 2
    ERROR = 3

    @classmethod
    def as_success(cls):
        return cls(cls.SUCCESS)

    @classmethod
    def as_failure(cls, *args):
        return cls(cls.FAILURE, *args)

    @classmethod
    def as_error(cls, *args):
        return cls(cls.ERROR, *args)

    def __init__(self, kind, exception = None, traceback = None):
        self.kind = kind
        self.exception = exception
        self.traceback = traceback
