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

The aim is for something pythonic, with nested context and good spec names being the primary focus: minimum magic, minimum fuss.
