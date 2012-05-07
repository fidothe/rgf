import sys, traceback

class Example(object):
    def __init__(self, description, spec_function):
        self.spec_function = spec_function
        self.description = description

    def run(self, example_group):
        example_group.run_before_each(self)
        try:
            self.spec_function(self)
            return ExampleResult(1, None, None)
        except AssertionError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            return ExampleResult(2, exc_value, exc_traceback)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            return ExampleResult(3, exc_value, exc_traceback)

class ExampleGroup(object):
    def __init__(self, parent, description):
        self.parent = parent
        self.examples = []
        self.description = description
        self.before_function = None

    def add_example(self, example):
        self.examples.append(example)

    def add_before(self, before_function):
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

def before(example_group = None):
    if example_group is None:
        example_group = _get_current_example_group()
    def before_wrapper(before_function):
        example_group.add_before(before_function)
    return before_wrapper

class ExampleResult(object):
    SUCCESS = 1
    FAILURE = 2
    ERROR = 3

    def __init__(self, kind, exception = None, traceback = None):
        self.kind = kind
        self.exception = exception
        self.traceback = traceback

class ProgressFormatter(object):
    def __init__(self, io):
        self.io = io

    def write_status(self, status):
        self.io.write(status)

    def write_line(self, line):
        self.io.write(line)
        self.io.write('\n')

    def success(self, example, example_result):
        self.write_status('.')

    def failure(self, example, example_result):
        self.write_status('F')

    def error(self, example, example_result):
        self.write_status('E')

    def summarise_results(self, total, successes, failures, errors):
        self.write_line('Ran %s examples: %s success, %s failure, %s error' % (total, successes, failures, errors))

    def summarise_failures_or_errors(self, failures_or_errors):
        for (example, example_result) in failures_or_errors:
            self.write_line(example.description)
            traceback.print_exception(type(example_result.exception), 
                    example_result.exception, example_result.traceback, file = self.io)

    def summarise_failures(self, failures):
        self.summarise_failures_or_errors(failures)

    def summarise_errors(self, errors):
        self.summarise_failures_or_errors(errors)

class Reporter(object):
    def __init__(self, formatter):
        self.formatter = formatter
    def example_ran(self, example, result):
        if result.kind == ExampleResult.SUCCESS:
            self.formatter.success(example, result)
        elif result.kind == ExampleResult.FAILURE:
            self.formatter.failure(example, result)
        elif result.kind == ExampleResult.ERROR:
            self.formatter.error(example, result)
        else:
            raise ValueError('Unrecognised Example result kind')
