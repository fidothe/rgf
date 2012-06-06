from rgf.dsl import *

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from rgf.core.runner import ProgressFormatter
from rgf.core.examples import Example

class MockExampleGroup(object):
    def run_before_each(self, example):
        pass

class MockExample(object):
    pass

def mock_world_factory():
    pass

with subject('ProgressFormatter'):
    @it('can log a success to an IO-like object')
    def s(w):
        io = StringIO()
        pf = ProgressFormatter(io)
        pf.success(MockExample(), (1, None))
        assert io.getvalue() == '.'

    @it('can log a failure to an IO-like object')
    def s(w):
        io = StringIO()
        pf = ProgressFormatter(io)
        pf.failure(MockExample(), (2, None))
        assert io.getvalue() == 'F'

    @it('can log an error to an IO-like object')
    def s(w):
        io = StringIO()
        pf = ProgressFormatter(io)
        pf.error(MockExample(), (3, None))
        assert io.getvalue() == 'E'

    @it('can summarise the results of running all examples')
    def s(w):
        io = StringIO()
        pf = ProgressFormatter(io)
        pf.summarise_results(total = 3, successes = 1, failures = 1, errors = 1)
        assert io.getvalue() == 'Ran 3 examples: 1 success, 1 failure, 1 error\n'

    with context('summarising Failures and Errors'):
        @before
        def b(w):
            def failed_test_function(self):
                assert False
            w.failing_example = Example("reports failure", failed_test_function)

            def error_test_function(self):
                raise KeyError('grrr')
            w.error_example = Example("reports error", error_test_function)

        @it('can summarise failures')
        def s(w):
            result = w.failing_example.run(MockExampleGroup(), mock_world_factory)
            io = StringIO()
            pf = ProgressFormatter(io)
            pf.summarise_failures([(w.failing_example, result)])
            assert io.getvalue() != '' # there must be a better test than this which isn't terrifyingly brittle

        @it('can summarise errors')
        def s(w):
            result = w.failing_example.run(MockExampleGroup(), mock_world_factory)
            io = StringIO()
            pf = ProgressFormatter(io)
            pf.summarise_errors([(w.error_example, result)])
            assert io.getvalue() != '' # there must be a better test than this which isn't terrifyingly brittle
