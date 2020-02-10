# Default patch
### What does this do
With this you can patch a callable (like a function) and give it default values.

#### But why?

For a personal project i needed to add an authorization token to parameters and headers to the REST-API calls.

It was not very DRY to add the authorization token to each parameter.

[There must be a better way](https://twitter.com/raymondh), ~~this _may_ be it~~.

### How does it work


``` 
    >>> func1 = lambda x: print(x)
    >>> func1 = default_patch(function, x='hello')
    >>> func1()
    'hello'
```

### Important to know
This should not be used. Don't trust this.

Read the tests, Run the tests.

Yes i know there is [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) and [inspect.BoundArguments.apply_defaults](https://docs.python.org/3/library/inspect.html#inspect.BoundArguments.apply_defaults)

#### What i learned
Even if you cant give a function a [decorator](https://wiki.python.org/moin/PythonDecorators), you can redirect the call through a wrapper