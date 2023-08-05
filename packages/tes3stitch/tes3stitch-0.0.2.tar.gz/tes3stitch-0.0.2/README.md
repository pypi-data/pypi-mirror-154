# tes3stitch

A small command line utility to stitch together the .bmp images created by the CreateMaps console command in [The Elder Scrolls III: Morrowind](https://store.steampowered.com/app/22320/The_Elder_Scrolls_III_Morrowind_Game_of_the_Year_Edition/).

[CreateMaps](https://en.uesp.net/wiki/Morrowind_Mod:CreateMaps) generates a large set of 256x256 pixel .bmp images of all exterior cells in the Morrowind/Maps folder. This Python 3 utility leverages the [pillow](https://python-pillow.org/) library to stitch the individual files into a single image according to their coordinates.

Using command line arguments, you can specify the folder where the .bmp files are located, the output path/filename and file type, the size per each cell (which controls the resulting size and resolution of the output file) and the background color (if any).

The approach was inspired by the [MWMOD-CreateMaps Assembly Script](https://en.uesp.net/wiki/File:MWMOD-CreateMaps_Assembly_Script.zip) by Seneca73, Atrayonis and mort.

## Installing and usage

1. Read the short UESP [guide to CreateMaps](https://en.uesp.net/wiki/Morrowind_Mod:CreateMaps) and run the command in Morrowind.exe, ensuring that the .bmp files are generated.
2. [Install Python 3](https://wiki.python.org/moin/BeginnersGuide/Download) on your computer, if not already present. Make sure it is of version 3.6 or later. The Python distribution should come packaged with PyPI.
3. Open a terminal (e.g., "cmd.exe" on Windows) and type `python3 -m pip install tes3stitch`.
4. Change your working directory to the `Maps` directory under your main Morrowind install directory and run `python3 -m tes3stitch`. Alternatively, run the script in whichever directory and specify the path to the `Maps` directory using the `-p` option.
5. Find the finished map in the same folder, under the name of `CellExport.png` (by default).
6. For configuration options, run `python3 -m tes3stitch -h` on the terminal.

## Future ideas

1. Provide a GUI with configuration options.
