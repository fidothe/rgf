from rgf.dsl import describe, it, before

from rgf.core.examples import ExampleGroup, ExampleSuite

def first_test_function(world):
    world.has_been_run = True

def before_func(world):
    world.before_was_run = True

with describe('DSL'):
    @it('provides describe helper context to create and set current ExampleGroup')
    def spec(world):
        eg = describe('This Example Group')
        assert type(eg) is ExampleGroup

    @it('provides it() decorator creator. The decorator creates Examples on the current ExampleGroup')
    def spec(world):
        with describe('Example Group with examples added by it()') as eg:
            decorator = it('Example description created by it()')
            example = decorator(first_test_function)
            assert example.description == 'Example description created by it()'
            assert eg.examples == [example]

    @it("provides before() decorator creator. The decorator adds a function to the current ExampleGroup's before runner")
    def spec(world):
        with describe('Example Group with before function') as eg:
            before(before_func)
            assert eg.before_function is before_func

    @it('describe allows the parent of the ExampleGroup to be specified')
    def spec(world):
        example_suite = ExampleSuite()
        with describe('ExampleGroup with hard-wired parent', parent = example_suite) as eg:
            assert eg.parent is example_suite

    @it('allows the ExampleGroup to be explicitly passed to the the it decorator')
    def spec(world):
        example_suite = ExampleSuite()
        example_group = ExampleGroup(example_suite, 'eg for explicit passing to it() decorator')
        decorator = it('has explicit ExampleGroup', example_group = example_group)
        example = decorator(first_test_function)
        assert example_group.examples == [example]

# from future, import...
# --> At this point we can start to break up the tests into multiple files :-)
# Actually work out the language issues
# rgf script returns non-zero exit status if any specs failed
# --> At this point we can be used by a CI bot :-)
# ExampleGroups can be properly nested
# before-functions are properly dealt with in nested contexts
# ProgressFormatter can output coloured dots if asked
# DocumentationFormatter can output something like Rspec's specdoc format
# formatter can be chosen by passing an arg to rgf
# config can be extracted to a .rgf project file
# --> At this point we're probably useful
