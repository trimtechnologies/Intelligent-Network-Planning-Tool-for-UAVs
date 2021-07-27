#!/usr/bin/env python

import io
import math
import sys
import time
from math import pi, cos, exp

import random
import copy

import folium
import numpy as np
import matplotlib
import matplotlib.cm
import matplotlib.pyplot as plt

from PyQt5 import uic, QtWebEngineWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QComboBox, QLineEdit, QLabel, QCheckBox
from PyQt5 import QtCore, QtWidgets
from folium import Map
from numpy.core.multiarray import ndarray
from typing import Tuple, List, Dict, Union, Any, Optional

from models.base_station import BaseStation
from controllers.base_station_controller import BaseStationController
from controllers.simulation_controller import SimulationController
from dialogs.alert_dialog_class import AlertDialogClass
from dialogs.about_dialog_class import AboutDialogClass
from dialogs.anatel_dialog_class import AnatelDialogClass
from dialogs.settings_dialog_class import SettingsDialogClass
from dialogs.help_dialog_class import HelpDialogClass
from dialogs.confirm_simulation_dialog_class import ConfirmSimulationDialogClass
from support.propagation_models import cost231_path_loss, log_distance_path_loss, log_distance_ref_d0, hata_path_loss, \
    two_rays_ground_reflection_path_loss
from support.constants import UFLA_LAT_LONG_POSITION, MIN_SENSITIVITY, SUBURBAN, \
    COST231_HATA_MODEL, FRISS_MODEL, TWO_RAYS_GROUND_REFLECTION_MODEL, LOG_DISTANCE_MODEL, ONE_SLOPE_MODEL, HATA_MODEL
from support.core import calculates_distance_between_coordinates, get_altitude, get_coordinate_in_circle
from support.physical_constants import r_earth

from base import context


class MainWindow(QMainWindow):
    """
    Main application class. This class load the main window
    """

    def __init__(self, parent=None):
        """
        Main window constructor
        :param parent:
        """
        # Init UI
        super().__init__()
        self.ui = uic.loadUi(context.get_resource("main_window.ui"), self)

        # Init controllers
        self.__base_station_controller = BaseStationController()
        self.__simulation_controller = SimulationController()

        # Init main map
        self.__init_rf_map()

        # Link calculate button with method
        self.button_calculate.clicked.disconnect()
        self.button_calculate.clicked.connect(self.on_button_calculate_clicked)

        # Init tha application menus
        self.__init_menus()

        # init tab components
        self.init_transmitter_components()
        self.init_receptor_components()
        self.init_model_components()
        self.init_simulated_annealing_components()
        self.init_output_components()

        self.set_default_values()

        # self.sub_area_bounds = [
        #     (-21.252142, -44.984765),
        #     (-21.252142, -45.013754),
        #     (-21.238862, -45.013754),
        #     (-21.238862, -44.984765),
        # ]

        # area menor
        # max_lat = -21.238862
        # min_lat = -21.252142
        # min_lng = -44.984765
        # max_lng = -45.013754

        # -45.055532,-21.276338,-44.939575,-21.223221

        # area maior
        max_lat = -21.223221
        min_lat = -21.276338
        min_lng = -44.939575
        max_lng = -45.055532

        self.sub_area_bounds = [
            (min_lat, min_lng),
            (min_lat, max_lng),
            (max_lat, max_lng),
            (max_lat, min_lng),
        ]

        # For more of one BS
        self.max_erb = 2

    def set_default_values(self):
        # Transmissor tab
        self.combo_box_anatel_base_station: QComboBox
        self.combo_box_anatel_base_station.setCurrentIndex(14)

        # Receptor tab
        self.input_rx_height: QLineEdit
        self.input_rx_gain: QLineEdit
        self.input_rx_sensitivity: QLineEdit

        self.input_rx_height.setText("2")
        self.input_rx_gain.setText("1")
        self.input_rx_sensitivity.setText("-180")

        # Propagation model tab
        self.combo_box_propagation_model: QComboBox
        self.combo_box_environment: QComboBox

        self.combo_box_propagation_model.setCurrentIndex(1)
        self.combo_box_environment.setCurrentIndex(1)

        # Meta-heuristic tab
        self.input_sa_temp_initial: QLineEdit
        self.input_sa_num_max_iterations: QLineEdit
        self.input_sa_num_max_perturbation_per_iteration: QLineEdit
        self.input_sa_num_max_success_per_iteration: QLineEdit
        self.input_sa_alpha: QLineEdit
        self.input_number_of_simulations: QLineEdit
        self.check_box_optimize_solution: QCheckBox
        self.check_box_optimize_height: QCheckBox
        self.check_box_optimize_power: QCheckBox
        self.check_box_save_simulations: QCheckBox

        self.input_sa_temp_initial.setText("200.0")
        self.input_sa_num_max_iterations.setText("2")
        self.input_sa_num_max_perturbation_per_iteration.setText("2")
        self.input_sa_num_max_success_per_iteration.setText("2")
        self.input_sa_alpha.setText("0.85")
        self.input_number_of_simulations.setText("1")
        self.check_box_optimize_solution.setChecked(True)
        self.check_box_optimize_height.setChecked(False)
        self.check_box_optimize_power.setChecked(False)
        self.check_box_save_simulations.setChecked(False)

        # Output tab
        self.combo_box_output_colour_scheme: QComboBox
        self.input_output_radius: QLineEdit

        self.combo_box_output_colour_scheme.setCurrentIndex(2)
        self.input_output_radius.setText("60")

        # Drone tab
        self.input_drone_transmit_power: QLineEdit
        self.input_drone_height: QLineEdit
        self.input_drone_frequency: QLineEdit

        self.input_drone_transmit_power.setText("40")
        self.input_drone_height.setText("70")
        self.input_drone_frequency.setText("869.0")

    def init_simulated_annealing_components(self) -> None:
        self.input_sa_temp_initial: QLineEdit
        self.input_sa_num_max_iterations: QLineEdit
        self.input_sa_num_max_perturbation_per_iteration: QLineEdit
        self.input_sa_num_max_success_per_iteration: QLineEdit
        self.input_sa_alpha: QLineEdit
        self.input_number_of_simulations: QLineEdit

    def init_output_components(self) -> None:
        self.combo_box_output_colour_scheme: QComboBox
        self.combo_box_output_colour_scheme.addItems([])
        self.combo_box_output_colour_scheme.currentIndexChanged.connect(
            self.on_combo_box_output_colour_scheme_changed)

    def init_model_components(self) -> None:
        self.combo_box_propagation_model: QComboBox
        self.combo_box_propagation_model.addItems([])
        self.combo_box_propagation_model.currentIndexChanged.connect(
            self.on_combo_box_propagation_model_changed)

        self.combo_box_environment: QComboBox
        self.combo_box_environment.addItems([])
        self.combo_box_environment.currentIndexChanged.connect(
            self.on_combo_box_environment_changed)

    def init_receptor_components(self) -> None:
        self.input_rx_height: QLineEdit
        self.input_rx_gain: QLineEdit
        self.input_rx_sensitivity: QLineEdit

    def init_transmitter_components(self) -> None:
        # For select a ERB
        self.combo_box_anatel_base_station: QComboBox

        self.fill_combo_box_anatel_base_station()
        self.combo_box_anatel_base_station.currentIndexChanged.connect(self.on_combo_box_anatel_base_station_changed)

    def fill_combo_box_anatel_base_station(self) -> None:
        db_configs = self.__base_station_controller.get_all_distinct()

        if db_configs is not None:
            for i, config in enumerate(db_configs):
                config: BaseStation
                self.combo_box_anatel_base_station.addItem(config.entidade + " - " + config.endereco, config.id)

    @pyqtSlot(name="on_combo_box_output_colour_scheme_changed")
    def on_combo_box_output_colour_scheme_changed(self) -> None:
        print("Items in the list 'combo_box_output_colour_scheme' are :")
        index = self.combo_box_output_colour_scheme.currentIndex()
        text = self.combo_box_output_colour_scheme.currentText()

        for count in range(self.combo_box_output_colour_scheme.count()):
            print(self.combo_box_output_colour_scheme.itemText(count))
        print("Current index", index, "selection changed ", text)

    @pyqtSlot(name="on_combo_box_environment_changed")
    def on_combo_box_environment_changed(self) -> None:
        print("Items in the list 'combo_box_environment' are :")
        index = self.combo_box_environment.currentIndex()
        text = self.combo_box_environment.currentText()

        for count in range(self.combo_box_environment.count()):
            print(self.combo_box_environment.itemText(count))
        print("Current index", index, "selection changed ", text)

    @pyqtSlot(name="on_combo_box_propagation_model_changed")
    def on_combo_box_propagation_model_changed(self) -> None:
        print("Items in the list 'combo_box_propagation_model' are :")
        index = self.combo_box_propagation_model.currentIndex()
        text = self.combo_box_propagation_model.currentText()

        for count in range(self.combo_box_propagation_model.count()):
            print(self.combo_box_propagation_model.itemText(count))
        print("Current index", index, "selection changed ", text)

    @pyqtSlot(name="on_combo_box_anatel_base_station_changed")
    def on_combo_box_anatel_base_station_changed(self) -> None:
        print("Items in the list 'combo_box_anatel_base_station' are :")
        self.combo_box_anatel_base_station: QComboBox
        index = self.combo_box_anatel_base_station.currentIndex()
        data = self.combo_box_anatel_base_station.itemData(index)

        erb = self.__base_station_controller.get_by_id(data)
        print("Index: " + str(index))
        print(erb.endereco)
        self.add_erb_map(erb)
        self.add_erb_in_details(erb)

    @pyqtSlot(name="on_combo_box_tx_coordinates_changed")
    def on_combo_box_tx_coordinates_changed(self) -> None:
        print("Items in the list 'combo_box_tx_coordinates' are :")
        index = self.combo_box_tx_coordinates.currentIndex()
        text = self.combo_box_tx_coordinates.currentText()

        for count in range(self.combo_box_tx_coordinates.count()):
            print(self.combo_box_tx_coordinates.itemText(count))
        print("Current index", index, "selection changed ", text)

    @pyqtSlot(name="on_menu_anatel_base_triggered")
    def on_menu_anatel_base_triggered(self) -> None:
        """
        This method is called when calculate button is clicked
        :return: None
        """
        anatel_dialog = AnatelDialogClass(self)
        anatel_dialog.setModal(True)
        anatel_dialog.setFixedSize(anatel_dialog.size())
        anatel_dialog.show()

    @pyqtSlot(name="on_menu_settings_triggered")
    def on_menu_settings_triggered(self) -> None:
        """
        This method is called when settings menu button is clicked
        :return: None
        """
        settings_dialog = SettingsDialogClass(self)
        settings_dialog.setModal(True)
        settings_dialog.show()

    @pyqtSlot(name="on_menu_about_triggered")
    def on_menu_about_triggered(self) -> None:
        """
        This method is called when about menu button is clicked
        :return: None
        """
        about_dialog = AboutDialogClass(self)
        about_dialog.setModal(True)
        about_dialog.show()

    @pyqtSlot(name="on_menu_help_triggered")
    def on_menu_help_triggered(self) -> None:
        """
        This method is called when help menu button is clicked
        :return: None
        """
        help_dialog = HelpDialogClass(self)
        help_dialog.setModal(True)
        help_dialog.show()

    @pyqtSlot(name="on_menu_exit_triggered")
    def on_menu_exit_triggered(self) -> None:
        """
        This method is called when exit menu button is clicked
        :return: None
        """
        sys.exit()

    @pyqtSlot(name="on_button_calculate_clicked")
    def on_button_calculate_clicked(self) -> None:
        """
        This method is called when calculate menu button is clicked
        :return: None
        """
        print("Calculate button!")

        # Check if input fields is fillers
        if not self.required_fields_fillers():
            return

        base_station_selected = self.get_bs_selected()
        propagation_model_selected = self.get_propagation_model_selected()

        data = {
            "simulation": {
                "propagation_model": propagation_model_selected['text'],
                "environment": str(self.combo_box_environment.currentText()),
                "max_ray": str(self.input_output_radius.text()) + "m"
            },
            "transmitter": {
                "entidade": str(base_station_selected.entidade),
                "uf_municipio": str(base_station_selected.uf),
                "endereco": str(base_station_selected.endereco)[0:35] + "...",
                "frequencia": str(base_station_selected.frequencia_inicial),
                "potencia_transmissao": str(base_station_selected.potencia_transmissao) + "W",
                "ganho": str(base_station_selected.ganho_antena) + "dBi",
                "elevacao": str(base_station_selected.elevacao),
                "polarizacao": str(base_station_selected.polarizacao),
                "altura": str(base_station_selected.altura) + "m",
                "latitude": str(base_station_selected.latitude),
                "longitude": str(base_station_selected.longitude),
            },
            "receptor": {
                "altura": str(self.input_rx_height.text()) + "m",
                "ganho": str(self.input_rx_gain.text()) + "dBi",
                "sensibilidade": str(self.input_rx_sensitivity.text()) + "dBm",
            },
            "heuristic": {
                "solucao_inicial": "(" + str(base_station_selected.latitude) + ", " + str(
                    base_station_selected.longitude) + ")",
                "temperatura_inicial": self.input_sa_temp_initial.text(),
                "numero_maximo_iteracoes": self.input_sa_num_max_iterations.text(),
                "numero_maximo_pertubacoes_por_iteracao": self.input_sa_num_max_perturbation_per_iteration.text(),
                "numero_maximo_sucessos_por_iteracao": self.input_sa_num_max_success_per_iteration.text(),
                "alpha": self.input_sa_alpha.text(),
                "optimize_solution": self.check_box_optimize_solution.isChecked(),
                "optimize_height": self.check_box_optimize_height.isChecked(),
                "optimize_power": self.check_box_optimize_power.isChecked(),
                "save_simulations": self.check_box_save_simulations.isChecked(),
                "number_of_simulations": self.input_number_of_simulations.text(),
            },
        }

        confirm_simulation_dialog = ConfirmSimulationDialogClass(data)
        confirm_simulation_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        confirm_simulation_dialog.setModal(True)
        confirm_simulation_dialog.setFixedSize(confirm_simulation_dialog.size())

        if confirm_simulation_dialog.exec_() == QtWidgets.QDialog.Accepted:
            total_simulations = int(self.input_number_of_simulations.text())
            for i in range(total_simulations):
                print("i/range=", i+1, "/", total_simulations)
                self.run_simulation()

    def add_erb_map(self, base_station: BaseStation) -> None:
        erb_location = (str(base_station.latitude), str(base_station.longitude))

        m = self.get_folium_map(location=erb_location)

        folium.Marker(
            location=erb_location,
            popup=base_station.entidade,
            draggable=False,
            icon=folium.Icon(prefix='glyphicon', icon='plane', color=base_station.color)
        ).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)

        self.web_view.setHtml(data.getvalue().decode())

    def add_erb_in_details(self, base_station: BaseStation) -> None:
        self.label_anatel_entity_value.setText(base_station.entidade)
        self.label_anatel_station_number_value.setText(base_station.num_estacao)
        self.label_anatel_uf_value.setText(base_station.uf)
        self.label_anatel_contry_value.setText(base_station.municipio)
        self.label_anatel_address_value.setText(base_station.endereco)
        self.label_anatel_final_frequency_value.setText(base_station.frequencia_final)
        self.label_anatel_initial_frequency_value.setText(base_station.frequencia_inicial)
        self.label_anatel_azimute_value.setText(base_station.azimute)
        self.label_anatel_gain_antenna_value.setText(base_station.ganho_antena)
        self.label_anatel_front_back_value.setText(base_station.ganho_frente_costa)
        self.label_anatel_half_pot_value.setText(base_station.angulo_meia_potencia)
        self.label_anatel_elevation_value.setText(base_station.elevacao)
        self.label_anatel_polarization_value.setText(base_station.polarizacao)
        self.label_anatel_height_antenna_value.setText(base_station.altura)
        self.label_anatel_power_transmission_value.setText(base_station.potencia_transmissao)
        self.label_anatel_latitude_value.setText(str(base_station.latitude))
        self.label_anatel_longitude_value.setText(str(base_station.longitude))
        self.label_anatel_first_licensing_value.setText(base_station.data_primeiro_licenciamento)

    def __init_menus(self) -> None:
        self.menu_action_exit.triggered.disconnect()
        self.menu_action_exit.triggered.connect(self.on_menu_exit_triggered)

        self.menu_action_anatel_base.triggered.disconnect()
        self.menu_action_anatel_base.triggered.connect(self.on_menu_anatel_base_triggered)

        self.menu_action_settings.triggered.disconnect()
        self.menu_action_settings.triggered.connect(self.on_menu_settings_triggered)

        self.menu_action_about.triggered.disconnect()
        self.menu_action_about.triggered.connect(self.on_menu_about_triggered)

        self.menu_action_help.triggered.disconnect()
        self.menu_action_help.triggered.connect(self.on_menu_help_triggered)

    def __init_rf_map(self) -> None:
        m = self.get_folium_map(UFLA_LAT_LONG_POSITION)

        data = io.BytesIO()
        m.save(data, close_file=False)

        self.web_view.setHtml(data.getvalue().decode())

    @staticmethod
    def get_folium_map(location=UFLA_LAT_LONG_POSITION, tiles="cartodb positron", zoom_start=16, control_scale=True) \
            -> Map:
        # tiles = "Stamen Terrain"
        return folium.Map(
            location=location,
            tiles=tiles,
            zoom_start=zoom_start,
            control_scale=control_scale
        )

    def required_fields_fillers(self) -> bool:
        title = None
        message = None

        if self.combo_box_anatel_base_station.currentIndex() == 0:
            title = "Selecione uma ERB"
            message = "ERB não selecionada! Selecione uma ERB para continuar..."

        if self.combo_box_propagation_model.currentIndex() == 0:
            title = "Selecione um modelo de propagação"
            message = "Modelo de propagação não selecionado! Selecione um modelo de propagação para continuar..."

        if self.combo_box_environment.currentIndex() == 0:
            title = "Selecione um ambiente"
            message = "Ambiente de propagação não selecionado! Selecione um ambiente de propagação para continuar..."

        if self.combo_box_output_colour_scheme.currentIndex() == 0:
            title = "Selecione um esquema de cores"
            message = "Esquema de cores não selecionada! Selecione um esquema de cores da propagação para continuar..."

        if not self.input_output_radius.text():
            title = "Raio Simulação"
            message = "Raio máximo de propagação não informado! Informe um raio máximo de propagação para continuar..."

        if not self.input_rx_height.text():
            title = "Altura RX"
            message = "Altura da antena receptora não informada! Informe uma altura para continuar..."

        if not self.input_rx_gain.text():
            title = "Ganho RX"
            message = "Ganho da antena receptora não informado! Informe o ganho para continuar..."

        if not self.input_rx_sensitivity.text():
            title = "Sensibilidade RX"
            message = "Sensibilidade da antena receptora não informada! Informe a Sensibilidade para continuar..."

        if title is not None and message is not None:
            AlertDialogClass(title, message).exec_()
            return False

        return True

    def get_bs_selected(self) -> BaseStation:
        self.combo_box_anatel_base_station: QComboBox
        index = self.combo_box_anatel_base_station.currentIndex()
        data = self.combo_box_anatel_base_station.itemData(index)

        base_station_selected: BaseStation
        return self.__base_station_controller.get_by_id(data)

    def get_propagation_model_selected(self) -> Dict[str, Union[int, Any]]:
        self.combo_box_propagation_model: QComboBox
        index = self.combo_box_propagation_model.currentIndex()
        data = self.combo_box_propagation_model.itemData(index)
        text = self.combo_box_propagation_model.currentText()

        return {
            'index': index,
            'data': data,
            'text': text
        }

    @staticmethod
    def objective_function(propagation_matrix: ndarray) -> float:
        fo_value = 0
        total_of_points = len(propagation_matrix) * len(propagation_matrix[0])

        for line in propagation_matrix:
            for value in line:
                if value >= MIN_SENSITIVITY:
                    fo_value += 1

        coverage_percent = (fo_value / total_of_points) * 100  # coverage percentage
        shadow_percent = 100 - coverage_percent  # shadow percentage

        fo_alpha = 7
        return (fo_alpha * coverage_percent) - ((10 - fo_alpha) * shadow_percent)  # weight 7 to 3

    @staticmethod
    def solution_overlap_max(propagation_array) -> ndarray:
        max_value = propagation_array[0]
        for i in range(1, len(propagation_array)):
            max_value = np.maximum(propagation_array[i], max_value)

        return max_value

    @staticmethod
    def __get_simulation_bounds(lat: float, long: float, dx: float, dy: float) \
            -> Tuple[Tuple[float, float], Tuple[float, float]]:

        new_latitude1 = lat + (round(dy / r_earth, 6)) * (round(180 / pi, 6))
        new_longitude1 = long + (round(dx / r_earth, 6)) * (round(180 / pi, 6)) / cos(round(lat * pi / 180, 6))

        new_latitude2 = lat - (round(dy / r_earth, 6)) * (round(180 / pi, 6))
        new_longitude2 = long - (round(dx / r_earth, 6)) * (round(180 / pi, 6)) / cos(round(lat * pi / 180, 6))

        lat_bounds = (round(new_latitude1, 6), round(new_latitude2, 6))
        long_bounds = (round(new_longitude1, 6), round(new_longitude2, 6))

        return lat_bounds, long_bounds

    @staticmethod
    def find_point(x1, y1, x2, y2, x, y):
        # print(x1, y1, x2, y2, x, y)

        return x1 < x < x2 and y1 < y < y2

    def is_point_inside_sub_area(self, point: Tuple) -> bool:
        # point = Feature(geometry=Point(point))
        # polygon = Polygon([self.sub_area_bounds])
        # return boolean_point_in_polygon(point, polygon)
        # -21.263461,-45.014334,-21.232582,-44.980860
        # http://bboxfinder.com/#-21.263461,-45.014334,-21.232582,-44.980860
        # Pegar coordenadas do Box e nao do Map
        return self.find_point(-21.263461, -45.014334, -21.232582, -44.980860, round(point[0], 6), round(point[1], 6))

    @staticmethod
    def percentage(percent: float, whole: float) -> float:
        return (percent * whole) / 100.0

    def calculates_path_loss(self, frequency: float, tx_h: float, rx_h: float, distance: float, mode: int,
                             pt: float = 0.0, g_t: float = 0.0, g_r: float = 0.0):
        self.combo_box_propagation_model: QComboBox
        pm = self.combo_box_propagation_model.currentIndex()

        if pm == COST231_HATA_MODEL:
            return cost231_path_loss(f=frequency, tx_h=tx_h, rx_h=rx_h, d=distance, mode=mode)
        elif pm == HATA_MODEL:
            return hata_path_loss(f=frequency, h_B=tx_h, h_M=rx_h, d=distance, mode=mode)
        elif pm == TWO_RAYS_GROUND_REFLECTION_MODEL:
            return two_rays_ground_reflection_path_loss(d=distance, g_t=g_t, g_r=g_r, h_t=tx_h, h_r=rx_h)
        elif pm == LOG_DISTANCE_MODEL:
            ref_d0 = log_distance_ref_d0(gamma=2, pt=pt)
            return log_distance_path_loss(d=distance, gamma=2, d0=1, pr_d0=ref_d0, pt=pt)
        elif pm == FRISS_MODEL:
            pass
        elif pm == ONE_SLOPE_MODEL:
            pass

    def simulates_propagation(self, base_station_selected: BaseStation) -> Tuple[
        ndarray, Union[ndarray, Tuple[ndarray, Optional[float]]], Union[ndarray, Tuple[ndarray, Optional[float]]]]:

        dy, dx = 6, 6  # 3km
        lat_bounds, long_bounds = self.__get_simulation_bounds(base_station_selected.latitude,
                                                               base_station_selected.longitude, dx, dy)
        # get coordinates list
        n_lats, n_longs = (500, 500)
        lats_deg = np.linspace((lat_bounds[0]), (lat_bounds[1]), n_lats)
        longs_deg = np.linspace((long_bounds[0]), (long_bounds[1]), n_longs)

        erb_location = (base_station_selected.latitude, base_station_selected.longitude)

        transmitted_power = float(base_station_selected.potencia_transmissao)

        altitude_tx = get_altitude(lat=erb_location[0], long=erb_location[1])

        rx_gain = float(self.input_rx_gain.text())

        #  Get limit altitudes
        min_altitude = math.inf
        max_altitude = - math.inf
        for i, point_long in enumerate(longs_deg):
            for j, point_lat in enumerate(lats_deg):
                altitude_point_terrain = get_altitude(lat=point_lat, long=point_long)

                if altitude_point_terrain < min_altitude:
                    min_altitude = altitude_point_terrain

                if altitude_point_terrain > max_altitude:
                    max_altitude = altitude_point_terrain

        propagation_matrix = np.empty([len(longs_deg), len(lats_deg)])

        height_rx = float(self.input_rx_height.text())

        for i, point_long in enumerate(longs_deg):
            for j, point_lat in enumerate(lats_deg):
                mobile_base_location = (point_lat, point_long)

                altitude_lat_long_rx = get_altitude(lat=point_lat, long=point_long)

                distance = calculates_distance_between_coordinates(mobile_base_location, erb_location)

                tx_h = (float(base_station_selected.altura) + altitude_tx) - min_altitude
                rx_h = (height_rx + altitude_lat_long_rx) - min_altitude

                path_loss = self.calculates_path_loss(frequency=float(base_station_selected.frequencia_inicial),
                                                      tx_h=tx_h, rx_h=rx_h, distance=distance, mode=SUBURBAN,
                                                      pt=float(base_station_selected.potencia_transmissao),
                                                      g_t=float(base_station_selected.ganho_antena), g_r=rx_gain)

                received_power = transmitted_power - path_loss

                consider_subareas = False
                # check if the is placed inside subrarea
                if consider_subareas and self.is_point_inside_sub_area(mobile_base_location):
                    propagation_matrix[i][j] = received_power + self.percentage(10, abs(received_power))
                else:
                    propagation_matrix[i][j] = received_power

        return propagation_matrix, lats_deg, longs_deg

    def print_simulation_result(self, base_station_selected: BaseStation, extra_points: List[BaseStation] = None) -> None:

        propagation_matrix, lats_deg, longs_deg = self.simulates_propagation(base_station_selected)

        main_erb_location = (base_station_selected.latitude, base_station_selected.longitude)

        lats_in_rad = np.deg2rad(lats_deg)
        longs_in_rad = np.deg2rad(longs_deg)

        longs_mesh, lats_mesh = np.meshgrid(longs_in_rad, lats_in_rad)

        lats_mesh_deg = np.rad2deg(lats_mesh)
        longs_mesh_deg = np.rad2deg(longs_mesh)

        color_map = matplotlib.cm.get_cmap('YlOrBr')

        print("propagation_matrix.min()=", propagation_matrix.min())
        print("propagation_matrix.max()=", propagation_matrix.max())

        # normed_data = (propagation_matrix - bm_min_sensitivity) / (bm_max_sensitivity - bm_min_sensitivity)
        normed_data = (propagation_matrix - propagation_matrix.min()) / (
                propagation_matrix.max() - propagation_matrix.min())

        colored_data = color_map(normed_data)

        m = self.get_folium_map(location=main_erb_location)

        folium.raster_layers.ImageOverlay(
            image=np.flip(colored_data, 1),
            bounds=[[lats_mesh_deg.min(), longs_mesh_deg.min()], [lats_mesh_deg.max(), longs_mesh_deg.max()]],
            mercator_project=True,
            opacity=0.6,
            interactive=True,
            cross_origin=False,
        ).add_to(m)

        # Print extra points in the map
        if extra_points is not None:
            for erb in extra_points:
                extra_erb_location = (erb.latitude, erb.longitude)

                folium.Marker(
                    location=extra_erb_location,
                    popup=erb.entidade,
                    draggable=False,
                    icon=folium.Icon(prefix='glyphicon', icon='plane', color=erb.color)
                ).add_to(m)

        # Print main point
        folium.Marker(
            location=main_erb_location,
            popup=base_station_selected.entidade,
            draggable=False,
            icon=folium.Icon(prefix='glyphicon', icon='plane', color=base_station_selected.color)
        ).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)

        self.web_view.setHtml(data.getvalue().decode())

    def run_simulation(self) -> None:
        self.check_box_save_simulations: QCheckBox
        save_simulations = self.check_box_save_simulations.isChecked()

        start = time.time()
        end = None

        self.check_box_optimize_solution: QCheckBox
        optimize_solution = self.check_box_optimize_solution.isChecked()

        base_station_selected = self.get_bs_selected()
        initial_solution = copy.deepcopy(base_station_selected)

        # Get propagation model text of select
        propagation_model = self.combo_box_propagation_model.currentText()

        # Get matrix result for matrix coordinates
        propagation_matrix, _, _ = self.simulates_propagation(base_station_selected)

        initial_fo = self.objective_function(propagation_matrix)

        print('propagation_matrix.shape=', propagation_matrix.shape)
        print('objective_function=', initial_fo)

        if optimize_solution:

            # Get values from inputs
            sa_temp_initial = float(self.input_sa_temp_initial.text())
            sa_num_max_iterations = int(self.input_sa_num_max_iterations.text())
            sa_num_max_perturbation_per_iteration = int(self.input_sa_num_max_perturbation_per_iteration.text())
            sa_num_max_success_per_iteration = int(self.input_sa_num_max_success_per_iteration.text())
            sa_alpha = float(self.input_sa_alpha.text())

            # Run simulated annealing
            best_array, _, FOs = self.simulated_annealing(base_station=base_station_selected, M=sa_num_max_iterations,
                                                          P=sa_num_max_perturbation_per_iteration,
                                                          L=sa_num_max_success_per_iteration,
                                                          T0=sa_temp_initial, alpha=sa_alpha)
            end = time.time()
            print("End of Simulated Annealing")

            #  print best solution found
            print("obtaining propagation matrix of the best solution...")
            # matrix_solution, _, _ = self.simulates_propagation(best_array)
            # best_fo = round(self.objective_function(matrix_solution), 2)
            best_fo, matrix_solution = self.evaluate_solution_array(best_array)

            print("generating visualization of the solution...")
            extra_bs = []

            print(self.get_lat_lng_from_array_solution(best_array))

            # best_array.color = 'red'
            # self.print_simulation_result(best_array, extra_bs)
            self.print_simulation_result(best_array[0], best_array[1:])

            print("len(FOs)=", len(FOs))

            print('(propagation_model)=', propagation_model)

            # Plot the objective function line chart
            print("generating graph of the behavior of the objective function...")
            FOs_to_plot = [item for item in FOs]
            print("FOs_to_plot=", FOs_to_plot)
            plt.plot(FOs_to_plot)
            plt.title("Comportamento do Simulated Annealing (" + str(propagation_model) + ")")
            plt.ylabel('Valor da FO')
            plt.xlabel('Solução candidata')
            plt.show()

            if save_simulations:
                print("Saving simulation in database...")
                data = {
                    "initial_latitude": str(initial_solution.latitude),
                    "initial_longitude": str(initial_solution.longitude),
                    "initial_height": str(initial_solution.altura),
                    "initial_power_transmission": str(initial_solution.potencia_transmissao),
                    "initial_objective_function": str(initial_fo),
                    "number_of_solutions": len(FOs) - 1,
                    "execution_seconds": str(end - start),
                    "started_at": str(start),
                    "ended_at": str(end),
                    "propagation_model": str(propagation_model),
                    "best_latitude": str(best_array.latitude),
                    "best_longitude": str(best_array.longitude),
                    "best_height": str(best_array.altura),
                    "best_power_transmission": str(best_array.potencia_transmissao),
                    "best_objective_function": str(best_fo),
                    "solutions": FOs
                }
                self.__simulation_controller.store(data)
                print("Done!")
        else:
            #  Show simulation map
            self.print_simulation_result(initial_solution)

        if end is None:
            end = time.time()

        self.label_geral_info_1: QLabel
        self.label_geral_info_1.setText("Simulação realizada com sucesso!")
        print("Simulation run in %s seconds" % round(end - start, 2))

        print("End of simulation!")

    def evaluate_solution(self, point: BaseStation) -> float:
        matrix_solution, _, _ = self.simulates_propagation(point)

        return self.objective_function(matrix_solution)

    def evaluate_solution_array(self, points: List[BaseStation]) -> Tuple[float, ndarray]:
        propagation_matrices = []

        for point in points:
            matrix_solution, _, _ = self.simulates_propagation(point)
            propagation_matrices.append(matrix_solution)

        overlaid_matrix = self.solution_overlap_max(propagation_matrices)

        return self.objective_function(overlaid_matrix), overlaid_matrix

    @staticmethod
    def disturb_solution(solution: BaseStation, disturbance_radius: float = 600) -> BaseStation:
        """
        Disturb a specific solution

        Args:
            solution: A base station solution
            disturbance_radius: The ray of disturbance in meters

        Returns:
            BaseStation:  Return the base station with a new position (lat long)
        """
        latitude = solution.latitude
        longitude = solution.longitude

        new_coordinates = get_coordinate_in_circle(latitude, longitude, disturbance_radius)

        solution.latitude = new_coordinates[0]
        solution.longitude = new_coordinates[1]

        return solution

    def generates_heights(self, height: float) -> list:
        """
        Function to get the possible heights for simulation

        Args:
            height (float): The main height

        Returns:
            list: Return a list of heights
        """
        percentage_height_15 = self.percentage(15, height)
        percentage_height_30 = self.percentage(30, height)

        self.combo_box_propagation_model: QComboBox
        self.check_box_optimize_height: QCheckBox

        pm = self.combo_box_propagation_model.currentIndex()

        pm_that_accept_height = pm == COST231_HATA_MODEL or pm == HATA_MODEL or pm == TWO_RAYS_GROUND_REFLECTION_MODEL

        if self.check_box_optimize_height.isChecked() and pm_that_accept_height:
            return [
                height - percentage_height_30,
                height - percentage_height_15,
                height,
                height + percentage_height_15,
                height + percentage_height_30,
            ]
        return [height]

    def generates_received_powers(self, power: float) -> list:
        """
        Function to get the possible transmission powers for simulation

        Args:
            power (float): The main transmission power

        Returns:
            list: Return a list of transmission powers
        """
        percentage_power_15 = self.percentage(15, power)
        percentage_power_30 = self.percentage(30, power)

        self.combo_box_propagation_model: QComboBox
        self.check_box_optimize_power: QCheckBox

        if self.check_box_optimize_power.isChecked():
            return [
                power - percentage_power_30,
                power - percentage_power_15,
                power,
                power + percentage_power_15,
                power + percentage_power_30,
            ]

        return [power]

    @staticmethod
    def get_lat_lng_from_array_solution(s_array: List[BaseStation]):
        positions = []
        for bs in s_array:
            positions.append({
                'latitude': bs.latitude,
                'longitude': bs.longitude,
                'color': bs.color
            })

        return positions

    def simulated_annealing(self, base_station: BaseStation, M: int, P: int, L: int, T0: float, alpha: float) \
            -> Tuple[Union[List[BaseStation], Any], float, List[float]]:
        """
        Performs the search using meta-heuristics

        Args:
            base_station: Main problem data.
            M: Maximum number of iterations.
            P: Maximum number of Disturbances per iteration.
            L: Maximum number of successes per iteration.
            T0: Initial temperature.
            alpha: Temperature reduction factor.

        Returns:
            Tuple: Returns a point (tuple of coordinates) being the most indicated.
        """

        # List of solutions found
        FOs = []

        # generate the array of solution
        s_array = []
        for _ in range(self.max_erb):
            s_array.append(copy.deepcopy(base_station))

        s0 = s_array.copy()

        antenna_height = float(base_station.altura)
        possible_heights = self.generates_heights(antenna_height)
        print("possible_heights=", str(possible_heights))

        antenna_power_received = float(base_station.potencia_transmissao)
        possible_powers_received = self.generates_received_powers(antenna_power_received)
        print("possible_powers_received=", str(possible_powers_received))

        print("Solução inicial: ")
        print(self.get_lat_lng_from_array_solution(s0))

        result = self.evaluate_solution_array(s_array)

        f_s = result[0]

        T = T0
        j = 1

        i_ap = 0

        # Store the BEST solution found
        best_s_array = s_array.copy()
        best_fs = f_s

        # Loop principal – Verifica se foram atendidas as condições de termino do algoritmo
        while True:
            print('T=', T)
            print("j/M=", j, "/", M)
            i = 1
            n_success = 0

            # Loop Interno – Realização de perturbação em uma iteração
            while True:
                print("i/P=", i, "/", P)
                print("n_success/L=", n_success, "/", L)

                initial_solutions_array = s_array.copy()

                # a cada iteração do SA, disturb_solution um dos APs
                i_ap = (i_ap + 1) % self.max_erb

                initial_solutions_array[i_ap] = self.disturb_solution(s_array[i_ap])

                # Get a different position to ERB
                # Si = self.disturb_solution(s)

                # For all possible antenna heights
                for height in possible_heights:
                    print("-----------------------")
                    print("antenna height=", height)
                    initial_solutions_array[i_ap].altura = height

                    for power in possible_powers_received:
                        print("transmission power=", power)
                        initial_solutions_array[i_ap].potencia_transmissao = power

                        # Get objective function value
                        result = self.evaluate_solution_array(initial_solutions_array)

                        f_si = result[0]

                        # Verificar se o retorno da função objetivo está correto. f(x) é a função objetivo
                        delta_fi = f_si - f_s

                        # Minimização: delta_fi >= 0
                        # Maximização: delta_fi <= 0
                        # Teste de aceitação de uma nova solução
                        if (delta_fi <= 0) or (exp(-delta_fi / T) > random.random()):

                            s_array = initial_solutions_array.copy()
                            f_s = f_si

                            n_success = n_success + 1

                            if f_s > best_fs:
                                best_fs = f_s
                                best_s_array = s_array.copy()

                            FOs.append(f_s)
                            # FOs.append({
                            #     "lat": Si.latitude,
                            #     "lng": Si.longitude,
                            #     "height": Si.altura,
                            #     "power": Si.potencia_transmissao,
                            #     "of": f_s
                            # })

                i = i + 1

                if (n_success >= L) or (i > P):
                    break

            # Atualização da temperatura (Decaimento geométrico)
            T = alpha * T

            # Atualização do contador de iterações
            j = j + 1

            if (n_success == 0) or (j > M):
                break

            print('n_success=', n_success)
            print('best_fs=', best_fs)

        print(len(FOs), " solutions covered")
        print('FOs=', str(FOs))

        FOs.append(best_fs)
        # FOs.append({
        #     "lat": best_s_array.latitude,
        #     "lng": best_s_array.longitude,
        #     "height": best_s_array.altura,
        #     "power": best_s_array.potencia_transmissao,
        #     "of": best_fs
        # })

        return best_s_array, best_fs, FOs