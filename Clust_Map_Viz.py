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
from bokeh.models import Span, Label
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

car_type_for_ob = '4'
Label_for_insp = 3

mask_select = (df['car-type'] == car_type_for_ob) & (df['Label'] == Label_for_insp)
df_new_viz = df.loc[mask_select]
select_car_ar = np.unique(df_new_viz['car-id'].as_matrix())

doc = curdoc()

source_map = ColumnDataSource()


p = figure(title='Datetime Data of Each Vehicle Id \n Car Type: \n Cluster Label: ',
           plot_width=800, plot_height=500, y_range=gates)

check_max = []
for it, id in enumerate(select_car_ar):
    # Purposefully full dataframe of car (Later could highlight cluster
    # only actions)
    mask_car = df['car-id'] == id
    df_temp = df.loc[mask_car]
    map_data_time = df_temp['Timestamp'].values
    map_data_gate = df_temp['gate-name'].values
    check_max.append(len(map_data_gate))
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
                   end=max(check_max) - 1,
                   value=0,
                   step=1,
                   title='Which Point to See')

p2 = figure(plot_height=500, plot_width=500, x_range=(0, 2), y_range=(0, 2),
            match_aspect=True, tools=[hover], title='Lekagul Preserve (Sensor Data Shown)')

p2.image_url(url=['https://raw.githubusercontent.com/john-guerra/vastChallenge2017'
                  '_example/master/minichallenge_1/Lekagul%20Roadways.bmp'], x=0, y=0, w=2, h=2,
             angle=np.pi / 2)
p2.circle(x='X', y='Y', source=source, size=10,
          alpha=0.9, color='Color')

p2.xaxis.major_tick_line_color = None
p2.xaxis.minor_tick_line_color = None

p2.yaxis.major_tick_line_color = None
p2.yaxis.minor_tick_line_color = None
animation_count = 0

df_callback = source.to_df()

start_val = source_map.data['Y'][0]
x1 = float(df_callback['X'].loc[df_callback['Names_Real'] == start_val].values)
x2 = float(df_callback['X'].loc[df_callback['Names_Real'] == start_val].values)
y1 = float(df_callback['Y'].loc[df_callback['Names_Real'] == start_val].values)
y2 = float(df_callback['Y'].loc[df_callback['Names_Real'] == start_val].values)

data = dict([('X', [x1, x2]),
             ('Y', [y1, y2])])
source_new = ColumnDataSource(data)


def update(attr, new, old):
    """
    Slider Update.

    Lets user chose which instance of vehicle travelling, in
    order to use the secondary slider to observe the path of
    specific vehicle over map overlay via sensor data over time
    (scale given on secondary graph)
    """
    seq_val = int(seq_Slider.value)
    in_val = int(in_Slider.value)
    seq_str_x = 'Timestamp ' + str(seq_val)
    seq_str_y = 'Gate ' + str(seq_val)
    source_map.data['X'] = source_map.data[seq_str_x]
    source_map.data['Y'] = source_map.data[seq_str_y]
    mask_val = []
    for mask_it in range(in_val + 1):
        mask_val.append(source_map.data['Y'][mask_it])
    df_out = df_callback[df_callback['Names_Real'].isin(mask_val)]
    x1 = float(df_out['X'].loc[df_out['Names_Real'] == mask_val[0]].values)
    x2 = float(df_out['X'].loc[df_out['Names_Real'] == mask_val[in_val]].values)
    y1 = float(df_out['Y'].loc[df_out['Names_Real'] == mask_val[0]].values)
    y2 = float(df_out['Y'].loc[df_out['Names_Real'] == mask_val[in_val]].values)
    out_x = [x1, x2]
    out_y = [y1, y2]
    source_new.data['X'] = out_x
    source_new.data['Y'] = out_y
    start_date = source_map.data['X'][in_val]
    start_date = float(start_date)
    highlight_start.location = start_date
    label.x = start_date
    if in_val != 0:
        x1 = float(df_out['X'].loc[df_out['Names_Real'] == mask_val[in_val]].values)
        x2 = float(df_out['X'].loc[df_out['Names_Real'] == mask_val[in_val - 1]].values)
        y1 = float(df_out['Y'].loc[df_out['Names_Real'] == mask_val[in_val]].values)
        y2 = float(df_out['Y'].loc[df_out['Names_Real'] == mask_val[in_val - 1]].values)
        out_x = [x1, x2]
        out_y = [y1, y2]
        p2.line(x=out_x, y=out_y, line_color='purple', line_width=6)


p2.circle(x='X', y='Y', source=source_new, size=15, color='purple')

start_date = source_map.data['X'][0]
start_date = float(start_date) / 1000000

highlight_start = Span(location=start_date,
                       dimension='height', line_color='green',
                       line_dash='dashed', line_width=3)

label = Label(x=start_date, y=0, text='Sensor')

p.add_layout(highlight_start)
p.add_layout(label)

p.xaxis.formatter = DatetimeTickFormatter(minutes=["%B %d %H:%M:%S"],
                                          hours=["%B %d %H:%M:%S"],
                                          days=["%d %B %Y"],
                                          months=["%d %B %Y"],
                                          years=["%d %B %Y"])

seq_Slider.on_change('value', update)
in_Slider.on_change('value', update)
doc.add_root(column(row(p2, p), seq_Slider, in_Slider))
