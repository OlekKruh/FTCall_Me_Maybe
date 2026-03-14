import re
import math


def fn_add_numbers(a: int, b: int) -> int:
    """Adds two integers.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        The sum of a and b.
    """
    return a + b


def fn_greet(name: str) -> str:
    """Creates a greeting message.

    Args:
        name: The name of the person to greet.

    Returns:
        A greeting string.
    """
    return f"Hello {name}"


def fn_reverse_string(s: str) -> str:
    """Reverses the given string.

    Args:
        s: The input string.

    Returns:
        The reversed version of the input string.
    """
    reversed_s = s[::-1]
    return reversed_s


def fn_get_square_root(a: int) -> float:
    """Calculates the square root of a number.

    Args:
        a: The integer to find the square root of.

    Returns:
        The square root as a float.
    """
    return math.sqrt(a)


def fn_substitute_string_with_regex(source_string: str,
                                    regex: str,
                                    replacement: str) -> str:
    """Substitutes parts of a string using a regular expression.

    Args:
        source_string: The string to be modified.
        regex: The regular expression pattern to search for.
        replacement: The string to replace matches with.

    Returns:
        The modified string after substitution.
    """
    return re.sub(regex, replacement, source_string)
