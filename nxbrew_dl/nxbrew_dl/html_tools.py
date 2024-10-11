import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .regex_tools import get_game_name, check_has_filetype


def get_game_index(
    nxbrew_url,
    cache=True,
):
    """Get the NXBrew index as a soup

    Args:
        nxbrew_url (string): NXBrew URL
        cache (bool): If True, will save the game index as a cache. Defaults to True FIXME
    """

    game_index_name = "game_index.html"
    url = urljoin(nxbrew_url, "Index/game-index/games/")

    if not cache:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
    else:
        if not os.path.exists(game_index_name):
            r = requests.get(url)
            with open(game_index_name, mode="wb") as f:
                f.write(r.content)
            r = r.content
        else:
            with open(game_index_name, mode="rb") as f:
                r = f.read()
        soup = BeautifulSoup(r, "html.parser")

    return soup


def get_game_dict(
    general_config,
    regex_config,
    nxbrew_url,
):
    """Download the game index, and parse relevant info out of it

    Args:
        general_config (dict): General configuration
        regex_config (dict): Regex configuration
        nxbrew_url (string): NXBrew URL
    """

    game_dict = {}

    # Load in the HTML
    game_html = get_game_index(nxbrew_url)
    index = game_html.find("div", {"id": "easyindex-index"})

    nsp_xci_variations = regex_config["nsp_variations"] + regex_config["xci_variations"]
    for item in index.find_all("li"):

        # Get the long name, the short name, and the URL
        long_name = item.text

        # If there are any forbidden titles, skip them here
        if long_name in general_config["forbidden_titles"]:
            continue

        short_name = get_game_name(long_name, nsp_xci_variations=nsp_xci_variations)
        url = item.find("a").get("href")

        if url in game_dict:
            raise ValueError(f"Duplicate URLs found: {url}")

        # Pull out whether NSP/XCI, and whether it has updates/DLCs
        remaining_name = long_name.replace(short_name, "")
        has_nsp = check_has_filetype(remaining_name, regex_config["nsp_variations"])
        has_xci = check_has_filetype(remaining_name, regex_config["xci_variations"])
        has_update = check_has_filetype(
            remaining_name, regex_config["update_variations"]
        )
        has_dlc = check_has_filetype(remaining_name, regex_config["dlc_variations"])

        game_dict[url] = {
            "long_name": long_name,
            "short_name": short_name,
            "url": url,
            "has_nsp": has_nsp,
            "has_xci": has_xci,
            "has_update": has_update,
            "has_dlc": has_dlc,
        }

    return game_dict
