

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class AlertDialogClass(QDialog):
    """
    This class load the help dialog pyqt component
    """

    def __init__(self, title, message, parent=None):
        """
        Confirm dialog class constructor
        :param parent:
        """
        QDialog.__init__(self, parent)

        self.setWindowTitle(title)

        print(title)
        print(message)

        q_btn = QDialogButtonBox.Ok  # | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(message)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
