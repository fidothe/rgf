from rgf.dsl import describe, it

with describe('D1'):
    @it('D spec')
    def f(w):
        pass

with describe('D2'):
    @it('D spec')
    def f(w):
        pass

