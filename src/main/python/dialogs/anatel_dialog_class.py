
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QProgressBar, QTableWidgetItem, QTableWidget, QLabel, QComboBox, QMessageBox
from pandas import DataFrame
from datetime import datetime

from models.base_station import BaseStation
from controllers.base_station_controller import BaseStationController
from controllers.settings_controller import SettingsController
from support.anatel import get_anatel_data, get_ufs_initials, get_uf_by_id, get_counties, get_uf_code, dms_to_dd
from support.constants import CURRENT_COUNTY_ID, CURRENT_UF_ID, LAST_DATABASE_UPDATE, INVALID_UF
from dialogs.alert_dialog_class import AlertDialogClass

from base import context
from support.core import convert_to_float


class AnatelDialogClass(QDialog):
    """
    This class load the Anatel dialog pyqt component
    """

    def __init__(self, parent=None):
        """
        Anatel dialog class constructor
        :param parent:
        """
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi(context.get_resource("anatel_dialog.ui"), self)

        self.__settings_controller = SettingsController()
        self.__base_station_controller = BaseStationController()

        self.init_ui_components()

    def get_current_uf_id(self):
        data = {
            'option': CURRENT_UF_ID,
        }
        res = self.__settings_controller.get(data)
        if res is not None:
            return res.value
        else:
            return -1

    def get_current_state_id(self):
        data = {
            'option': CURRENT_COUNTY_ID,
        }
        res = self.__settings_controller.get(data)
        if res is not None:
            return res.value
        else:
            return -1

    def get_last_update_date(self):
        data = {
            'option': LAST_DATABASE_UPDATE,
        }
        res = self.__settings_controller.get(data)
        if res is not None:
            return res.value
        else:
            return None

    def init_ui_components(self):
        current_uf_id = self.get_current_uf_id()
        current_county_id = self.get_current_state_id()
        print(current_uf_id)
        print(current_county_id)

        self.fill_combo_box_state()

        current_index_uf = self.get_current_state_index(current_uf_id)
        self.combo_box_state.setCurrentIndex(current_index_uf)

        if current_index_uf != -1:
            self.fill_combo_box_country(self.combo_box_state.itemText(current_index_uf))
        else:
            self.combo_box_county.addItems(["Select a UF first"])

        current_country_uf = self.get_current_county_index(current_county_id)
        self.combo_box_county.setCurrentIndex(current_country_uf)

        self.fill_erb_table_with_database_info()

        self.combo_box_state.currentIndexChanged.connect(self.on_combo_box_state_changed)
        self.combo_box_county.currentIndexChanged.connect(self.on_combo_box_county_changed)

        self.update_database_button.clicked.disconnect()
        self.update_database_button.clicked.connect(self.on_update_database_button_clicked)

        # Label info - last update
        last_update_date = self.get_last_update_date()
        print(last_update_date)

        if last_update_date is None:
            label_last_update = "The database has not yet been updated."
        else:
            date = str(datetime.strptime(last_update_date[:-7], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y às %H:%M:%S"))
            label_last_update = "Database updated in " + date

        self.label_last_update: QLabel
        self.label_last_update.setText(label_last_update)

    def get_current_state_index(self, current_uf_id):
        self.combo_box_state: QComboBox
        if current_uf_id != -1:
            for count in range(self.combo_box_state.count()):
                if str(self.combo_box_state.itemData(count)) == current_uf_id:
                    return count
        return 0

    def get_current_county_index(self, current_county_id):
        self.combo_box_county: QComboBox
        if current_county_id != -1:
            for count in range(self.combo_box_county.count()):
                if str(self.combo_box_county.itemData(count)) == current_county_id:
                    return count
        return 0

    @pyqtSlot(name="on_combo_box_state_changed")
    def on_combo_box_state_changed(self):
        self.combo_box_county.clear()

        index = self.combo_box_state.currentIndex()

        if index != 0 and index != -1 and index is not None:
            uf_id = self.combo_box_state.itemData(index)
            self.__create_or_update_uf(uf_id)
            uf_initial = get_uf_by_id(uf_id)
            self.fill_combo_box_country(uf_initial)

    def fill_combo_box_country(self, uf):
        """
        This method fill the combo box country county according to uf
        :param uf:
        :return:
        """
        self.combo_box_county: QComboBox

        counties = get_counties(uf)

        if counties != INVALID_UF:
            for county in counties:
                self.combo_box_county.addItem(county[0], county[1])

        self.combo_box_county.setCurrentIndex(0)

    def __create_or_update_last_updated_date(self):
        data = {
            'option': LAST_DATABASE_UPDATE,
            'value': datetime.now()
        }

        # The setting no exists, then store
        if not self.__settings_controller.get(data):
            result = self.__settings_controller.store(data)
            print('Result from store last updated date: ' + str(result))
        else:
            # The setting exists, then update
            result = self.__settings_controller.update(data, None)
            print('Result from update last updated date: ' + str(result))

    def __create_or_update_uf(self, uf_id):
        data = {
            'option': CURRENT_UF_ID,
            'value': uf_id
        }

        # The setting no exists, then store
        if not self.__settings_controller.get(data):
            result = self.__settings_controller.store(data)
            print('Result from store uf id: ' + str(result))
        else:
            # The setting exists, then update
            result = self.__settings_controller.update(data, None)
            print('Result from update uf id: ' + str(result))

    def __create_or_update_state(self, state_id):
        data = {
            'option': CURRENT_COUNTY_ID,
            'value': state_id
        }

        # The setting no exists, then store
        if not self.__settings_controller.get(data):
            result = self.__settings_controller.store(data)
            print('Result from store state id: ' + str(result))

            if result is not None:
                AlertDialogClass("update base",
                                 "Region settings successfully updated! Remember to update the base of "
                                 "ERBs.").exec_()
        else:
            # The setting exists, then update
            result = self.__settings_controller.update(data, None)
            print('Result from update state id: ' + str(result))

    @pyqtSlot(name="on_combo_box_county_changed")
    def on_combo_box_county_changed(self):
        index = self.combo_box_county.currentIndex()
        # text = self.combo_box_county.currentText()

        uf_id = self.combo_box_county.itemData(index)
        self.__create_or_update_state(uf_id)

    def disable_ui_components(self):
        self.anatel_table.setDisabled(True)
        self.update_database_button.setDisabled(True)
        self.combo_box_state.setDisabled(True)
        self.combo_box_county.setDisabled(True)

    def enable_ui_components(self):
        self.anatel_table.setDisabled(False)
        self.update_database_button.setDisabled(False)
        self.combo_box_state.setDisabled(False)
        self.combo_box_county.setDisabled(False)

    def fill_combo_box_state(self):
        """
        This method fill the combo box country state according with all ufs
        :return:
        """
        self.combo_box_state: QComboBox
        ufs = get_ufs_initials()

        for uf in ufs:
            self.combo_box_state.addItem(uf, get_uf_code(uf))

    def fill_erb_table_with_database_info(self):
        # delete all register from table
        self.anatel_table.setRowCount(0)

        self.anatel_table: QTableWidget

        self.anatel_table.removeRow(0)
        row_position = self.anatel_table.rowCount()

        db_configs = self.__base_station_controller.get_all()

        total = len(db_configs)
        processed = 0

        for i, config in enumerate(db_configs):
            config: BaseStation

            table_row_count = row_position + i
            self.anatel_table.insertRow(table_row_count)

            self.anatel_table.setItem(table_row_count, 0, QTableWidgetItem(str(config.id)))
            self.anatel_table.setItem(table_row_count, 1, QTableWidgetItem(str(config.status)))
            self.anatel_table.setItem(table_row_count, 2, QTableWidgetItem(str(config.entity)))
            self.anatel_table.setItem(table_row_count, 3, QTableWidgetItem(str(config.fistel_number)))
            self.anatel_table.setItem(table_row_count, 4, QTableWidgetItem(str(config.service_number)))
            self.anatel_table.setItem(table_row_count, 5, QTableWidgetItem(str(config.radio_frequency_authorization_number)))
            self.anatel_table.setItem(table_row_count, 6, QTableWidgetItem(str(config.station_number)))
            self.anatel_table.setItem(table_row_count, 7, QTableWidgetItem(str(config.address)))
            self.anatel_table.setItem(table_row_count, 8, QTableWidgetItem(str(config.uf)))
            self.anatel_table.setItem(table_row_count, 9, QTableWidgetItem(str(config.county)))
            self.anatel_table.setItem(table_row_count, 10, QTableWidgetItem(str(config.registration)))
            self.anatel_table.setItem(table_row_count, 11, QTableWidgetItem(str(config.technology)))
            self.anatel_table.setItem(table_row_count, 12, QTableWidgetItem(str(config.access_resource)))
            self.anatel_table.setItem(table_row_count, 13, QTableWidgetItem(str(config.initial_frequency)))
            self.anatel_table.setItem(table_row_count, 14, QTableWidgetItem(str(config.final_frequency)))
            self.anatel_table.setItem(table_row_count, 15, QTableWidgetItem(str(config.azimute)))
            self.anatel_table.setItem(table_row_count, 16, QTableWidgetItem(str(config.station_type)))
            self.anatel_table.setItem(table_row_count, 17, QTableWidgetItem(str(config.physical_infrastructure_classification)))
            self.anatel_table.setItem(table_row_count, 18, QTableWidgetItem(str(config.physical_infrastructure_sharing)))
            self.anatel_table.setItem(table_row_count, 19, QTableWidgetItem(str(config.antenna_type)))
            self.anatel_table.setItem(table_row_count, 20, QTableWidgetItem(str(config.antenna_approval)))
            self.anatel_table.setItem(table_row_count, 21, QTableWidgetItem(str(config.antenna_gain)))
            self.anatel_table.setItem(table_row_count, 22, QTableWidgetItem(str(config.gain_front_coast)))
            self.anatel_table.setItem(table_row_count, 23, QTableWidgetItem(str(config.half_power_angle)))
            self.anatel_table.setItem(table_row_count, 24, QTableWidgetItem(str(config.elevation_degree)))
            self.anatel_table.setItem(table_row_count, 25, QTableWidgetItem(str(config.polarization)))
            self.anatel_table.setItem(table_row_count, 26, QTableWidgetItem(str(config.height)))
            self.anatel_table.setItem(table_row_count, 27, QTableWidgetItem(str(config.transmission_approval)))
            self.anatel_table.setItem(table_row_count, 28, QTableWidgetItem(str(config.transmit_power)))
            self.anatel_table.setItem(table_row_count, 29, QTableWidgetItem(str(config.latitude)))
            self.anatel_table.setItem(table_row_count, 30, QTableWidgetItem(str(config.longitude)))
            self.anatel_table.setItem(table_row_count, 31, QTableWidgetItem(str(config.latitude_dms)))
            self.anatel_table.setItem(table_row_count, 32, QTableWidgetItem(str(config.longitude_dms)))
            self.anatel_table.setItem(table_row_count, 33, QTableWidgetItem(str(config.debit_code_tfi)))
            self.anatel_table.setItem(table_row_count, 34, QTableWidgetItem(str(config.date_of_first_licensing)))
            self.anatel_table.setItem(table_row_count, 35, QTableWidgetItem(str(config.created_at)))

            processed = processed + 1
            self.progress_bar_anatel.setValue(round(((processed / total) * 100), 2))

        self.anatel_table.setDisabled(False)
        self.update_database_button.setDisabled(False)

    def save_offline_erb_data(self, erb_config: DataFrame):
        self.__base_station_controller.destroy_all()

        total = len(erb_config.values)
        processed = 0

        for row in erb_config.values:
            data = {
                "status": row[0],
                "entity": row[1],
                "fistel_number": row[2],
                "service_number": row[3],
                "radio_frequency_authorization_number": row[4],
                "station_number": row[5],
                "address": row[6],
                "address_complement": row[7],
                "uf": row[8],
                "county": row[9],
                "registration": row[10],
                "technology": row[11],
                "technology_type": row[12],
                "access_resource": row[13],
                "initial_frequency": convert_to_float(row[14]),
                "final_frequency": convert_to_float(row[15]),
                "azimute": row[16],
                "station_type": row[17],
                "physical_infrastructure_classification": row[18],
                "physical_infrastructure_sharing": row[19],
                "antenna_type": row[20],
                "antenna_approval": row[21],
                "antenna_gain": convert_to_float(row[22]),
                "gain_front_coast": row[23],
                "half_power_angle": row[24],
                "elevation_degree": row[25],
                "polarization": row[26],
                "height": convert_to_float(row[27]),
                "transmission_approval": row[28],
                "transmit_power": convert_to_float(row[29]),
                "latitude": dms_to_dd(row[30]),
                "longitude": dms_to_dd(row[31]),
                "latitude_dms": row[30],
                "longitude_dms": row[31],
                "debit_code_tfi": row[32],
                "date_of_licensing": row[33],
                "date_of_first_licensing": row[34],
                "network_number": row[35],
                "item_id": row[36],
                "date_validation": row[37],
                "fistel_number_assoc": row[38],
                "associate_entity_name": row[39],
            }
            self.__base_station_controller.store(data)

            processed = processed + 1
            self.progress_bar_anatel.setValue(round(((processed / total) * 100), 2))

    @pyqtSlot(name="on_update_database_button_clicked")
    def on_update_database_button_clicked(self):
        """
        This method add Anatel antenna info rows in the table
        :return:
        """
        self.label_last_update: QLabel
        self.progress_bar_anatel: QProgressBar

        self.label_last_update.setText("Searching for information in the online database...")

        self.combo_box_state: QComboBox
        uf_sigle = self.combo_box_state.itemText(self.combo_box_state.currentIndex())
        country_code = self.combo_box_county.itemData(int(self.combo_box_county.currentIndex()))

        erb_config = get_anatel_data(uf_sigle, int(country_code))

        self.label_last_update.setText("Saving information offline")

        self.save_offline_erb_data(erb_config)
        self.fill_erb_table_with_database_info()

        self.label_last_update.setText("Updated local database!")

        self.__create_or_update_last_updated_date()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'If a database update was performed, remember to restart '
                                                           'the application so that the Base Station information is '
                                                           'loaded again.',
                                     QMessageBox.Ok, QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            event.accept()
            print('Window closed')
        else:
            event.ignore()
