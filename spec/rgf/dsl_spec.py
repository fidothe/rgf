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
        example_suite = ExampleSuite()
        ExampleSuite.set_suite(example_suite)
        with describe('Example Group with examples added by it()') as eg:
            decorator = it('Example description created by it()')
            example = decorator(first_test_function)
            assert eg.examples == [example]

    @it("provides before() decorator creator. The decorator adds a function to the current ExampleGroup's before runner")
    def spec(world):
        with describe('Example Group with before function') as eg:
            before(before_func)
            assert eg.before_function is before_func
