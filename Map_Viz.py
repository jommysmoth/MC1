"""Fuck off and Die."""

from PIL import Image

import pandas as pd

from bokeh.models import ColumnDataSource, TapTool, HoverTool
from bokeh.plotting import figure, output_file, show

import numpy as np
output_file('Map_Gates_Tap.html')

df = pd.read_csv('Lekagul Sensor Data.csv')
df_matrix = df['gate-name'].as_matrix()
gate_names = np.unique(df_matrix)


im = Image.open('Lekagul Roadways.bmp')
N = 200
plot_height = 750
plot_width = 750

im = np.asarray(im.convert('RGB'))
lab_im = np.zeros((N, N))
color_pal = np.chararray((N, N), itemsize=10)

x_listhold = []
y_listhold = []
full_list = []
for j in range(im.shape[0]):
    for i, x in enumerate(im[:, j, :]):
        hex = '#%02x%02x%02x' % tuple(x)
        if x[0] == x[1] == x[2]:
            fill = x.sum()
        else:
            x_listhold.append(i)
            y_listhold.append(j)
x_list = []
y_list = []
x_list[:] = [x / 100 for x in x_listhold]
y_list[:] = [x / 100 for x in y_listhold]
Names = ['Entrance 1', 'Ranger Stop 4', 'Ranger Stop 1', 'Camping 5', 'Gate 2',
         'Camping 2', 'Camping 3', 'Camping 4', 'Camping 0', 'Gate 1', 'Entrance 0',
         'Gate 0', 'General Gate 1', 'General Gate 7', 'General Gate 4',
         'Ranger Stop 2', 'Ranger Stop 0', 'Gate 7', 'Ranger Stop 7',
         'General Gate 2', 'General Gate 0', 'Entrance 3', 'Gate 6',
         'Ranger Stop 6', 'General Gate 5', 'Ranger Base', 'Camping 1',
         'Gate 5', 'General Gate 6', 'Gate 8', 'Entrance 4', 'Ranger Stop 3',
         'Gate 3', 'Camping 6', 'Ranger Stop 5', 'Gate 4', 'Camping 7', 'Camping 8',
         'Entrance 1', 'General Gate 3']

data = dict([('X', x_list), ('Y', y_list), ('Name', Names)])

tap = TapTool()
hover = HoverTool()
hover.tooltips = [("Sensor Name", "@Name")]

source = ColumnDataSource(data)

p = figure(plot_height=plot_height, plot_width=plot_width,
           match_aspect=True, tools=[tap, hover])

p.image_url(url=['Lekagul Roadways.bmp'], x=0, y=0, w=2, h=2,
            angle=np.pi / 2)
p.circle(x='X', y='Y', source=source, size=10,
         alpha=0.9, color='red')
p.line(x='X', y='Y', source=source, color='pink')


def update(attr, old, new):
    """
    Taptool Update.

    Trying to use to taptool for good stuff
    """
    inds = np.array(new['1d']['indicies'])
    print(inds)

p.xaxis.major_tick_line_color = None
p.xaxis.minor_tick_line_color = None

p.yaxis.major_tick_line_color = None
p.yaxis.minor_tick_line_color = None

p.xaxis.major_label_text_font_size = '0pt'
p.yaxis.major_label_text_font_size = '0pt'

show(p)
