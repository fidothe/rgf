class Example(object):
    def __init__(self, description, spec_function, example_group):
        self.spec_function = spec_function
        self.description = description
        self.example_group = example_group

    def run(self):
        self.example_group.run_before_each(self)
        try:
            self.spec_function(self)
            return (1, None)
        except AssertionError as e:
            return (2, e)
        except Exception as e:
            return (3, e)

class ExampleGroup(object):
    def __init__(self):
        self.examples = []
        self.before_function = None

    def add_example(self, example):
        self.examples.append(example)

    def add_before(self, before_function):
        self.before_function = before_function

    def run(self):
        [example.run() for example in self.examples]

    def run_before_each(self, example):
        if self.before_function:
            self.before_function(example)
