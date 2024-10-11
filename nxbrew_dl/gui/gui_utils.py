import logging
import sys

import colorlog
from PySide6.QtCore import Slot
from PySide6.QtGui import QDesktopServices

from ..gui.custom_widgets import TableRowWidget


@Slot()
def open_url(url):
    """Opens a URL"""

    QDesktopServices.openUrl(url)


def add_row_to_table(
    table,
    row_dict,
    row_name_key="long_name",
):
    """Add row to table, using a dictionary of important info

    Args:
        table (QTableWidget): Table to add row to
        row_dict (dict): Dictionary of data for the row
        row_name_key (str): Key used to identify the name for the row.
            Defaults to "long_name"
    """

    row_position = table.rowCount()

    table.insertRow(row_position)

    row = TableRowWidget(
        row_dict,
        row_name_key=row_name_key,
    )
    row.setup_row(
        table=table,
        row_position=row_position,
    )

    return row


def get_gui_logger(log_level="info"):
    """Get the logger for the GUI

    Args:
        log_level (str, optional): Logging level. Defaults to "info".
    """
    logger = logging.getLogger()

    # Set the log level based on the provided parameter
    log_level = log_level.upper()
    if log_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif log_level == "INFO":
        logger.setLevel(logging.INFO)
    elif log_level == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
    else:
        logger.critical(f"Invalid log level '{log_level}', defaulting to 'INFO'")
        logger.setLevel(logging.INFO)
    log_handler = colorlog.StreamHandler(sys.stdout)
    log_handler.setFormatter(
        colorlog.ColoredFormatter("%(log_color)s%(levelname)s: %(message)s")
    )
    logger.addHandler(log_handler)

    return logger
