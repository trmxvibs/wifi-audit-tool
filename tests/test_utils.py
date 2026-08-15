# tests/test_utils.py
from utils.helpers import colorful_print


def test_colorful_print_wraps_known_color(capsys):
    """Known color should wrap text in the matching ANSI code and reset."""
    from colorama import Fore, Style
    colorful_print("hello", "green")
    captured = capsys.readouterr()
    # helpers.py maps "green" to the bright variant (matches the
    # original \033[92m code), not colorama's plain Fore.GREEN.
    assert Fore.LIGHTGREEN_EX in captured.out
    assert "hello" in captured.out
    assert Style.RESET_ALL in captured.out


def test_colorful_print_falls_back_on_unknown_color(capsys):
    """Unknown color name should not crash; falls back to reset code."""
    colorful_print("hello", "not-a-real-color")
    captured = capsys.readouterr()
    assert "hello" in captured.out
