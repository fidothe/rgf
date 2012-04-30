class Example(object):
    def __init__(self, description, spec_function):
        self.spec_function = spec_function
        self.description = description

    def run(self):
        self.spec_function(self)
