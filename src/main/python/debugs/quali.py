from support.propagation_models import cost231_path_loss, fspl_path_loss, log_distance_path_loss, hata_path_loss
import io
import sys
import random
import folium
import numpy as np
import matplotlib
import matplotlib.cm
from haversine import haversine, Unit
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from scipy.constants import pi, speed_of_light
from math import log10


def calc_distance(point_1, point_2, unit=Unit.KILOMETERS):
    return haversine(point_1, point_2, unit=unit)


def mw_to_dbm(mw):
    """
    Método que converte a potência recebida dada em mW para dBm
    :param mw: Valor em miliwatts.
    :return: Valor de miliwatts convertido para decibéis.
    """
    return 10. * log10(mw)

def print_map(plot=False):
    ERB_LOCATION = (-21.226244, -44.978407)

    transmitted_frequency = 1872.500
    transmitted_power = 40 # 46.02 # 40W -> 46.02
    SENSITIVITY = -134

    n_lats, n_lons = (40, 40)
    lat_bounds = (-21.211645, -21.246091)  # lat_bounds[1]
    long_bounds = (-44.995876, -44.954157)  # long_bounds[0]

    lats_deg = np.linspace((lat_bounds[0]), (lat_bounds[1]), n_lats)
    lons_deg = np.linspace((long_bounds[0]), (long_bounds[1]), n_lons)

    lats_in_rad = np.deg2rad(lats_deg)
    longs_in_rad = np.deg2rad(lons_deg)

    lons_mesh, lats_mesh = np.meshgrid(longs_in_rad, lats_in_rad)

    lats_mesh_deg = np.rad2deg(lats_mesh)
    lons_mesh_deg = np.rad2deg(lons_mesh)

    distances = []
    distances_pl = []

    propagation_matrix = np.empty([n_lats, n_lons])
    for i, point_long in enumerate(lons_deg):
        for j, point_lat in enumerate(lats_deg):
            point = (point_lat, point_long)
            distance = calc_distance(ERB_LOCATION, point)

            tx_h = 56  # Base station height 30 to 200m
            rx_h = 1  # Mobile station height 1 to 10m
            mode = 2  # 1 = URBAN, 2 = SUBURBAN, 3 = OPEN

            path_loss = cost231_path_loss(transmitted_frequency, tx_h, rx_h, distance, mode)
            received_power = (mw_to_dbm(transmitted_power * 1000)) - path_loss

            distances.append(distance)
            distances_pl.append(received_power)

            propagation_matrix[i][j] = received_power
            # if received_power >= SENSITIVITY:
            #     propagation_matrix[i][j] = received_power
            # else:
            #     propagation_matrix[i][j] = 0

    distance_y = calc_distance((lat_bounds[0], long_bounds[0]), (lat_bounds[1], long_bounds[0]))  # |
    distance_x = calc_distance((lat_bounds[0], long_bounds[0]), (lat_bounds[0], long_bounds[1]))  # --
    print("Tamanho matrix de dados calculado: ", propagation_matrix.shape)
    print("Área: ", distance_y, "x", distance_x, "=", round(distance_y * distance_x, 2), "km2")
    # ------------------------------------------------------------------------------------------------------------------
    # N = 256
    # vals = np.ones((N, 4))
    # vals[:, 0] = np.linspace(90 / 256, 1, N)
    # vals[:, 1] = np.linspace(40 / 256, 1, N)
    # vals[:, 2] = np.linspace(40 / 256, 1, N)
    # newcmp = ListedColormap(vals)



    # get colormap
    ncolors = 512
    color_array = plt.get_cmap('YlOrRd')(range(ncolors))

    # change alpha values
    color_array[:, -1] = np.linspace(0.0, 1.0, ncolors)

    # create a colormap object
    map_object = LinearSegmentedColormap.from_list(name='rainbow_alpha', colors=color_array)

    # register this new colormap with matplotlib
    plt.register_cmap(cmap=map_object)

    # show some example data
    f, ax = plt.subplots()
    h = ax.imshow(np.random.rand(100, 100), cmap='rainbow_alpha')
    plt.colorbar(mappable=h)
    # ------------------------------------------------------------------------------------------------------------------

    # color_map = matplotlib.cm.get_cmap('YlOrRd')
    # color_map = matplotlib.cm.get_cmap('plasma')
    # color_map = matplotlib.cm.get_cmap('spring')
    # color_map = matplotlib.cm.get_cmap('summer')
    color_map = matplotlib.cm.get_cmap('rainbow_alpha') # custom
    # color_map = matplotlib.cm.get_cmap('gist_ncar')
    # color_map = matplotlib.cm.get_cmap('nipy_spectral')
    # color_map = matplotlib.cm.get_cmap('jet')
    # color_map = matplotlib.cm.get_cmap('Wistia')
    # color_map = matplotlib.cm.get_cmap('copper')
    # color_map = matplotlib.cm.get_cmap('Oranges')

    normed_data = (propagation_matrix - propagation_matrix.min()) / \
                  (propagation_matrix.max() - propagation_matrix.min())
    colored_data = color_map(normed_data)

    m = folium.Map(
        location=ERB_LOCATION,
        zoom_start=16,
        control_scale=True
    )

    folium.raster_layers.ImageOverlay(
        image=colored_data,
        bounds=[[lats_mesh_deg.min(), lons_mesh_deg.min()], [lats_mesh_deg.max(), lons_mesh_deg.max()]],
        mercator_project=True,

        opacity=0.4,
        interactive=True,
        cross_origin=False,
    ).add_to(m)

    folium.Marker(
        location=ERB_LOCATION,
        popup='Estação Rádio Base Vivo',
        draggable=False,
        icon=folium.Icon(prefix='glyphicon', icon='tower')
    ).add_to(m)

    # data = io.BytesIO()
    # m.save(data, close_file=False)
    # self.web_view.setHtml(data.getvalue().decode())
    m.save("quali.html")

    print(distances_pl)

    if plot:
        print("Num de itens: ", len(distances))
        fig, ax = plt.subplots()
        ax.plot(distances, distances_pl)

        ax.set(xlabel='Distancia (km)', ylabel='Potência recebida (dBw)', title='Potência do Sinal Recebido')
        ax.grid()
        plt.savefig("quali_dbw.png")
        plt.show()


def table():
    distances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    transmitted_frequency = 869.000  # 1872.500

    tx_h = 56  # Base station height 30 to 200m
    rx_h = 1  # Mobile station height 1 to 10m
    mode = 2  # 1 = URBAN, 2 = SUBURBAN, 3 = OPEN

    txPower = 75.185  # 14  # transmission power in dB
    antennaeGain = 15.9  # Total antennae gains(transmitter + receiver) in dB
    refDist = 1  # reference distance from the transceiver in meters
    refLoss = 20 * log10(
        (4 * pi * refDist * transmitted_frequency / speed_of_light))  # free space path loss at the reference distance
    ERP = txPower + antennaeGain - refLoss  # kind of the an equivalent radiation power

    path_loss_cost231 = []
    path_loss_fspl = []
    log_distance = []
    path_loss_hata = []

    for distance in distances:
        path_loss_cost231.append(cost231_path_loss(transmitted_frequency, tx_h, rx_h, distance, mode))

    for distance in distances:
        path_loss_fspl.append(fspl_path_loss(distance, transmitted_frequency))

    for distance in distances:
        log_distance.append(log_distance_path_loss(distance * 1000, gamma=3, d0=1, pr_d0=ERP, pt=txPower))

    for distance in distances:
        path_loss_hata.append(hata_path_loss(f=transmitted_frequency, h_B=tx_h, h_M=rx_h, d=distance, mode=2))

    fig, ax = plt.subplots()
    ax.plot(distances, path_loss_cost231)
    ax.plot(distances, path_loss_fspl)
    ax.plot(distances, log_distance)
    ax.plot(distances, path_loss_hata)

    ax.set(xlabel='Distancia (km)', ylabel='Path Loss (dB)',
           # title='Atenuação do Sinal - cost231'
           )
    ax.grid()
    plt.show()


if __name__ == '__main__':
    print_map(True)
    # table()
