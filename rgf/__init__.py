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
        except Exception as e:
            return (3, e)
