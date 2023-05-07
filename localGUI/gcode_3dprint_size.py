# %% Import libraries

import os
import tkinter as tk
from tkinter import filedialog
import re


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Select GCODE file to analyze")
        self.label.pack()

        self.file_list = tk.Listbox(self.master, selectmode=tk.MULTIPLE)
        self.file_list.pack()

        self.select_button = tk.Button(self.master, text="Select files", command=self.select_files)
        self.select_button.pack()

        self.analyze_button = tk.Button(self.master, text="Analyze dimensions", command=self.analyze_dimensions)
        self.analyze_button.pack()

    def select_files(self):
        filetypes = [('GCODE files', '*.gco;*.gcode;*.txt')]
        files = filedialog.askopenfilenames(filetypes=filetypes)
        for file in files:
            self.file_list.insert(tk.END, file)

    
    def get_max_size( self, lines):
        
        pattern_xy= 'G1.X(\d*.\d*).Y(\d*.\d*).E\d*.\d*.;.perimeter'
        pattern_z = 'G1.Z(\d*.\d*).F\d*.\d*.;.restore.layer.Z'
        pattern_width = ';TYPE:Perimeter\n;WIDTH:(\d*.\d*).'
        
        matches_xy = re.findall(pattern_xy, lines)
        x = list(list(zip(*matches_xy))[0])
        y = list(list(zip(*matches_xy))[1])
        x = [float(el) for el in x]
        y = [float(el) for el in y]

        matches_z = re.findall(pattern_z, lines)
        z = [float(el) for el in matches_z]
        
        matches_width = re.findall(pattern_width, lines)
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

    def analyze_dimensions(self):
        for file in self.file_list.get(0, tk.END):
            input_file = os.path.abspath(file)
            filename = os.path.splitext(os.path.basename(file))[0]
            
            with open(input_file, 'r') as f:
                lines = f.readlines()
            print(f'File: {filename}')
            print(self.get_max_size(''.join(lines)))  
        self.file_list.delete(tk.ANCHOR)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.pack()
    root.mainloop()