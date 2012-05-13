from rgf.dsl import describe, it, before
import os.path, subprocess, re

from rgf.core.examples import ExampleSuite
from rgf.core.runner import Runner

class MockReporter(object):
    def __init__(self):
        self.examples_ran= []

    def example_ran(self, *args):
        self.examples_ran.append(args)

    def run_finished(self):
        self.run_finished_was_called = True

with describe('Runner'):
    @it('can collect and run spec files through a Reporter')
    def f(w):
        reporter = MockReporter()
        runner = Runner(reporter)
        suite = ExampleSuite()
        runner.run(suite, os.path.abspath(os.path.join(__file__, '../../../../../fixture_spec')))
        assert len(reporter.examples_ran) > 0

with describe('rgf script'):
    @it('can create and run a runner')
    def f(w):
        p = subprocess.Popen('python rgf/cold_runner.py fixture_spec', shell = True, stdout = subprocess.PIPE)
        output, p_null = p.communicate()
        return_val = p.wait()
        assert return_val == 0
        assert re.compile(r'4 examples').search(output) is not None
