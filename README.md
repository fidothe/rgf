red / green / refactor
======================

A currently experimental attempt at an RSpec-esque BDD testing framework for Python.

Basically we're aiming for syntax along these lines:

```python
from rgf import describe, it

with describe("That Thing"):
    @it("test desc")
    def spec(context):
        # test code here
        assert stuff() 
```

`x_spec.py` files go in a directory structure under, by convention, `spec/` in the
root of your project and are run using:

```bash
rgf spec
```


The specifics of the syntax are currently wrong, being borrowed directly from RSpec.
Suggestions warmly received.

(Current front-runners are `subject` and `context` in place of `describe`, keeping `it` for the spec decorator.)

Because the spec functions are just functions, not methods, and are hoovered up by the `@it` decorator they're
effectively anonymous and can all have the same name for ease of thinking:

```python
with subject('This Class'):
    @it('can calculate X')
    def s(world):
        pass

    @it('can account for Y')
    def s(world):
        pass
```


The aim is for something pythonic, with nested context and good spec names being the primary focus: minimum magic, minimum fuss.
