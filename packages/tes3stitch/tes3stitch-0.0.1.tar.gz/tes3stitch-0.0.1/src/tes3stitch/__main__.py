"""Image stitcher for the TES III: Morrowind CreateMaps command.

Stitches together the 256x256 pixel .bmp images that Morrowind creates when running the
`CreateMaps <plugin>.esm` console command.

Requires Pillow library for Python 3.

Created by Sultan of Rum for Tamriel Rebuilt. Inspired by the prior work of Seneca37,
Atrayonis and mort.
"""


# TODO: add a GUI, leave an option for CLI
# TODO: test whether a full-resolution all-Tamriel map is feasible in terms of memory size
import argparse

from tes3stitch import stitch


def main():
    # Set up command line arguments.
    cmd_parser = argparse.ArgumentParser(
        description="Image stitcher for the TES III: Morrowind CreateMaps command. \
Stitches together the 256x256 pixel .bmp images that Morrowind creates when running \
the `CreateMaps <plugin>.esm` console command. Requires Pillow library for Python 3.",
        epilog="Created by Sultan of Rum for Tamriel Rebuilt. Inspired by the prior \
work of Seneca37, Atrayonis and mort.",
    )
    cmd_parser.add_argument(
        "-p",
        "--path",
        default=".",
        metavar="PATH",
        help="Path to the folder containing input .bmp files. Defaults to current \
working directory.",
    )
    cmd_parser.add_argument(
        "-o",
        "--output",
        default="CellExport.png",
        metavar="FILENAME",
        help="Filename of output image. Defaults to 'CellExport.png'.",
    )
    cmd_parser.add_argument(
        "-w",
        "--width",
        default=40,
        metavar="WIDTH",
        type=int,
        help="Width (in pixels) to which individual .bmp images will be resized prior \
to stitching. Defaults to 40. Original width is 256.",
    )
    cmd_parser.add_argument(
        "-c",
        "--color",
        default="#00000000",
        metavar="COLOR",
        help="Background color. Accepts CSS3-style color specifiers. Defaults to \
transparent.",
    )
    cmd_parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Supress command line output. Defaults to off.",
    )
    args = cmd_parser.parse_args()

    # Fetch file names and coordinates
    filedict = stitch.coordinate_dict(path=args.path)
    if not filedict:
        raise SystemExit(f"No .bmp files found in {args.path}.")

    # Combine images
    combined = stitch.combine_images(filedict, tilewidth=args.width, color=args.color)
    combined.save(args.output)

    # Print message
    if not args.silent:
        print(
            f"Stitched together {len(filedict)} tiles with tile size of {args.width} x \
{args.width} pixels as {args.output} ({combined.width} x {combined.height} px)."
        )


if __name__ == "__main__":
    main()
