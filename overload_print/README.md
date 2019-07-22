# Overload print
### What does this do
Overload the print function of Python into a logger

#### But why?

Prototyping is easy in python, however it can become complex quick.

Logging is always preferred in complex situations but no one takes the time to do this properly in a prototype script.

Imagine the developer working on the prototype script breaks something.

Suddenly the complex script doesn't work anymore but the code is full of print statements 

Now there is a need of a logger to debug the script.

One might do a _find_ 'print(' _and replace_ 'logger.debug('.

But there is a catch, the print statement can handle multiple arguments, the logger can not.

Here comes this script into play. 

overload_print combines the flexibility of print() and the power of logging.log()

### How does it work

Import this script with:

``` from overload_print import print ```

The overloaded print statement takes all the arguments given and converts them into a string and logs it.

Print keyword arguments are respected and are visible in the log.

Logging levels are respected too by the keyword: level. But the default is 'DEBUG'

### Important to know
This is no substitute to the logging module.

This should not be used.

#### What i learned
```type()``` is a powerful function, it can create a class in a single line.

##### Fun
![print statement meme](https://i.redd.it/1o3y48clugl11.jpg)
