# pylen
Python Filament Length Generator
        <html><head/>
        <body><p>Pylen Help:</p>
        <p>Program Purpose:</p>
        <p>Read 3DPrinter Gcode and extract filament usage per layer.
        The filamanent usage is the cumulative filament used at the &quot;END&quot; of each layer.
        </p>
        <p/>Uses:
        <p/>-Estimate filament used per layer
        <p/>-Plan layer color usage for multi color printing
        <p>File-&gt;Open</p>
        <p>Sets the path to the gcode file to be read. The default behavior is to set the report output path as the gcode_file.csv</p>
        <p>Report File Path</p><p>The path where pylen generates its report information as a .csv format which can be opened in a spreadsheet program</p><p>Generate:</p>
        <p>After the gcode path has been set using the File-&gt;Open action. Click on the Generate Button to create a usage report and display a usage graph</p>
        <p>Notes:</p>
        <p>Tested using Cura withe Ender 3 profile / Marlin flavor gcode!</p>
        <p>Send sample gcode for your printer to b.moniey@gmail.com to help add new flavors</p>
        </body></html>
        
 ![pylen_gui](https://github.com/[bmoniey]/[pylen]/pylen_gui_screenshot.jpg?raw=true)
 

Release Notes:
Version 1.0.0
Tested only in Windows 7
Tested only using Cura generated gcode
Tested using Ender 3 profile
Tested only so far with Marlin Flavor gcode

TODO:
-would like to add feature adding concept of layer segments
-these segment would allow generator of filament segment cut legths which can be used on a multi-color print
