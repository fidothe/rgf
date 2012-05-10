from rgf.dsl import describe, it

with describe('A'):
    @it('A spec')
    def f(w):
        pass
