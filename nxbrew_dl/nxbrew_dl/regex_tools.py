import re


def get_game_name(
    f,
    nsp_xci_variations,
):
    """Get game name, which is normally up to "Switch NSP", but there are some edge cases

    Args:
        f (str): Name
        nsp_xci_variations (list): List of potential NSP/XCI name variations
    """

    # This is a little fiddly, the default is something like [Name] Switch NSP/XCI or whatever, but there's also
    # various other possibilities. Search for "Switch" (with optional NSP/XCI variations), "Cloud Version", "eShop",
    # "Switch +, "+ Update", and "+ DLC"
    regex_str = (
        "^.*?"
        "(?="
        f"(?:\\s?Swi(?:tc|ct)h)?\\s(?:\\(?{'|'.join(nsp_xci_variations)})\\)?"
        "|"
        "(?:\\s[-|–]\\sCloud Version)"
        "|"
        "(?:\(eShop\))"
        "|"
        "(?:\\s?Switch\\s\+)"
        "|"
        "(?:\\s?\+\\sUpdate)"
        "|"
        "(?:\\s?\+\\sDLC)"
        ")"
    )

    reg = re.findall(regex_str, f)

    # If we find something, then pull that out
    if len(reg) > 0:
        f = reg[0]

    return f


def check_has_filetype(
    f,
    search_str,
):
    """Check whether the game has an associated filetype

    Args:
        f (str): Name of the file
        search_str (list): List of potential values to check for
    """

    regex_str = "|".join(search_str)

    reg = re.findall(regex_str, f)

    if len(reg) > 0:
        return True
    else:
        return False
