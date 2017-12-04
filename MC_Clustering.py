"""
Clustering.

Attempting to cluster the data for finding cars
exhibiting behavior outside of the norm labelsl.
"""

from sklearn.cluster import KMeans, DBSCAN
from collections import Counter

import numpy as np

from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.core.properties import value

import pandas as pd
from datetime import datetime
import time

km = DBSCAN(eps=5, min_samples=4)

# km = KMeans(n_clusters=5)

df = pd.read_csv('Lekagul Sensor Data.csv')
df_matrix = df['car-type'].as_matrix()
car_type_list = sorted(list(np.unique(df_matrix)))
df['gate-name-int'] = pd.factorize(df['gate-name'])[0]
df['car-type-int'] = pd.factorize(df['car-type'])[0]

legend_var = ['2 axle car (or motorcycle)', '2 axle Truck',
              'Ranger', '3 axle Truck', '4 axle (and above) Truck',
              '2 axle Bus', '3 axle Bus']

d = df['Timestamp'].values

time_fill = []
for i, x in enumerate(d):
    hold_time = datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    hold_time = time.mktime(hold_time.timetuple())
    d[i] = hold_time

data_cluster_test = df[['Timestamp', 'gate-name-int', 'car-type-int']]
data_cluster_train = data_cluster_test.sample(1000)

km.fit(data_cluster_train.values)

y_cluster = km.fit_predict(data_cluster_test.values)

df['Label'] = y_cluster
clust_num = np.unique(y_cluster)
print(len(clust_num))

mask = df['Label'] == -1
df_clean = df.loc[~mask]
print(df_clean)

Cluster_Names = []
for clust in clust_num:
    if clust != -1:
        cluster_name_fill = 'Cluster ' + str(clust)
        Cluster_Names.append(cluster_name_fill)

data = dict([('Real_Cars', Cluster_Names)])

color = ['blue', 'red', 'yellow',
         'purple', 'cyan', 'black', 'green']

source = ColumnDataSource(data)

new_zipper = []
for x in car_type_list:
    mask = df['car-type'] == x
    car_df = df.loc[mask]
    zipper = Counter(car_df['Label'].values).items()
    label, counts = zip(*zipper)
    check = list(set(clust_num) - set(label))
    re_zip = list(zip(label, counts))
    for filler in check:
        re_zip.append((filler, 0))
    re_zip_fill = [i for i in re_zip if i[0] != -1]
    label, counts = zip(*sorted(re_zip_fill))
    source.add(counts, name=x)


p = figure(title='Labeled Clusters Sorted by Car Type (No Outliers)',
           plot_height=600, plot_width=1000, x_range=Cluster_Names)

p.vbar_stack(car_type_list,
             x='Real_Cars',
             source=source,
             width=1,
             color=color,
             line_color='white',
             legend=[value(x) for x in legend_var],
             muted_color=color,
             muted_alpha=0.25)

p.legend.location = 'top_left'
p.legend.click_policy = 'mute'
p.xaxis.major_label_orientation = 1.2
show(p)