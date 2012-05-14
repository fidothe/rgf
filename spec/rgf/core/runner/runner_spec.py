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
        runner.run(suite, os.path.abspath(os.path.join(__file__, '../../../../../fixture_specs/success')))
        assert len(reporter.examples_ran) > 0

with describe('rgf script'):
    def run_spec_script(spec_path):
        p = subprocess.Popen('./cold_runner %s' % spec_path, shell = True, stdout = subprocess.PIPE)
        output, p_null = p.communicate()
        return_val = p.wait()
        return (return_val, output)

    @it('can create and run a runner')
    def f(w):
        return_val, output = run_spec_script('fixture_specs/success')
        assert re.compile(r'4 examples'.encode('utf-8')).search(output) is not None

    @it('returns exit status 0 on a successful run')
    def f(w):
        return_val, output = run_spec_script('fixture_specs/success')
        assert return_val == 0

    @it('returns exit status 1 if there are failures')
    def f(w):
        return_val, output = run_spec_script('fixture_specs/failed')
        assert return_val == 1

