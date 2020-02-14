# Handy decorators
### What does this do?
A decorator is a function that takes another function and extends the behavior of the decorated function without changing said function.


Example:
```
>>> from deco import clapping_hands
>>> @clappinghands  # <- decorator
>>> def text_function(text: str) -> str:
...    return str(text)
...
>>> some_text = 'Whitespace becomes clapping hands emoji\'s'
>>> result = text_function(some_text)
>>> print(result)
Whitespace👏becomes👏clapping👏hands👏emoji's
>>>
```
