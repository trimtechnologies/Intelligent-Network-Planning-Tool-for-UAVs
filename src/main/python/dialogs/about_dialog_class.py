

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from base import context


class AboutDialogClass(QDialog):
    """
    This class load the about dialog pyqt component
    """
    def __init__(self, parent=None):
        """
        About dialog class constructor
        :param parent:
        """
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi(context.get_resource("about_dialog.ui"), self)
