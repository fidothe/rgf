from rgf.dsl import *
import os, re

try:
    from sets import Set as set
except ImportError:
    # `sets` module deprecated since 2.6
    pass

from rgf.core.runner import Collector
from rgf.core.examples import ExampleSuite

with subject('Collector'):
    @before
    def b(w):
        w.spec_file_path = os.path.abspath('fixture_specs/success/b/b_spec.py')
        w.spec_root_path = os.path.abspath('fixture_specs/success')

    @it('can find spec files in a directory hierarchy')
    def s(w):
        actual = set(Collector(w.spec_root_path).found_spec_files())
        expected = ['a_spec.py', 'b/b_spec.py', 'c/d/d_spec.py']
        expected = set(['%s/%s' % (w.spec_root_path, x) for x in expected])
        assert actual == expected

    @it('can import a spec file and collect its ExampleGroups')
    def s(w):
        collector = Collector('/path/to/spec')
        root_module = 'rgf_anon_collector'
        mod = collector.import_spec_file(w.spec_file_path, root_module)
        assert re.compile(r'^%s\.spec_[0-9a-f]+$' % root_module).match(mod.__name__)
        assert os.path.splitext(mod.__file__)[0] == os.path.splitext(w.spec_file_path)[0]

    @it('can import multiple spec files')
    def s(w):
        collector = Collector(w.spec_root_path)
        imported_files = []
        def mock_import_file_func(path, root):
            imported_files.append(path)
        collector.import_spec_file = mock_import_file_func
        collector.import_spec_files()
        expected = ['a_spec.py', 'b/b_spec.py', 'c/d/d_spec.py']
        expected = set(['%s/%s' % (w.spec_root_path, x) for x in expected])
        assert set(imported_files) == expected, '%r != %r' % (imported_files, expected)

    @it('collects files to an ExampleSuite when it imports them')
    def s(w):
        collector = Collector(w.spec_root_path)
        example_suite = ExampleSuite()
        collector.collect_to(example_suite)
        assert len(example_suite.example_groups) == 4
