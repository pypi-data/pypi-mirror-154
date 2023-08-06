# For opening browser tabs.
from webbrowser import open_new_tab

# For silencing browser output.
from os import dup, close, open, devnull, O_RDWR, dup2


def web_open_tab(url: str):
    """Open given url on new tab.

    Args:
        url (str): Url to open.
    """

    # Close standard error.
    stderr = dup(1)
    close(1)

    # Close standard output.
    stdout = dup(2)
    close(2)

    # Open output to null.
    open(devnull, O_RDWR)

    # Try to open new tab.
    try:
        open_new_tab(url)
    finally:
        # Restore standard error.
        dup2(stderr, 1)
        # Restore standard output.
        dup2(stdout, 2)
