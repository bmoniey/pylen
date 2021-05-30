# PYLEN - Python Filament Length Generator:

A utility for extracting filament usage by layer from your 3D printer gcode.
The output can be used for making multi-color 3D prints with a single extruder by welding filament segments together. A simple filament welder is linked below.

## Outputs
- Plot of filament length at the end of each layer
- Filament Layer Report as CSV
- Cut Length Work Sheet which allows the user to define segments and calculates the filament cut lengths

## Filament Welder:
- [Filament Welder on GrabCAD](https://grabcad.com/library/3dprint-filament-welder-1)
- [Filament Welder on Thingiverse](https://www.thingiverse.com/thing:4736586)
    
## Pylen GUI:

 ![pylen_gui](https://github.com/bmoniey/pylen/blob/master/pylen_gui_screenshot.jpg?raw=true)

## Example Cut Length Worksheet

![Cut Length Worksheet](https://github.com/bmoniey/pylen/blob/master/pylen_clen_ui.png?raw=true)

## Example Plot of Filament Usage by Layer:

![Layer_Plot](https://github.com/bmoniey/pylen/blob/master/pylen_plot_example.png?raw=true)

## Multi Color Print Samples:

 ![multi_color_print](https://github.com/bmoniey/pylen/blob/master/gallery/avl_logo_blue_silver_white.png)
 
# Binaries:
- [Latest Binaries](https://github.com/bmoniey/pylen/tree/master/dist)
- No installer, just unzip to a folder and run pylen.exe

# Release Notes:

## Version 1.2.0 May 29,2021
- Added support for units. Milli-Meter,Meter,Inch
- moved all file paths to settings object

## Version 1.1.1 May 22, 2021

- Issue1 Header Layer count not equal to layers found in gcode.
Resolved in this version by truncating the data based
the End of Gcode tag.
The layer count is reset and the length data is truncated to the new layer count.

## Version 1.1.0 January 30, 2021

- Added cut length work sheet with segment support
- Added support for basic settings

## Version 1.0.0 January 23, 2021

- Tested only in Windows 7,Windows 10
- Tested only using Cura slicer generated gcode
- Tested using Ender 3 profile
- Tested only so far with Marlin Flavor gcode

# TODO:

- Test this utility with various gcode flavors
- Test out on some other operating systems (any volunteers)
- Create a plugin for cura

## Running from source:
### Firstime install requirements
`pip install -r requirements.txt`

### run pylen_main.py
`python -m pylen_main.py`

## build your own window exe
`python -m pylen_setup.y build`

