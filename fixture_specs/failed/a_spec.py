from rgf.dsl import describe, it

with describe("This isn't going to end well"):
    @it('goes boom')
    def s(w):
        assert False
