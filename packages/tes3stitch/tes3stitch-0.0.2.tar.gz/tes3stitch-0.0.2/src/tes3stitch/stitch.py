import pathlib
import re
import numpy as np
from PIL import Image


def find_xy(filename):
    """Find x and y coordinate in filename. Regex search for parenthesis, two groups for
    digits separated by comma, ending parenthesis. Required info will be stored in
    groups 1 and 2."""
    x, y = re.search(r"\((-?\d+),(-?\d+)\)", filename).group(1, 2)
    return int(x), int(y)


def coordinate_dict(path, pattern="*.bmp"):
    """Returns dict of .bmp (or other pattern) file paths in directory, keyed by
    a tuple of coordinates."""
    file_list = pathlib.Path(path).glob(pattern)
    return {find_xy(file_path.name): file_path for file_path in file_list}


def combine_images(filedict, tilewidth=40, color="#00000000"):
    """Stitches together images based on a dictionary of files per coordinate."""
    # Use coordinates and tile widths to calculate where to paste.
    x_min = min((x for (x, y) in filedict))
    x_max = max((x for (x, y) in filedict))
    y_min = min((y for (x, y) in filedict))
    y_max = max((y for (x, y) in filedict))
    x_size = (x_max - x_min + 1) * tilewidth
    y_size = (y_max - y_min + 1) * tilewidth

    # Paste tiles on new properly sized canvas.
    stitched = Image.new("RGBA", (x_size, y_size), color)

    for (x, y), filename in filedict.items():
        x_offset = (x - x_min) * tilewidth
        y_offset = (y_max - y) * tilewidth
        with Image.open(pathlib.Path(filename)) as tile:
            sized_tile = tile.resize((tilewidth, tilewidth))
            stitched.paste(sized_tile, (x_offset, y_offset))

    return stitched
