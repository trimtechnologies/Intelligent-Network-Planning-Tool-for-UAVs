from PyQt5 import QtCore
from fbs_runtime.application_context.PyQt5 import ApplicationContext

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

context = ApplicationContext()
