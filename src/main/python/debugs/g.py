
# -*- coding: utf-8 -*-

import branca
import folium
import geojsoncontour
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
import scipy.ndimage
from folium import plugins
from scipy.interpolate import griddata

# Setup
temp_mean = 2
temp_std = 20
debug = False

# Setup colormap
colors = ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba']
vmin = temp_mean - 2 * temp_std
vmax = temp_mean + 2 * temp_std
levels = len(colors)
cm = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax).to_step(levels)

df = pd.DataFrame({
    'latitude': np.random.normal(-21.2272003, 0.25, 500),
    'longitude': np.random.normal(-44.9783222, 0.25, 500),
    'temperature': np.random.randint(temp_mean, temp_std, 500)
})
# Create a dataframe with fake data

# The original data
x_orig = np.asarray(df.longitude.tolist())
y_orig = np.asarray(df.latitude.tolist())
z_orig = np.asarray(df.temperature.tolist())

# Make a grid
x_arr = np.linspace(np.min(x_orig), np.max(x_orig), 500)
y_arr = np.linspace(np.min(y_orig), np.max(y_orig), 500)
x_mesh, y_mesh = np.meshgrid(x_arr, y_arr)

# Grid the values
z_mesh = griddata((x_orig, y_orig), z_orig, (x_mesh, y_mesh), method='linear')

# Gaussian filter the grid to make it smoother
sigma = [15, 15]
z_mesh = sp.ndimage.filters.gaussian_filter(z_mesh, sigma, mode='constant')

# Create the contour
contourf = plt.contourf(x_mesh, y_mesh, z_mesh, levels, alpha=0.5, colors=colors, linestyles='None', vmin=vmin,
                        vmax=vmax)

# Convert matplotlib contourf to geojson
geojson = geojsoncontour.contourf_to_geojson(
    contourf=contourf,
    min_angle_deg=3.0,
    ndigits=5,
    stroke_width=1,
    fill_opacity=0.5)

# Set up the folium plot
geomap = folium.Map([df.latitude.mean(), df.longitude.mean()], zoom_start=10, tiles="cartodbpositron")

# Plot the contour plot on folium
folium.GeoJson(
    geojson,
    style_function=lambda x: {
        'color': x['properties']['stroke'],
        'weight': x['properties']['stroke-width'],
        'fillColor': x['properties']['fill'],
        'opacity': 0.6,
    }).add_to(geomap)

# Add the colormap to the folium map
cm.caption = 'Temperature'
geomap.add_child(cm)

# Fullscreen mode
plugins.Fullscreen(position='topright', force_separate_button=True).add_to(geomap)

# Plot the data
geomap.save(f'folium_contour_temperature_map.html')

xvalues = np.array([-41, -42, -43, -44, -45])
yvalues = np.array([-21, -22, -23, -24, -25])
xx, yy = np.meshgrid(xvalues, yvalues, )

print(xx)
print(yy)
