import pandas as pd
import numpy as np
from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.palettes import Spectral9
from collections import Counter
from bokeh.layouts import row
from bokeh.core.properties import value
import matplotlib.pyplot as plt
output_file('Testing.html')

data = pd.read_csv('Lekagul Sensor Data.csv')
data_car_id = data['car-id'].as_matrix()
data.columns
plot_width = 1000
plot_height = 1000
width = 1

data['car-int-id'] = pd.factorize(data['car-id'])[0]+1
# Replacing unique car id with factorized integer for ease
data['gate-name-int'] = pd.factorize(data['gate-name'])[0] + 1

all_gate_names = np.unique(data['gate-name'].as_matrix())
all_car_types = np.unique(data['car-type'].as_matrix())
source = ColumnDataSource()
source.add(all_gate_names, name='Gate Names')
for car_type in all_car_types:
	df = data[data['car-type'] == car_type]
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

legend_var = ['2 axle car (or motorcycle)', '2 axle Truck', 'Ranger', '3 axle Truck','4 axle (and above) Truck', '2 axle Bus', '3 axle Bus']
p = figure(plot_width=plot_width, plot_height=plot_height,
           x_range=labels)
p.vbar_stack(all_car_types,
             x='Gate Names',
             width=width,
             source=source,
             color=['blue', 'red', 'yellow',
             'purple', 'cyan', 'black', 'green'],
             line_color='white',
             legend=[value(x) for x in legend_var])
p.xaxis.major_label_orientation = 1.2
p.legend.location = 'top_left'

show(p)