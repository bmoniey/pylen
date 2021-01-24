# pylen
Python Filament Length Generator
A GUI written in python for extracting filament usage by layer from your 3D printers gcode.
The output of the GUI is a plot of the cumulative filament usage at the end of each layer.
A report is generated as a CSV file for the user.

This utility is especially useful for making multi color 3D prints that have a single color per layer.
    
Pylen GUI:

 ![pylen_gui](https://github.com/bmoniey/pylen/blob/master/pylen_gui_screenshot.jpg?raw=true)

Multi Color Print Sample:

 ![pylen_gui](https://github.com/bmoniey/pylen/blob/master/pylen_multi_color_print_magykdragon_logo.jpg?raw=true)

Binaries:
        build/bdist.win32       microsoft msi install

Release Notes:
Version 1.0.0
Tested only in Windows 7
Tested only using Cura slicer generated gcode
Tested using Ender 3 profile
Tested only so far with Marlin Flavor gcode

TODO:
-would like to add feature adding concept of layer segments
-these segment would allow generator of filament segment cut legths which can be used on a multi-color print
-test this utility with various gcode flavors
