# pylen
# Python Filament Length Generator:

A GUI written in python for extracting filament usage by layer from your 3D printers gcode.
The output of the GUI is a plot of the cumulative filament usage at the end of each layer.
A report is generated as a CSV file for the user. Use this along with your Cura slicer generate the gcode. Use the layer preview to identify where you want the layers to start one color and begin on another. Use the data in the report to calculate the length of filamant used on each layer. The plan is for future versions of this utility to automate this step. The filament can be welded together to form segments which start and end at just the right time to make beautiful multi-color prints on a signle nozzle printer.

This utility is especially useful for making multi color 3D prints possible with a single extruder printer like the Ender 3.

## Filament Welder which makes splicing filament easy:
- [Filament Welder on GrabCAD](https://grabcad.com/library/3dprint-filament-welder-1)
- [Filament Welder on Thingiverse](https://www.thingiverse.com/thing:4736586)
    
## Pylen GUI:

 ![pylen_gui](https://github.com/bmoniey/pylen/blob/master/pylen_gui_screenshot.jpg?raw=true)

## Example Plot of Filament Usage by Layer:

![Layer_Plot](https://github.com/bmoniey/pylen/blob/master/pylen_plot_example.png?raw=true)

## Multi Color Print Sample:

 ![multi_color_print](https://github.com/bmoniey/pylen/blob/master/pylen_multi_color_print_magykdragon_logo.JPG?raw=true)

# Binaries:
[Latest Binaries](https://github.com/bmoniey/pylen/tree/master/dist)

# Release Notes:

## Version 1.0.0

- Tested only in Windows 7,Windows 10
- Tested only using Cura slicer generated gcode
- Tested using Ender 3 profile
- Tested only so far with Marlin Flavor gcode

# TODO:
- add feature adding concept of layer segments
- Segment feature would allow generation of filament cut sheet
- test this utility with various gcode flavors
- test out on some other operating systems (any volunteers)
- create a plugin for cura

## Running from source:
### Firstime install requirements
`pip install -r requirements.txt`

### run pylen_main.py
`python -m pylen_main.py`

