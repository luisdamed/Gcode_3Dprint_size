def get_max_size(text):
        
        pattern_xy= 'G1.X(\d*.\d*).Y(\d*.\d*).E\d*.\d*.;.perimeter'
        pattern_z = 'G1.Z(\d*.\d*).F\d*.\d*.;.restore.layer.Z'
        pattern_width = ';TYPE:Perimeter\n;WIDTH:(\d*.\d*).'
        
        matches_xy = re.findall(pattern_xy, text)
        x = list(list(zip(*matches_xy))[0])
        y = list(list(zip(*matches_xy))[1])
        x = [float(el) for el in x]
        y = [float(el) for el in y]

        matches_z = re.findall(pattern_z, text)
        z = [float(el) for el in matches_z]
        
        matches_width = re.findall(pattern_width, text)
        widths = [float(el) for el in matches_width]
        avg_width = sum(widths)/len(widths)
        print(f'Avg. width: {avg_width:.2f} mm')
        
        x_max = max(x) - min(x) + avg_width
        y_max = max(y) - min(y) + avg_width
        z.sort()
        z_max = z[-1]
        return f'Max. X dimension: {x_max:.2f} mm\n'\
               f'Max. Y dimension: {y_max:.2f} mm\n'\
               f'Max. Z dimension: {z_max:.2f} mm\n'\

import re
import timeit
input_file = 'Shape-Box_0.2mm_PLA_MINI_25m.gcode'

with open(input_file, 'r') as f:
                lines = f.readlines()  # List of strings, one for each line 

text_string  = ''.join(lines) # Large string containing all the text


num_tests = 100
test_time = timeit.timeit('print(get_max_size(text_string))', 
              setup='from __main__ import get_max_size, text_string',
              number=num_tests)
print(f'Number of lines of G-Code file is: {len(lines)}')
print(f'Average execution time is {test_time/num_tests} seconds, tested {num_tests} times')

