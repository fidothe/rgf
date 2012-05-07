class Example(object):
    def __init__(self, description, spec_function):
        self.spec_function = spec_function
        self.description = description

    def run(self, example_group):
        example_group.run_before_each(self)
        try:
            self.spec_function(self)
            return (1, None)
        except AssertionError as e:
            return (2, e)
        except Exception as e:
            return (3, e)

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

    def run(self):
        [example.run(self) for example in self.examples]

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

    def run(self):
        [example_group.run() for example_group in self.example_groups]

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

class ProgressFormatter(object):
    output_map = {1: '.', 2: 'F', 3: 'E'}

    def __init__(self, io):
        self.io = io

    def write_status(self, status):
        self.io.write(status)

    def write_line(self, line):
        self.io.write(line)
        self.io.write('\n')

    def success(self, example, example_finish_status):
        self.write_status('.')

    def failure(self, example, example_finish_status):
        self.write_status('F')

    def error(self, example, example_finish_status):
        self.write_status('E')

    def summarise_results(self, total, successes, failures, errors):
        self.write_line('Ran %s examples: %s success, %s failure, %s error' % (total, successes, failures, errors))
