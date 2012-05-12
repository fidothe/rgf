from rgf.dsl import describe, it

with describe('B'):
    @it('B spec')
    def f(w):
        pass

