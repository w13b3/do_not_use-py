#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# class_deco.py


class _AbstractDecorator:
    """ Base class to easily create convenient decorators """
    func_object = object()

    def __init__(self, function: object = func_object, **options):
        self.options = {}
        self.store_options(**options)  # store the given options

        self.decorated_function = self.func_object
        if function is not self.func_object:
            self.decorate(function)

    def decorate(self, function: callable) -> object:
        """ Remember the function to decorate """
        if not callable(function):
            raise TypeError(f'Cannot decorate non callable object {function!r}')
        self.decorated_function = function
        return self

    def store_options(self, **options) -> object:
        """ Store decorator's options """
        self.options = options
        return self

    def __call__(self, *args, **kwargs) -> (object or callable):
        """ Call the decorated function if available, else decorate first argument """
        if self.decorated_function is self.func_object:
            function_self = args[0]
            if args[1:] or kwargs:
                raise ValueError('Cannot decorate and setup simultaneously with __call__()')
            self.decorate(function_self)
            return self
        else:
            return self.execute(*args, **kwargs)

    def execute(self, *args, **kwargs):
        """ Execute the decorator """
        return self.decorated_function(*args, **kwargs)


class AddBefore(_AbstractDecorator):
    """ Decorator that greets return value of decorated function """

    def store_options(self, **kwargs):
        self.add = kwargs.get('add', '')
        return super(self.__class__, self).store_options()

    def execute(self, *args, **kwargs):
        """ execute decorated function and return modified result """
        name = super(self.__class__, self).execute(*args, **kwargs)
        return f'{self.add} {name}!'


if __name__ == '__main__':
    @AddBefore(add='-> Decorator added this <- ')
    def return_and_between_text(*args):
        return ' and '.join(args)
    print(return_and_between_text('this', 'that'))
