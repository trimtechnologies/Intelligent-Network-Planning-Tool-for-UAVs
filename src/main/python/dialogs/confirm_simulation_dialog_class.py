import datetime

from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLabel

from base import context


class ConfirmSimulationDialogClass(QDialog):
    """
    This class load the help dialog pyqt component
    """

    def __init__(self, data: dict, parent=None):
        """
        Confirm Simulation dialog class constructor
        :param parent:
        """
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi(context.get_resource("confirm_simulation_dialog.ui"), self)

        self.val = None
        simulation = data['simulation']
        print('propagation_model=', simulation['propagation_model'])
        print('environment=', simulation['environment'])
        print('max_ray=', simulation['max_ray'])

        transmitter = data['transmitter']
        print('entity=', transmitter['entity'])
        print('uf_municipal=', transmitter['uf_municipal'])
        print('address=', transmitter['address'])
        print('frequency=', transmitter['frequency'])
        print('gain=', transmitter['gain'])
        print('transmission_power=', transmitter['transmission_power'])
        print('elevation=', transmitter['elevation'])
        print('polarization=', transmitter['polarization'])
        print('height=', transmitter['height'])
        print('latitude=', transmitter['latitude'])
        print('longitude=', transmitter['longitude'])

        receptor = data['receptor']
        print('height=', receptor['height'])
        print('gain=', receptor['gain'])
        print('sensitivity=', receptor['sensitivity'])

        heuristic = data['heuristic']
        print('initial_solution=', heuristic['initial_solution'])
        print('initial_temperature=', heuristic['initial_temperature'])
        print('maximum_number_of_iterations=', heuristic['maximum_number_of_iterations'])
        print('maximum_number_of_disturbances_per_iteration=', heuristic['maximum_number_of_disturbances_per_iteration'])
        print('maximum_number_of_successes_per_iteration=', heuristic['maximum_number_of_successes_per_iteration'])
        print('alpha=', heuristic['alpha'])
        print('optimize_solution=', heuristic['optimize_solution'])
        print('optimize_height=', heuristic['optimize_height'])
        print('optimize_power=', heuristic['optimize_power'])
        print('save_simulations=', heuristic['save_simulations'])
        print('number_of_simulations=', heuristic['number_of_simulations'])
        print('number_of_erb_solutions=', heuristic['number_of_erb_solutions'])

        heuristic['optimize_solution'] = "Sim" if heuristic['optimize_solution'] else "Não"
        heuristic['optimize_height'] = "Sim" if heuristic['optimize_height'] else "Não"
        heuristic['optimize_power'] = "Sim" if heuristic['optimize_power'] else "Não"
        heuristic['save_simulations'] = "Sim" if heuristic['save_simulations'] else "Não"

        drone = data['drone']  # ToDo: add in layout
        print('transmit_power=', drone['transmit_power'])
        print('frequency=', drone['frequency'])
        print('height=', drone['height'])

        # Simulation details
        self.label_modelo_propagacao_value: QLabel
        self.label_ambiente_value: QLabel
        self.label_radio_maximo_value: QLabel

        # Transmissor
        self.label_entidade_value: QLabel
        self.label_uf_municipio_value: QLabel
        self.label_endereco_value: QLabel
        self.label_frequencia_value: QLabel
        self.label_ganho_value: QLabel
        self.label_potencia_transmissao_value: QLabel
        self.label_elevacao_value: QLabel
        self.label_polarizacao_value: QLabel
        self.label_altura_value: QLabel
        self.label_latitude_value: QLabel
        self.label_longitude_value: QLabel

        # Meta-heuristic
        self.label_solucao_inicial_value: QLabel
        self.label_temperatura_inicial_value: QLabel
        self.label_num_maximo_iteracoes_value: QLabel
        self.label_num_maximo_pertubacoes_iteracao_value: QLabel
        self.label_num_maximo_sucessos_iteracao_value: QLabel
        self.label_alpha_value: QLabel

        # Receptor details
        self.label_bs_altura_value: QLabel
        self.label_bs_ganho_value: QLabel
        self.label_bs_sensibilidade_value: QLabel

        # Add values ins labels
        self.label_modelo_propagacao_value.setText(simulation['propagation_model'])
        self.label_ambiente_value.setText(simulation['environment'])
        self.label_radio_maximo_value.setText(simulation['max_ray'])
        self.label_entidade_value.setText(transmitter['entidade'])
        self.label_uf_municipio_value.setText(transmitter['uf_municipio'])
        self.label_endereco_value.setText(transmitter['endereco'])
        self.label_frequencia_value.setText(transmitter['frequencia'])
        self.label_ganho_value.setText(transmitter['ganho'])
        self.label_potencia_transmissao_value.setText(transmitter['potencia_transmissao'])
        self.label_elevacao_value.setText(transmitter['elevacao'])
        self.label_polarizacao_value.setText(transmitter['polarizacao'])
        self.label_altura_value.setText(transmitter['altura'])
        self.label_latitude_value.setText(transmitter['latitude'])
        self.label_longitude_value.setText(transmitter['longitude'])
        self.label_bs_altura_value.setText(receptor['altura'])
        self.label_bs_ganho_value.setText(receptor['ganho'])
        self.label_bs_sensibilidade_value.setText(receptor['sensibilidade'])
        self.label_solucao_inicial_value.setText(heuristic['solucao_inicial'])
        self.label_temperatura_inicial_value.setText(heuristic['temperatura_inicial'])
        self.label_num_maximo_iteracoes_value.setText(heuristic['numero_maximo_iteracoes'])
        self.label_num_maximo_pertubacoes_iteracao_value.setText(heuristic['numero_maximo_pertubacoes_por_iteracao'])
        self.label_num_maximo_sucessos_iteracao_value.setText(heuristic['numero_maximo_sucessos_por_iteracao'])
        self.label_alpha_value.setText(heuristic['alpha'])
        self.label_optimize_solution_value.setText(heuristic['optimize_solution'])
        self.label_optimize_height_value.setText(heuristic['optimize_height'])
        self.label_optimize_power_value.setText(heuristic['optimize_power'])
        self.label_save_simulation_value.setText(heuristic['save_simulations'])
        self.label_number_of_simulations_value.setText(heuristic['number_of_simulations'])
        self.label_number_of_erbs_value.setText(heuristic['number_of_erb_solutions'])

        # Confirm button
        self.btn_confirmar_simulacao.clicked.disconnect()
        self.btn_confirmar_simulacao.clicked.connect(self.on_btn_confirmar_simulacao_clicked)

        # Cancel button
        self.btn_cancelar_simulacao.clicked.disconnect()
        self.btn_cancelar_simulacao.clicked.connect(self.on_btn_cancelar_simulacao_clicked)

    def fill_data(self, data):
        pass
        # label_modelo_propagacao_value
        # label_ambiente_value
        # label_radio_maximo_value

        # label_entidade_value
        # label_uf_municipio_value
        # label_endereco_value
        # label_frequencia_value
        # label_ganho_value
        # label_elevacao_value
        # label_polarizacao_value
        # label_altura_value
        # label_latitude_value
        # label_longitude_value

        # label_bs_altura_value
        # label_bs_ganho_value
        # label_bs_sensibilidade_value

    @pyqtSlot(name="on_btn_confirmar_simulacao_clicked")
    def on_btn_confirmar_simulacao_clicked(self):
        """
        This method is called when confirm simulation button is clicked
        :return: None
        """
        print("Confirmation button!")
        self.val = 6666
        self.accept()

    @pyqtSlot(name="on_btn_cancelar_simulacao_clicked")
    def on_btn_cancelar_simulacao_clicked(self):
        """
        This method is called when cancel simulation button is clicked
        :return: None
        """
        print("Cancel button!")
        self.val = -123
        self.reject()
