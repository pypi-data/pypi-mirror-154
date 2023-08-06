"""Internal module for functions that will be imported in __init__.py for shorter syntax."""

from __future__ import annotations
import textwrap

from typing import Union

from typing_extensions import Literal

from .colors.colors_module import colorize

USED_AROUND = True


def format_str(
    message: str,
    caption: str = "User message",
    around: Union[bool, str] = "config",
    use_object_conversion: bool = True,
    indent: int = 4,
    uncolored_message: None | str = None,
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "WARNING",
) -> str:
    """Return enhanced colored message. Used for raising exceptions, assertions.

    Args:
        message (str): Any string content of warning.
        caption (str, optional): Heading of warning. Defaults to 'User message'.
        around (Union[bool, str], optional): If print to file - whether print ====== lines around.
            If 'auto', then if output is to file, then around = False, if output == "console", around = True.
            If 'config', use global config (defaults 'auto'). Defaults to 'config'.
        use_object_conversion (bool, optional): Turn into object (If call in raise - only way to
            print colors). If you need string to variable, call str(). Defaults to True.
        indent (int, optional): By how many spaces are logs indented (for better visibility). If 0,
            than no indentation. Defaults to 4.
        uncolored_message (None | str, optional): Appendix added to end that will not be colorized (or
            already is colorized). Used for example for tracebacks. Defaults to None.
        level (str, optional): Defaults to "DEBUG".

    Returns:
        str: Enhanced message as a string, that is wrapped by and can be colorized.

    Example:
        >>> format_str("Formated", caption="Caption")
        <BLANKLINE>
        <BLANKLINE>
            ========= Caption =========
        <BLANKLINE>
            Formated
        <BLANKLINE>
            ===========================
        <BLANKLINE>
        <BLANKLINE>
    """

    # If only caption do not print None or False
    if not message:
        message = ""

    if around == "config":
        around = USED_AROUND

    updated_str = colorize(message, level=level)

    if uncolored_message:
        if not around:
            uncolored_message = uncolored_message + "\n"
        updated_str = updated_str + uncolored_message

    if around:
        updated_str = wrap(updated_str, caption=caption, level=level)

    else:
        if caption:
            updated_str = f"{colorize(caption, level=level)}: {updated_str}"

    if indent:
        updated_str = textwrap.indent(text=updated_str, prefix=" " * indent)

    if use_object_conversion:
        updated_str = use_object_conversion_str(updated_str)

    return updated_str


class StringObject(str):
    """Custom wrapper so it can be edited."""

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def __repr__(self) -> str:
        return f"{self.message}"


def wrap(
    message: str,
    caption: None | str = None,
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "WARNING",
):
    """Wrap string with significant lines (===========) with optional caption.

    Args:
        message (str): Message to be wrapped.
        caption (None | str, optional): In the middle of first wrapping line. Defaults to None.
        level (Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], optional): Define what color will
            be used. Defaults to "WARNING".

    Returns:
        str: Formatted message

    Example:
        >>> print(wrap("Hello", caption="Caption"))
        <BLANKLINE>
        <BLANKLINE>
        ========= Caption =========
        <BLANKLINE>
        Hello
        <BLANKLINE>
        ===========================
        <BLANKLINE>
        <BLANKLINE>
    """
    top_line = f"========= {caption} =========" if caption else "============================="
    bottom_line = colorize(f"{'=' * len(top_line)}", level=level) + "\n\n"
    top_line = colorize(top_line, level=level)
    return f"\n\n{top_line} \n\n{message} \n\n{bottom_line}"


def use_object_conversion_str(message: str) -> StringObject:
    """Make a class from a string to be able to apply escape characters and colors if raise.

    Args:
        message (str): Any string you use.

    Returns:
        Object: Object, that can return string if printed or used in warning or raise.
    """

    return StringObject(message)
