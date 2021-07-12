import folium
import matplotlib
import numpy as np


def generate_propagation_map_layer(shape_of_propagation, lat_bounds, long_bounds, ):
    n_lats, n_lons = shape_of_propagation

    lats = np.linspace(np.deg2rad(lat_bounds[0]), np.deg2rad(lat_bounds[1]), n_lats)
    lons = np.linspace(np.deg2rad(long_bounds[0]), np.deg2rad(long_bounds[1]), n_lons)

    lons, lats = np.meshgrid(lons, lats)

    lats = np.rad2deg(lats)
    lons = np.rad2deg(lons)

    count = 1
    data = np.empty([n_lats, n_lons])
    for i in range(n_lons):
        for j in range(n_lats):
            data[i][j] = count
            count += 1

    print(data.shape)

    return lons, lats, data


lon, lat, data = generate_propagation_map_layer(
    lat_bounds=(-21.211645, -21.246091),
    long_bounds=(-44.995876, -44.954157),
    shape_of_propagation=(1000, 1000)
)

color_map = matplotlib.cm.get_cmap('rainbow')

print(type(data))

normed_data = (data - data.min()) / (data.max() - data.min())
colored_data = color_map(normed_data)

m = folium.Map(location=[-21.2262173, -44.9779183], zoom_start=14)

folium.raster_layers.ImageOverlay(
    image=colored_data,
    bounds=[[lat.min(), lon.min()], [lat.max(), lon.max()]],
    mercator_project=True,

    opacity=0.6,
    interactive=True,
    cross_origin=False,
).add_to(m)

m.save('sample.html')
