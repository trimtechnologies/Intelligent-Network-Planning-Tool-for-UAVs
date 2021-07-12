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
        self.input_sa_num_max_iterations.setText("3")
        self.input_sa_num_max_perturbation_per_iteration.setText("5")
        self.input_sa_num_max_success_per_iteration.setText("140")
        self.input_sa_alpha.setText("0.85")
        self.input_number_of_simulations.setText("1")
        self.check_box_optimize_solution.setChecked(True)
        self.check_box_optimize_height.setChecked(True)
        self.check_box_optimize_power.setChecked(True)
        self.check_box_save_simulations.setChecked(True)

        # Output tab
        self.combo_box_output_colour_scheme: QComboBox
        self.input_output_radius: QLineEdit

        self.combo_box_output_colour_scheme.setCurrentIndex(2)
        self.input_output_radius.setText("60")

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

        # html = f"""
        #         <h1> {base_station.entidade}</h1>
        #         <p>You can use any html here! Let's do a list:</p>
        #         <ul>
        #             <li>Latitude: {base_station.latitude}</li>
        #             <li>Longitude: {base_station.longitude}</li>
        #         </ul>
        #         """
        # iframe = folium.IFrame(html=html, width=200, height=200)
        # popup = folium.Popup(iframe, max_width=2650)

        folium.Marker(
            location=erb_location,
            popup=base_station.entidade,
            draggable=False,
            icon=folium.Icon(prefix='glyphicon', icon='tower', color=base_station.color)
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

        coverage_percent = (fo_value / total_of_points) * 100  # porcentagem de cobertura
        shadow_percent = 100 - coverage_percent  # porcentagem de sombra

        fo_alpha = 7
        return (fo_alpha * coverage_percent) - ((10 - fo_alpha) * shadow_percent)  # pesos 7 pra 3

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

    def find_point(self, x1, y1, x2, y2, x, y):
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

        erb_location = (base_station_selected.latitude, base_station_selected.longitude)

        lats_in_rad = np.deg2rad(lats_deg)
        longs_in_rad = np.deg2rad(longs_deg)

        longs_mesh, lats_mesh = np.meshgrid(longs_in_rad, lats_in_rad)

        lats_mesh_deg = np.rad2deg(lats_mesh)
        longs_mesh_deg = np.rad2deg(longs_mesh)

        color_map = matplotlib.cm.get_cmap('YlOrBr')

        print("propagation_matrix.min()=", propagation_matrix.min())
        print("propagation_matrix.max()=", propagation_matrix.max())

        # dados normatizados
        # normed_data = (propagation_matrix - bm_min_sensitivity) / (bm_max_sensitivity - bm_min_sensitivity)
        normed_data = (propagation_matrix - propagation_matrix.min()) / (
                propagation_matrix.max() - propagation_matrix.min())

        colored_data = color_map(normed_data)

        m = self.get_folium_map(location=erb_location)

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
                erb_location = (erb.latitude, erb.longitude)

                folium.Marker(
                    location=erb_location,
                    popup=erb.entidade,
                    draggable=False,
                    icon=folium.Icon(prefix='glyphicon', icon='tower', color=erb.color)
                ).add_to(m)

        # Print main point
        folium.Marker(
            location=erb_location,
            popup=base_station_selected.entidade,
            draggable=False,
            icon=folium.Icon(prefix='glyphicon', icon='tower', color=base_station_selected.color)
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

        # print(propagation_matrix)
        print('propagation_matrix.shape=', propagation_matrix.shape)
        print('objective_function=', initial_fo)

        if optimize_solution:
            run_only_test = False

            if run_only_test:
                FOs = [{'lat': -21.222768035349166, 'lng': -44.97706843930947, 'height': 39.2, 'power': 42.0, 'of': -130.94}, {'lat': -21.222768035349166, 'lng': -44.97706843930947, 'height': 47.6, 'power': 42.0, 'of': -111.24399999999997}, {'lat': -21.222768035349166, 'lng': -44.97706843930947, 'height': 56.0, 'power': 42.0, 'of': -93.22}, {'lat': -21.222768035349166, 'lng': -44.97706843930947, 'height': 64.4, 'power': 42.0, 'of': -74.976}, {'lat': -21.222768035349166, 'lng': -44.97706843930947, 'height': 64.4, 'power': 51.0, 'of': 144.652}, {'lat': -21.222768035349166, 'lng': -44.97706843930947, 'height': 72.8, 'power': 42.0, 'of': -58.52400000000003}, {'lat': -21.222768035349166, 'lng': -44.97706843930947, 'height': 72.8, 'power': 51.0, 'of': 177.092}, {'lat': -21.2232355324757, 'lng': -44.980804836844214, 'height': 39.2, 'power': 42.0, 'of': -110.29599999999999}, {'lat': -21.2232355324757, 'lng': -44.980804836844214, 'height': 47.6, 'power': 42.0, 'of': -90.49999999999997}, {'lat': -21.2232355324757, 'lng': -44.980804836844214, 'height': 56.0, 'power': 42.0, 'of': -73.77199999999999}, {'lat': -21.2232355324757, 'lng': -44.980804836844214, 'height': 64.4, 'power': 42.0, 'of': -58.59200000000001}, {'lat': -21.2232355324757, 'lng': -44.980804836844214, 'height': 72.8, 'power': 42.0, 'of': -44.77199999999999}, {'lat': -21.22345617331082, 'lng': -44.97882015383907, 'height': 39.2, 'power': 42.0, 'of': -101.80399999999997}, {'lat': -21.22345617331082, 'lng': -44.97882015383907, 'height': 39.2, 'power': 51.0, 'of': 104.20800000000003}, {'lat': -21.22345617331082, 'lng': -44.97882015383907, 'height': 47.6, 'power': 42.0, 'of': -83.27600000000001}, {'lat': -21.22345617331082, 'lng': -44.97882015383907, 'height': 56.0, 'power': 42.0, 'of': -67.04800000000003}, {'lat': -21.22345617331082, 'lng': -44.97882015383907, 'height': 56.0, 'power': 51.0, 'of': 171.12800000000001}, {'lat': -21.22345617331082, 'lng': -44.97882015383907, 'height': 56.0, 'power': 78.0, 'of': 694.26}, {'lat': -21.22345617331082, 'lng': -44.97882015383907, 'height': 64.4, 'power': 42.0, 'of': -52.27599999999998}, {'lat': -21.22345617331082, 'lng': -44.97882015383907, 'height': 72.8, 'power': 42.0, 'of': -39.22799999999998}, {'lat': -21.223571424305284, 'lng': -44.97521470970552, 'height': 39.2, 'power': 42.0, 'of': -92.088}, {'lat': -21.223571424305284, 'lng': -44.97521470970552, 'height': 47.6, 'power': 42.0, 'of': -74.16799999999998}, {'lat': -21.223571424305284, 'lng': -44.97521470970552, 'height': 56.0, 'power': 42.0, 'of': -57.391999999999996}, {'lat': -21.223571424305284, 'lng': -44.97521470970552, 'height': 64.4, 'power': 42.0, 'of': -42.644000000000005}, {'lat': -21.223571424305284, 'lng': -44.97521470970552, 'height': 72.8, 'power': 42.0, 'of': -28.887999999999977}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 39.2, 'power': 42.0, 'of': -67.424}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 39.2, 'power': 60.0, 'of': 517.2239999999999}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 39.2, 'power': 69.0, 'of': 662.4719999999999}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 47.6, 'power': 42.0, 'of': -49.98399999999998}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 56.0, 'power': 42.0, 'of': -34.920000000000016}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 56.0, 'power': 51.0, 'of': 219.64}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 56.0, 'power': 60.0, 'of': 566.54}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 56.0, 'power': 78.0, 'of': 696.576}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 64.4, 'power': 42.0, 'of': -21.560000000000002}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 64.4, 'power': 69.0, 'of': 676.1800000000001}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 64.4, 'power': 78.0, 'of': 697.188}, {'lat': -21.222903643448394, 'lng': -44.971665304779734, 'height': 72.8, 'power': 42.0, 'of': -8.69599999999997}, {'lat': -21.223601964785495, 'lng': -44.972126784619846, 'height': 39.2, 'power': 42.0, 'of': -50.867999999999995}, {'lat': -21.223601964785495, 'lng': -44.972126784619846, 'height': 39.2, 'power': 51.0, 'of': 193.18}, {'lat': -21.223601964785495, 'lng': -44.972126784619846, 'height': 39.2, 'power': 69.0, 'of': 670.088}, {'lat': -21.223601964785495, 'lng': -44.972126784619846, 'height': 39.2, 'power': 78.0, 'of': 696.3280000000001}, {'lat': -21.223601964785495, 'lng': -44.972126784619846, 'height': 47.6, 'power': 42.0, 'of': -35.831999999999994}, {'lat': -21.223601964785495, 'lng': -44.972126784619846, 'height': 56.0, 'power': 42.0, 'of': -22.127999999999986}, {'lat': -21.223601964785495, 'lng': -44.972126784619846, 'height': 64.4, 'power': 42.0, 'of': -8.623999999999967}, {'lat': -21.223601964785495, 'lng': -44.972126784619846, 'height': 72.8, 'power': 42.0, 'of': 5.271999999999991}, {'lat': -21.22650793382981, 'lng': -44.974883196009905, 'height': 39.2, 'power': 42.0, 'of': -54.355999999999995}, {'lat': -21.22650793382981, 'lng': -44.974883196009905, 'height': 39.2, 'power': 51.0, 'of': 215.48000000000002}, {'lat': -21.22650793382981, 'lng': -44.974883196009905, 'height': 47.6, 'power': 42.0, 'of': -38.067999999999955}, {'lat': -21.22650793382981, 'lng': -44.974883196009905, 'height': 47.6, 'power': 51.0, 'of': 249.80799999999996}, {'lat': -21.22650793382981, 'lng': -44.974883196009905, 'height': 56.0, 'power': 42.0, 'of': -20.924000000000007}, {'lat': -21.22650793382981, 'lng': -44.974883196009905, 'height': 64.4, 'power': 42.0, 'of': -3.9799999999999898}, {'lat': -21.22650793382981, 'lng': -44.974883196009905, 'height': 72.8, 'power': 42.0, 'of': 12.379999999999995}, {'lat': -21.225441378951523, 'lng': -44.97774259617032, 'height': 39.2, 'power': 42.0, 'of': -70.77200000000002}, {'lat': -21.225441378951523, 'lng': -44.97774259617032, 'height': 47.6, 'power': 42.0, 'of': -55.551999999999964}, {'lat': -21.225441378951523, 'lng': -44.97774259617032, 'height': 47.6, 'power': 51.0, 'of': 211.192}, {'lat': -21.225441378951523, 'lng': -44.97774259617032, 'height': 56.0, 'power': 42.0, 'of': -39.668000000000006}, {'lat': -21.225441378951523, 'lng': -44.97774259617032, 'height': 56.0, 'power': 51.0, 'of': 245.372}, {'lat': -21.225441378951523, 'lng': -44.97774259617032, 'height': 56.0, 'power': 78.0, 'of': 697.056}, {'lat': -21.225441378951523, 'lng': -44.97774259617032, 'height': 64.4, 'power': 42.0, 'of': -24.055999999999955}, {'lat': -21.225441378951523, 'lng': -44.97774259617032, 'height': 72.8, 'power': 42.0, 'of': -9.584000000000003}, {'lat': -21.225145180739826, 'lng': -44.974517464623894, 'height': 39.2, 'power': 42.0, 'of': -60.964}, {'lat': -21.225145180739826, 'lng': -44.974517464623894, 'height': 47.6, 'power': 42.0, 'of': -44.964}, {'lat': -21.225145180739826, 'lng': -44.974517464623894, 'height': 56.0, 'power': 42.0, 'of': -29.50799999999998}, {'lat': -21.225145180739826, 'lng': -44.974517464623894, 'height': 64.4, 'power': 42.0, 'of': -14.724000000000075}, {'lat': -21.22537366539022, 'lng': -44.973303068618115, 'height': 39.2, 'power': 42.0, 'of': -44.843999999999994}, {'lat': -21.22537366539022, 'lng': -44.973303068618115, 'height': 47.6, 'power': 42.0, 'of': -29.17199999999997}, {'lat': -21.22537366539022, 'lng': -44.973303068618115, 'height': 56.0, 'power': 42.0, 'of': -13.604000000000013}, {'lat': -21.22537366539022, 'lng': -44.973303068618115, 'height': 64.4, 'power': 42.0, 'of': 1.3719999999999288}, {'lat': -21.22537366539022, 'lng': -44.973303068618115, 'height': 72.8, 'power': 42.0, 'of': 16.876000000000005}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 39.2, 'power': 42.0, 'of': -7.69199999999995}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 39.2, 'power': 51.0, 'of': 288.96400000000006}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 39.2, 'power': 60.0, 'of': 600.696}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 39.2, 'power': 69.0, 'of': 682.3120000000001}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 39.2, 'power': 78.0, 'of': 697.464}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 47.6, 'power': 42.0, 'of': 7.904000000000025}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 47.6, 'power': 69.0, 'of': 685.168}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 47.6, 'power': 78.0, 'of': 697.968}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 56.0, 'power': 42.0, 'of': 23.50799999999998}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 64.4, 'power': 42.0, 'of': 38.872000000000014}, {'lat': -21.22460679000056, 'lng': -44.970318114129384, 'height': 72.8, 'power': 42.0, 'of': 55.46799999999996}, {'lat': -21.224760927328912, 'lng': -44.968680982551376, 'height': 39.2, 'power': 42.0, 'of': 12.688000000000017}, {'lat': -21.224760927328912, 'lng': -44.968680982551376, 'height': 47.6, 'power': 42.0, 'of': 28.19999999999999}, {'lat': -21.224760927328912, 'lng': -44.968680982551376, 'height': 56.0, 'power': 51.0, 'of': 394.1159999999999}, {'lat': -21.224760927328912, 'lng': -44.968680982551376, 'height': 56.0, 'power': 69.0, 'of': 688.424}, {'lat': -21.224760927328912, 'lng': -44.968680982551376, 'height': 56.0, 'power': 78.0, 'of': 698.356}, {'lat': -21.224760927328912, 'lng': -44.968680982551376, 'height': 64.4, 'power': 42.0, 'of': 60.45599999999999}, {'lat': -21.225908887294224, 'lng': -44.96625550028057, 'height': 39.2, 'power': 42.0, 'of': -36.084}, {'lat': -21.225908887294224, 'lng': -44.96625550028057, 'height': 47.6, 'power': 42.0, 'of': -17.335999999999956}, {'lat': -21.225908887294224, 'lng': -44.96625550028057, 'height': 56.0, 'power': 42.0, 'of': -0.10000000000005116}, {'lat': -21.225908887294224, 'lng': -44.96625550028057, 'height': 56.0, 'power': 60.0, 'of': 604.956}, {'lat': -21.225908887294224, 'lng': -44.96625550028057, 'height': 56.0, 'power': 69.0, 'of': 681.94}, {'lat': -21.225908887294224, 'lng': -44.96625550028057, 'height': 56.0, 'power': 78.0, 'of': 695.752}, {'lat': -21.225908887294224, 'lng': -44.96625550028057, 'height': 64.4, 'power': 42.0, 'of': 16.767999999999972}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 39.2, 'power': 42.0, 'of': 76.67200000000003}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 47.6, 'power': 42.0, 'of': 96.01199999999997}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 64.4, 'power': 42.0, 'of': 134.29200000000003}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 64.4, 'power': 51.0, 'of': 505.664}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 64.4, 'power': 60.0, 'of': 662.532}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 64.4, 'power': 69.0, 'of': 693.552}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 64.4, 'power': 78.0, 'of': 699.688}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 72.8, 'power': 42.0, 'of': 153.71200000000005}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 72.8, 'power': 51.0, 'of': 522.9680000000001}, {'lat': -21.22758158898211, 'lng': -44.96701973056145, 'height': 39.2, 'power': 42.0, 'of': 47.512}, {'lat': -21.22758158898211, 'lng': -44.96701973056145, 'height': 47.6, 'power': 42.0, 'of': 66.93599999999995}, {'lat': -21.22758158898211, 'lng': -44.96701973056145, 'height': 56.0, 'power': 42.0, 'of': 86.15600000000003}, {'lat': -21.22758158898211, 'lng': -44.96701973056145, 'height': 56.0, 'power': 60.0, 'of': 649.1840000000001}, {'lat': -21.22758158898211, 'lng': -44.96701973056145, 'height': 56.0, 'power': 78.0, 'of': 699.052}, {'lat': -21.22758158898211, 'lng': -44.96701973056145, 'height': 64.4, 'power': 42.0, 'of': 105.22000000000008}, {'lat': -21.22758158898211, 'lng': -44.96701973056145, 'height': 72.8, 'power': 42.0, 'of': 124.0}, {'lat': -21.228004857501524, 'lng': -44.96663171818059, 'height': 64.4, 'power': 78.0, 'of': 699.688}]
                best_fo = FOs[-1]

                # The best solution found
                best = base_station_selected  # Just for clone
                best.latitude = best_fo["lat"]
                best.longitude = best_fo["lng"]
                best.potencia_transmissao = best_fo["power"]
                best.altura = best_fo["height"]
                best.color = 'red'

            else:
                # Run simulated annealing
                best, _, FOs = self.simulated_annealing(base_station=base_station_selected, M=3, P=5, L=140, T0=200.0,
                                                        alpha=.85)

            end = time.time()
            print("End of Simulated Annealing")

            #  print best solution found
            print("obtaining propagation matrix of the best solution...")
            matrix_solution, _, _ = self.simulates_propagation(best)
            best_fo = round(self.objective_function(matrix_solution), 2)

            print("generating visualization of the solution...")
            extra_bs = []

            extra_bs.append(initial_solution)

            for fo in FOs:
                bs = BaseStation()
                bs.latitude = fo["lat"]
                bs.longitude = fo["lng"]
                bs.potencia_transmissao = fo["power"]
                bs.altura = fo["height"]
                bs.color = 'gray'

                extra_bs.append(bs)

            best.color = 'red'
            self.print_simulation_result(best, extra_bs)

            print("len(FOs)=", len(FOs))

            print('(propagation_model)=', propagation_model)

            print("(initial.latitude, initial.longitude)=",
                  (round(initial_solution.latitude, 6), round(initial_solution.longitude, 6)))
            print("(initial.altura)=", initial_solution.altura)
            print("(initial.potencia_transmissao)=", initial_solution.potencia_transmissao)
            print('(initial.fo)=', round(initial_fo, 2))
            print()
            print("(best.latitude, best.longitude)=", (round(best.latitude, 6), round(best.longitude, 6)))
            print("(best.altura)=", best.altura)
            print("(best.potencia_transmissao)=", best.potencia_transmissao)
            print('(best.fo)=', best_fo)
            print()
            distance_of_solutions = calculates_distance_between_coordinates(
                (initial_solution.latitude, initial_solution.longitude), (best.latitude, best.longitude))
            print("Distance of solutions=", round(distance_of_solutions, 2))

            # Plot the objective function line chart
            print("generating graph of the behavior of the objective function...")
            FOs_to_plot = [item['of'] for item in FOs]
            print("FOs_to_plot=", FOs_to_plot)
            plt.plot(FOs_to_plot)
            plt.title("Comportamento do Simulated Annealing (" + str(propagation_model) + ")")
            plt.ylabel('Valor da FO')
            plt.xlabel('Solução candidata')
            plt.show()

            if save_simulations and not run_only_test:
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
                    "distance_of_solutions": str(distance_of_solutions),
                    "best_latitude": str(best.latitude),
                    "best_longitude": str(best.longitude),
                    "best_height": str(best.altura),
                    "best_power_transmission": str(best.potencia_transmissao),
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
        # self.label_geral_info_1.setText("Simulação executada em %s segundos" % round(end - start, 2))
        self.label_geral_info_1.setText("Simulação realizada com sucesso!")
        print("Simulation run in %s seconds" % round(end - start, 2))

        print("End of simulation!")

    def evaluate_solution(self, point: BaseStation) -> float:
        matrix_solution, _, _ = self.simulates_propagation(point)

        return self.objective_function(matrix_solution)

    @staticmethod
    def disturb_solution(solution: BaseStation, disturbance_radius: float = 460) -> BaseStation:
        """
        Disturb a specific solution
        :param solution: A base station solution
        :param disturbance_radius: The ray of disturbance in meters
        :return: Return the base station with a new position (lat long)
        """
        latitude = solution.latitude
        longitude = solution.longitude

        new_coordinates = get_coordinate_in_circle(latitude, longitude, disturbance_radius)

        solution.latitude = new_coordinates[0]
        solution.longitude = new_coordinates[1]

        return solution

    def generates_heights(self, height: float) -> list:
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

    def simulated_annealing(self, base_station: BaseStation, M: int, P: int, L: int, T0: float, alpha: float) \
            -> Tuple[Union[BaseStation, Any], float, List[Dict[str, float]]]:
        """
        :param base_station: Dados do problema principal
        :param M: Número máximo de iterações.
        :param P: Número máximo de Perturbações por iteração.
        :param L: Número máximo de sucessos por iteração.
        :param T0: Temperatura inicial.
        :param alpha: Factor de redução da temperatura.
        :return: Retorna um ponto (tupla de coordenadas) sendo a mais indicada.
        """

        # List of solutions found
        FOs = []

        # Initial solution
        s = base_station

        antenna_height = float(base_station.altura)
        possible_heights = self.generates_heights(antenna_height)
        print("possible_heights=", str(possible_heights))

        antenna_power_received = float(base_station.potencia_transmissao)
        possible_powers_received = self.generates_received_powers(antenna_power_received)
        print("possible_powers_received=", str(possible_powers_received))

        s0 = s
        print("Solução inicial: " + str((s0.latitude, s0.longitude)))

        result_fo = self.evaluate_solution(s)

        f_s = result_fo

        T = T0
        j = 1

        # Store the BEST solution found
        best_fs = f_s
        best_erb = s0

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

                # Get a different position to ERB
                Si = self.disturb_solution(s)

                # For all possible antenna heights
                for height in possible_heights:
                    print("-----------------------")
                    print("antenna height=", height)
                    Si.altura = height

                    for power in possible_powers_received:
                        print("transmission power=", power)
                        Si.potencia_transmissao = power

                        # Get objective function value
                        result_fo = self.evaluate_solution(Si)

                        f_si = result_fo

                        # Verificar se o retorno da função objetivo está correto. f(x) é a função objetivo
                        delta_fi = f_si - f_s

                        # Minimização: delta_fi >= 0
                        # Maximização: delta_fi <= 0
                        # Teste de aceitação de uma nova solução
                        if (delta_fi <= 0) or (exp(-delta_fi / T) > random.random()):

                            s = copy.deepcopy(Si)
                            f_s = f_si

                            n_success = n_success + 1

                            if f_s > best_fs:
                                best_fs = f_s
                                best_erb = copy.deepcopy(Si)

                            FOs.append({
                                "lat": Si.latitude,
                                "lng": Si.longitude,
                                "height": Si.altura,
                                "power": Si.potencia_transmissao,
                                "of": f_s
                            })

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

        FOs.append({
            "lat": best_erb.latitude,
            "lng": best_erb.longitude,
            "height": best_erb.altura,
            "power": best_erb.potencia_transmissao,
            "of": best_fs
        })

        return best_erb, best_fs, FOs
