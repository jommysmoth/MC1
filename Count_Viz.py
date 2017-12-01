"""
Counting Vizulization.

This file, when executed with bokeh serve --show  Count_Viz.py
gives a stacked bar vizulization of how different car types
travel between different gate, any given interval of time
"""

import pandas as pd
import numpy as np
from datetime import date, datetime
from bokeh.plotting import ColumnDataSource, figure, show, output_file, curdoc
from bokeh.palettes import Spectral9
from bokeh.models import CustomJS
from collections import Counter
from bokeh.layouts import column
from bokeh.core.properties import value
import matplotlib.pyplot as plt
from bokeh.models import HoverTool
from bokeh.models.widgets import DateRangeSlider

data = pd.read_csv('Lekagul Sensor Data.csv')
data_car_id = data['car-id'].as_matrix()
data.columns
plot_width = 1100
plot_height = 500
width = 1

hover = HoverTool()
hover.tooltips = [('index', '$index')]
all_gate_names = np.unique(data['gate-name'].as_matrix())
all_car_types = np.unique(data['car-type'].as_matrix())
source = ColumnDataSource()
source.add(all_gate_names, name='Gate Names')
legend_var = ['2 axle car (or motorcycle)', '2 axle Truck',
              'Ranger', '3 axle Truck', '4 axle (and above) Truck',
              '2 axle Bus', '3 axle Bus']

start_y = '2016'
start_m = '02'
start_d = '10'
end_y = '2016'
end_m = '04'
end_d = '20'
start_mask = '2016-02-10'
end_mask = '2016-04-20'

mask = (data['Timestamp'] >= start_mask) & (data['Timestamp'] <= end_mask)
time_dude = data.loc[mask]
print(time_dude)
for iter, car_type in enumerate(all_car_types):
    df = time_dude[time_dude['car-type'] == car_type]
    gate_values = df['gate-name'].values
    labels, values = zip(*sorted(Counter(gate_values).items()))
    labels = list(labels)
    values = list(values)
    for i in all_gate_names:
        if i not in labels:
            labels.append(i)
            values.append(0)
    zipped = sorted(zip(labels, values))
    labels, values = zip(*zipped)
    labels = np.asarray(labels)
    values = np.asarray(values)
    source.add(values, name=car_type)

date_slider = DateRangeSlider(title='Date Range',
                              start=date(2015, 5, 1),
                              end=date(2016, 5, 30),
                              value=(date(int(start_y),
                                          int(start_m),
                                          int(start_d)),
                                     date(int(end_y),
                                          int(end_m),
                                          int(end_d))),
                              step=1)
color = ['blue', 'red', 'yellow',
         'purple', 'cyan', 'black', 'green']


def date_range_update(attrname, old, new):
    """
    Callback for Date Range Slider Interaction.

    All of previous created for the ColumnDataSource
    must be redone in the update in order to correctly
    interact with the graph.
    """
    d1 = datetime.fromtimestamp(date_slider.value[0] / 1000)
    d2 = datetime.fromtimestamp(date_slider.value[1] / 1000)
    start_mask = d1.strftime('%Y-%m-%d')
    end_mask = d2.strftime('%Y-%m-%d')
    mask = (data['Timestamp'] >= start_mask) & (data['Timestamp'] <= end_mask)
    time_dude = data.loc[mask]
    for iter, car_type in enumerate(all_car_types):
        df = time_dude[time_dude['car-type'] == car_type]
        gate_values = df['gate-name'].values
        labels, values = zip(*sorted(Counter(gate_values).items()))
        labels = list(labels)
        values = list(values)
        for i in all_gate_names:
            if i not in labels:
                labels.append(i)
                values.append(0)
        zipped = sorted(zip(labels, values))
        labels, values = zip(*zipped)
        labels = np.asarray(labels)
        values = np.asarray(values)
        source.data[car_type] = values


p = figure(plot_width=plot_width, plot_height=plot_height,
           x_range=labels, tools=[hover])
p.vbar_stack(all_car_types,
             x='Gate Names',
             width=width,
             source=source,
             color=color,
             line_color='white',
             legend=[value(x) for x in legend_var],
             muted_color=color,
             muted_alpha=0.25)
p.xaxis.major_label_orientation = 1.2
p.legend.location = 'top_left'
p.legend.click_policy = 'mute'
date_slider.on_change('value', date_range_update)
curdoc().add_root(column(p, date_slider))

, 48, 51, 54, 361, 255, 66, 471, 57