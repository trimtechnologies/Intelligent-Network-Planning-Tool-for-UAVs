

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from base import context


class HelpDialogClass(QDialog):
    """
    This class load the help dialog pyqt component
    """
    def __init__(self, parent=None):
        """
        Help dialog class constructor
        :param parent:
        """
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi(context.get_resource("help_dialog.ui"), self)
