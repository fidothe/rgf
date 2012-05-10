import traceback, os, os.path, re, imp
from rgf.core.examples import ExampleResult

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
        self.success_count = 0
        self.failures = []
        self.errors = []

    def example_ran(self, example, result):
        if result.kind == ExampleResult.SUCCESS:
            self.success_count += 1
            self.formatter.success(example, result)
        elif result.kind == ExampleResult.FAILURE:
            self.failures.append((example, result))
            self.formatter.failure(example, result)
        elif result.kind == ExampleResult.ERROR:
            self.errors.append((example, result))
            self.formatter.error(example, result)
        else:
            raise ValueError('Unrecognised Example result kind')

    def run_finished(self):
        self.formatter.summarise_results(self.total_number_of_examples(),
                self.number_of_successes(), 
                self.number_of_failures(),
                self.number_of_errors())
        self.formatter.summarise_failures(self.failures)
        self.formatter.summarise_errors(self.errors)

    def total_number_of_examples(self):
        return self.success_count + self.number_of_failures() + self.number_of_errors()

    def number_of_successes(self):
        return self.success_count

    def number_of_failures(self):
        return len(self.failures)

    def number_of_errors(self):
        return len(self.errors)

class Collector(object):
    def __init__(self, start_path):
        self.start_path = start_path

    def found_spec_files(self):
        spec_files = []
        spec_matcher = re.compile(r'[\w]+_spec\.py$')
        for path, dirs, files in os.walk(self.start_path):
            for name in files:
                if spec_matcher.match(name):
                    spec_files.append(os.path.join(path, name))
        return spec_files

    def import_spec_file(self, path, root):
        module_hierarchy_components = os.path.relpath(path, root).split(os.path.sep)
        last_mod, ext = os.path.splitext(module_hierarchy_components[-1])
        module_hierarchy_components[-1:] = [last_mod]
        module_hierarchy_components[:0] = ['spec']
        name = '.'.join(module_hierarchy_components)
        with file(path) as f:
            mod = imp.load_module(name, f, path, ('.py', 'U', imp.PY_SOURCE))
        return mod
