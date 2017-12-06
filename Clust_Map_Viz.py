"""
Using Clustering Data For Map Based Visualization.

Actively shows interesting Data from Clusters made in
a useful Visualization

"""
import numpy as np

from PIL import Image

from collections import Counter

from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Slider

import pandas as pd

df = pd.read_csv('Dataframe_Labels.csv')
gates = np.unique(df['gate-name'].values)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

plot_height = 500
plot_width = 500


num_most_common = 50000
common_cars = Counter(df['car-id']).most_common(num_most_common)
id_tag, counter_value = zip(*common_cars)
df = df[df['car-id'].isin(id_tag)]

mask_select = (df['car-type'] == '4') & (df['Label'] == 3)
df_new_viz = df.loc[mask_select]
select_car_ar = np.unique(df_new_viz['car-id'].as_matrix())

doc = curdoc()

source_map = ColumnDataSource()


p = figure(title='Not  Sure Yet', plot_width=1200, plot_height=800,
           y_range=gates)


for it, id in enumerate(select_car_ar):
    # Purposefully full dataframe of car (Later could highlight cluster
    # only actions)
    mask_car = df['car-id'] == id
    df_temp = df.loc[mask_car]
    map_data_time = df_temp['Timestamp'].values
    map_data_gate = df_temp['gate-name'].values
    source_map.add(map_data_time, name='Timestamp ' + str(it))
    source_map.add(map_data_gate, name='Gate ' + str(it))
source_map.add(source_map.data['Timestamp 0'], name='X')
source_map.add(source_map.data['Gate 0'], name='Y')

p.line(x='X', y='Y', source=source_map)
p.circle(x='X', y='Y', source=source_map, size=10, color='red')

im_url = 'Lekagul Roadways.bmp'
im = Image.open(im_url)
im = np.array(im.convert('RGB'))
plot_height = 500
plot_width = 500

hover = HoverTool()
hover.tooltips = [("Sensor Name", "@Name")]

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

source = ColumnDataSource(data)

seq_Slider = Slider(start=0,
                    end=it,
                    value=0,
                    step=1,
                    title='Which Instance to Monitor')

in_Slider = Slider(start=0,
                   end=13,
                   value=0,
                   step=1,
                   title='Which Point to See')

p2 = figure(plot_height=800, plot_width=800, x_range=(0, 2), y_range=(0, 2),
            match_aspect=True, tools=[hover])

p2.image_url(url=['https://raw.githubusercontent.com/john-guerra/vastChallenge2017'
                  '_example/master/minichallenge_1/Lekagul%20Roadways.bmp'], x=0, y=0, w=2, h=2,
             angle=np.pi / 2)
p2.circle(x='X', y='Y', source=source, size=10,
          alpha=0.9, color='Color')

p.xaxis.formatter = DatetimeTickFormatter(minutes=["%B %d %H:%M:%S"],
                                          hours=["%B %d %H:%M:%S"],
                                          days=["%d %B %Y"],
                                          months=["%d %B %Y"],
                                          years=["%d %B %Y"])

p2.xaxis.major_tick_line_color = None
p2.xaxis.minor_tick_line_color = None

p2.yaxis.major_tick_line_color = None
p2.yaxis.minor_tick_line_color = None
animation_count = 0

df_callback = source.to_df()


def update(attr, new, old):
    """
    Animation Update.

    Should be able to update both graphs in
    order to show how the vehicle moves over
    the map over all of the given dates of
    data.
    """
    seq_val = int(seq_Slider.value)
    in_val = int(in_Slider.value)
    seq_str_x = 'Timestamp ' + str(seq_val)
    seq_str_y = 'Gate ' + str(seq_val)
    source_map.data['X'] = source_map.data[seq_str_x]
    source_map.data['Y'] = source_map.data[seq_str_y]
    """
    x = []
    y = []
    x.append(source.data['X'][in_val])
    y.append(source.data['Y'][in_val])
    x.append(0)
    y.append(0)
    print('Here')
    data = dict([('X', x),
                ('Y', y)])
    print('No Here')
    source_new = ColumnDataSource(data)
    print('Could be here')
    p2.circle(x='X', y='Y', source=source_new,
              size=15, color='purple')
    """
    df_callback


seq_Slider.on_change('value', update)
in_Slider.on_change('value', update)
doc.add_root(column(row(p2, p), seq_Slider, in_Slider))
