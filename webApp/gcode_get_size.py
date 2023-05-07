import re

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
        return f'{x_max:.2f}', f'{y_max:.2f}', f'{z_max:.2f}'


