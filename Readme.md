# Get 3D print size from G-Code

This is a simple script I made to determine the maximum dimensions of a 3D print job from its G-code.

I've created a WebApp that you can use to check the dimensions of a model by uploading a gcode file. (*-> URL to be updated*)

Alternatively, running the script for [local usage](localGUI/gcode_3dprint_size.py) will launch a GUI that allows selecting a number of .gcode, .gco, or .txt files to analyze. The output will be written in the command prompt, as in the following example:
```
>> File: Shape-Box_0.2mm_PLA_MINI_25m
>> Avg. width:  0.44 mm
>> Max. X dimension: 18.00 mm
>> Max. Y dimension: 18.00 mm
>> Max. Z dimension: 18.00 mm
```
The dimensions are found using Regexes, therefore, as of now, it only works for G-Code generated from [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/)(tested on version 2.5.0+win64) with Verbosed G-code. It might work for other software based on [Slic3r](https://slic3r.org/), and can definitely be customized to work with [Cura](https://ultimaker.com/software/ultimaker-cura).


## About this
Read more on [this blog article I wrote](https://www.makerluis.com/getting-the-size-of-3d-print-from-gcode/).

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E3FQ4XO)
