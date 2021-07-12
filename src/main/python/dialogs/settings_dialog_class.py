
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox

from controllers.settings_controller import SettingsController
from controllers.base_station_controller import BaseStationController
from support.constants import CURRENT_UF_ID, INVALID_UF
from support.anatel import get_ufs_initials, get_counties, get_uf_code, get_uf_by_id
from support.constants import CURRENT_COUNTY_ID
from dialogs.alert_dialog_class import AlertDialogClass

from base import context


class SettingsDialogClass(QDialog):
    """
    This class load the settings dialog pyqt component
    """

    def __init__(self, parent=None):
        """
        Settings dialog class constructor
        :param parent:
        """
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi(context.get_resource("settings_dialog.ui"), self)

        self.__settings_controller = SettingsController()
        self.__base_station_controller = BaseStationController()

        self.fill_combo_box_state()

        current_uf_id = self.get_current_uf_id()
        current_county_id = self.get_current_state_id()

        current_index_uf = self.get_current_state_index(current_uf_id)
        self.combo_box_state.setCurrentIndex(current_index_uf)

        if current_index_uf != -1:
            self.fill_combo_box_country(self.combo_box_state.itemText(current_index_uf))
        else:
            self.combo_box_county.addItems(["Select a UF first"])

        current_country_uf = self.get_current_county_index(current_county_id)
        self.combo_box_county.setCurrentIndex(current_country_uf)

        self.combo_box_state.currentIndexChanged.connect(self.on_combo_box_state_changed)
        self.combo_box_county.currentIndexChanged.connect(self.on_combo_box_county_changed)

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

    def on_combo_box_state_changed(self, index):
        """
        This method is fired when combo box country state is changed
        :param int index: Index of state in combo_box_state component
        :return: None
        """
        self.combo_box_county.clear()

        if index != 0:
            uf_id = self.combo_box_state.itemData(index)
            self.__create_or_update_uf(uf_id)
            uf_initial = get_uf_by_id(uf_id)
            self.fill_combo_box_county(uf_initial)

    def __create_or_update_uf(self, uf_id):
        data = {
            'option': CURRENT_UF_ID,
            'value': uf_id
        }

        # The setting no exists, then store
        if not self.__settings_controller.get(data):
            result = self.__settings_controller.store(data)
            print('Result from store: ' + str(result))
        else:
            # The setting exists, then update
            result = self.__settings_controller.update(data, None)
            print('Result from update: ' + str(result))

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
                AlertDialogClass("Atualizar base",
                                 "Configurações de região atualizadas com sucesso! Lembre-se de atualizar a base de "
                                 "ERBs.").exec_()
        else:
            # The setting exists, then update
            result = self.__settings_controller.update(data, None)
            print('Result from update state id: ' + str(result))

    def on_combo_box_county_changed(self, index):
        """
        This method is fired when combo box county state is changed
        :param int index: Index of county in combo_box_county component
        :return: None
        """
        county_id = self.combo_box_county.itemData(index)
        self.__create_or_update_state(county_id)

    def fill_combo_box_county(self, uf):
        """
        This method fill the combo box country county according to uf
        :param uf:
        :return:
        """
        self.combo_box_county: QComboBox
        counties = get_counties(uf)
        for county in counties:
            self.combo_box_county.addItem(county[0], county[1])

    def fill_combo_box_state(self):
        """
        This method fill the combo box country state according with all ufs
        :return:
        """
        self.combo_box_state: QComboBox
        ufs = get_ufs_initials()
        self.combo_box_state.addItem("Select", -1)

        for uf in ufs:
            self.combo_box_state.addItem(uf, get_uf_code(uf))

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
