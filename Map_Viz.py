"""
Map-Based Visualization.

This interactive visulization lets the user choose
which sensor to observe how differnt car traffic
is over the course of seperate times of the day
(i.e. morning, day and night).
"""

from PIL import Image

import pandas as pd

from collections import Counter

from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, HoverTool, TapTool
from bokeh.models.widgets import CheckboxButtonGroup
from bokeh.plotting import figure, curdoc

import numpy as np

df = pd.read_csv('Lekagul Sensor Data.csv')
df_matrix = df['car-type'].as_matrix()
car_type_list = sorted(list(np.unique(df_matrix)))
legend_var = ['2 axle car (or motorcycle)', '2 axle Truck',
              'Ranger', '3 axle Truck', '4 axle (and above) Truck',
              '2 axle Bus', '3 axle Bus']

just_time = df['Timestamp'].str[-8:]
just_time = just_time.values
for i, edit in enumerate(just_time):
    just_time[i] = just_time[i].replace(':', '')
    just_time[i] = int(just_time[i])

df.Timestamp = just_time
df.loc[df.Timestamp < 119999, 'Timestamp'] = df.loc[df.Timestamp < 119999,
                                                    'Timestamp'].values + 240000


# Start at Night
# Morning: 4-12
morning_start = 40000 + 240000
morning_end = 119999 + 240000
# Day: 12-8
day_start = 120000
day_end = 199999
# Night: 8-4
night_start = 200000
night_end = 280000
mask = (df['Timestamp'] >= night_start) & (df['Timestamp'] <= night_end)
df_time = df.loc[mask]


im_url = 'Lekagul Roadways.bmp'
im = Image.open(im_url)
im = np.array(im.convert('RGB'))
plot_height = 500
plot_width = 500

N = 200
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
Names_Real = ['entrance0', 'ranger-stop4', 'ranger-stop1', 'camping5', 'gate2',
              'camping2', 'camping3', 'camping4', 'camping0', 'gate1', 'entrance0',
              'gate0', 'general-gate1', 'general-gate7', 'general-gate4',
              'ranger-stop2', 'ranger-stop0', 'gate7', 'ranger-stop7',
              'general-gate2', 'general-gate0', 'entrance3', 'gate6',
              'ranger-stop6', 'general-gate5', 'ranger-base', 'camping1',
              'gate5', 'general-gate6', 'gate8', 'entrance4', 'ranger-stop3',
              'gate3', 'camping6', 'ranger-stop5', 'gate4', 'camping7', 'camping8',
              'entrance1', 'general-gate3']
Names = ['Entrance 1', 'Ranger Stop 4', 'Ranger Stop 1', 'Camping 5', 'Gate 2',
         'Camping 2', 'Camping 3', 'Camping 4', 'Camping 0', 'Gate 1', 'Entrance 0',
         'Gate 0', 'General Gate 1', 'General Gate 7', 'General Gate 4',
         'Ranger Stop 2', 'Ranger Stop 0', 'Gate 7', 'Ranger Stop 7',
         'General Gate 2', 'General Gate 0', 'Entrance 3', 'Gate 6',
         'Ranger Stop 6', 'General Gate 5', 'Ranger Base', 'Camping 1',
         'Gate 5', 'General Gate 6', 'Gate 8', 'Entrance 4', 'Ranger Stop 3',
         'Gate 3', 'Camping 6', 'Ranger Stop 5', 'Gate 4', 'Camping 7', 'Camping 8',
         'Entrance 1', 'General Gate 3']

color_tot = ['green', 'blue', 'red', 'yellow', 'orange']
color_list = []
for col_fil in Names:
    if 'Entrance' in col_fil:
        color_list.append(color_tot[0])
    if 'Gate' in col_fil:
        if 'General' in col_fil:
            color_list.append(color_tot[1])
        else:
            color_list.append(color_tot[2])
    if 'Ranger' in col_fil:
        color_list.append(color_tot[3])
    if 'Camping' in col_fil:
        color_list.append(color_tot[4])

data = dict([('X', x_list), ('Y', y_list),
            ('Name', Names), ('Names_Real', Names_Real),
            ('Color', color_list)])
data_img = dict([('url', [im_url])])
car_types = ['1', '2', '2P', '3', '4', '5', '6']
data_int = dict([('Car-Type', car_types),
                 ('Count', [0, 0, 0, 0, 0, 0, 0]),
                 ('Real_Names', legend_var)])

tap = TapTool()
hover = HoverTool()
hover.tooltips = [("Sensor Name", "@Name")]

source = ColumnDataSource(data)
img_souce = ColumnDataSource(data_img)
int_source = ColumnDataSource(data_int)

CheckBox_list = ['Morning', 'Day', 'Night']
CBG = CheckboxButtonGroup(labels=CheckBox_list, active=[2])

p = figure(plot_height=plot_height, plot_width=plot_width,
           match_aspect=True, tools=[tap, hover, 'lasso_select'])
p_int = figure(plot_height=plot_height, plot_width=1000,
               x_range=legend_var)

p.image_url(url=['https://raw.githubusercontent.com/john-guerra/vastChallenge2017'
                 '_example/master/minichallenge_1/Lekagul%20Roadways.bmp'], x=0, y=0, w=2, h=2,
            angle=np.pi / 2)
p.circle(x='X', y='Y', source=source, size=10,
         alpha=0.9, color='Color')
p_int.vbar(x='Real_Names', bottom=0, width=1, top='Count',
           source=int_source, line_color='white')
empty = False


def update(attr, old, new):
    """
    Taptool/Selection Update.

    Trying to use to taptool/other selections
    for good stuff
    """
    inds = source.selected['1d']['indices']
    check_time = CBG.active
    if len(check_time) == 1:
        if 0 in check_time:
            mask = (df['Timestamp'] >= morning_start) & (df['Timestamp'] <= morning_end)
            df_time = df.loc[mask]
        if 1 in check_time:
            mask = (df['Timestamp'] >= day_start) & (df['Timestamp'] <= day_end)
            df_time = df.loc[mask]
        if 2 in check_time:
            mask = (df['Timestamp'] >= night_start) & (df['Timestamp'] <= night_end)
            df_time = df.loc[mask]

    if len(check_time) == 2:
        if 0 not in check_time:
            mask = (df['Timestamp'] >= day_start) & (df['Timestamp'] <= night_end)
            df_time = df.loc[mask]
        if 1 not in check_time:
            mask = (df['Timestamp'] >= night_start) & (df['Timestamp'] <= morning_end)
            df_time = df.loc[mask]
        if 2 not in check_time:
            mask = (df['Timestamp'] >= night_start) & (df['Timestamp'] <= morning_end)
            df_time = df.loc[~mask]
    if check_time == [0, 1, 2]:
        df_time = df
    if check_time == []:
        print('Please Select a Time')

    sel = []
    for zero in range(7):
        int_source.data['Count'][zero] = 0
    for x in inds:
        sel.append(source.data['Names_Real'][x])
    sel_df = df_time[df_time['gate-name'].isin(sel)]
    cars_ar = sel_df['car-type'].as_matrix()
    count_changer = []
    holdcount = 0
    if inds != []:
        types, counts = zip(*sorted(Counter(cars_ar).items()))
        for i, type_check in enumerate(car_type_list):
            if type_check in types:
                count_changer.append(counts[holdcount])
                holdcount += 1
            else:
                count_changer.append(0)
        int_source.data['Count'] = count_changer
    else:
        int_source.data['Count'] = np.zeros(7)

p.xaxis.major_tick_line_color = None
p.xaxis.minor_tick_line_color = None

p.yaxis.major_tick_line_color = None
p.yaxis.minor_tick_line_color = None

p.xaxis.major_label_text_font_size = '0pt'
p.yaxis.major_label_text_font_size = '0pt'
"""


p_int.yaxis.major_label_orientation = np.pi / 2
p_int.xaxis.major_label_orientation = -np.pi / 6
p_int.xaxis.axis_label = 'Traffic Through Select Points (For Given)'
"""
source.on_change('selected', update)
CBG.on_change('active', update)
curdoc().add_root(column(row(p, p_int), CBG))
