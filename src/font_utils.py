from DrissionPage._pages.chromium_frame import ChromiumFrame
from DrissionPage._units.listener import DataPacket
from fontTools.ttLib import TTFont
from loguru import logger
from requests import (
    Response,
)  # Assuming you're using the requests library for HTTP requests


def get_woff_from_frame(iframe: ChromiumFrame):
    """
    Not implemented
    """
    return ""


def save_woff_file(dataPacket: DataPacket, file_path: str) -> None:
    """
    Save the WOFF font data from the response to a file.

    Args:
        response (Response): The response object containing the font data.
        file_path (str): The path where the font file will be saved.
    """
    response = dataPacket.response
    status = response.status

    # Not Modified
    if status == 304:
        woff = get_woff_from_frame()
    # OK
    elif status == 200:
        woff = response.body
    with open(file_path, "wb") as f:
        f.write(woff)


def process_font_file(font_path: str) -> dict:
    """
    Process a font file, save its XML representation, and return a mapping of character codes to glyph names.

    Args:
        font_path (str): Path to the font file.

    Returns:
        dict: A dictionary mapping character codes (in hex) to glyph names.
    """
    # Load the font file
    font = TTFont(font_path)

    # Save the font data as an XML file
    font.saveXML(font_path + ".xml")

    cmap = font.getBestCmap()

    # Convert the mapping keys to hex and return the new mapping
    font_map = {}
    for key, value in cmap.items():
        if value.startswith("uni"):
            # Extract the hexadecimal part and convert it to a Unicode character
            unicode_char = chr(int(value[3:], 16))
            font_map[hex(key)] = unicode_char
        else:
            # Handle other cases if necessary
            font_map[hex(key)] = value

    return font_map


# Function to map characters using font_map
def map_text(text, font_map):
    """Map the text using the font_map to correct the scrambled characters."""
    return "".join(font_map.get(hex(ord(char)), char) for char in text)
