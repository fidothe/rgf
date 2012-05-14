from rgf.dsl import describe, it, before

from rgf.core.examples import ExampleResult

class MockException(object):
    pass

class MockTraceback(object):
    pass

with describe('ExampleResult'):
    @it('reports that it was a success')
    def s(w):
        result = ExampleResult.as_success()
        assert result.is_success()

with describe('ExampleResult failed'):
    @before
    def b(w):
        w.mock_exception = MockException()
        w.mock_traceback = MockTraceback()
        w.result = ExampleResult.as_failure(w.mock_exception, w.mock_traceback)

    @it('reports that it was a failure')
    def s(w):
        assert w.result.is_failure()

    @it('reports that it was not a success')
    def s(w):
        assert w.result.is_not_success()

    @it('returns the exception')
    def s(w):
        assert w.result.exception is w.mock_exception

    @it('returns the traceback')
    def s(w):
        assert w.result.traceback is w.mock_traceback

with describe('ExampleResult error'):
    @before
    def b(w):
        w.mock_exception = MockException()
        w.mock_traceback = MockTraceback()
        w.result = ExampleResult.as_error(w.mock_exception, w.mock_traceback)

    @it('reports that it was an error')
    def s(w):
        assert w.result.is_error()

    @it('reports that it was not a success')
    def s(w):
        assert w.result.is_not_success()

    @it('returns the exception')
    def s(w):
        assert w.result.exception is w.mock_exception

    @it('returns the traceback')
    def s(w):
        assert w.result.traceback is w.mock_traceback
