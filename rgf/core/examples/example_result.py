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

    def is_success(self):
        return self.kind == self.SUCCESS

    def is_failure(self):
        return self.kind == self.FAILURE

    def is_error(self):
        return self.kind == self.ERROR

    def is_not_success(self):
        return self.kind != self.SUCCESS
