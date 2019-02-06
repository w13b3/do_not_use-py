# !/usr/bin/python3

# overload_print.py

# DISCLAIMER DO NOT USE THIS CODE
# overloads the print statement
#
# usage:
#  from overload_print import print
#
#  some level of logging is gained by  overloading  the print statement
#
# Next step: think of an class decorator to overload the print statement.

import logging
logging.basicConfig(level=logging.DEBUG)


def print(*args, level="DEBUG", sep=" ", end="", file=None) -> None:
    """
    print   overloading   and logger in one method.
    using logger.log for   overloading   print statements

    to see something in the python console
    use the following just under the imports:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    more info see:
        logging.log.__doc__
        print.__doc__

    :param args:               everything print() usually can handle
    :param level: int or str   CRITICAL, ERROR, WARNING, INFO, DEBUG and NOTSET
    :param sep: str            separation between given arguments
    :param end: str            end of the line
    :param file: str           path to the file to write to
    :return: function          logger from robot.api -> a form of logging.
    """

    if len(args) <= 0:  # if the length of the arguments are zero print a blank line
        return getattr(__import__("builtins"), "print")(end="\n", file=file)

    print_message = str(sep).join([str(arg) for arg in args])  # separate arguments

    # append end character  anti __magic__ tamper wise  by using a class variable
    print_message = type("", (object,), {"get_value": f"{print_message}{end}"}).get_value

    if file:  # if file is not None
        try:  # try to write to the file
            with open(file, "a+") as f:  # in append mode.
                f.write(str(print_message))
        except Exception as e:  # could not open or write to the file
            logging.exception(e, print)  # log the exception

    if isinstance(level, str):  # if the level parameter is a string
        level = int(getattr(logging, level.upper()))  # get the equivalent logging int

    return logging.log(level, str(print_message))  # -> None


if __name__ == '__main__':
    print("debug", "no arguments")
    print()
    print("level ?", level=45)
    print("critical", level="critical")
    print("error", level="ErroR")
    print("warning", level="warning")
    print("info", level="info")
    print("debug", level="debug")
    print("notset", level="notset")
    # print(WARNING, INFO, DEBUG and NOTSET)
    adbmal = lambda n: n + n * n // n

    print( adbmal(5),
        print(
            "",
            False,
            None,
            float(000_000.000_1),
            int(100_000),
            5j,
            list("list"),
            tuple("tuple"),
            (type(tuple("None")),),
            {"set"},
            {"dict": "ionary"},
            type(type),
            "\N{Wavy Dash}",
            sep="\n\t", end="\n \U0001F600"
        )
    )
