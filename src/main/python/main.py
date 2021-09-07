#!/usr/bin/env python

import sys

from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property


from support.database import create_tables
from windows.main_window import MainWindow


class AppContext(ApplicationContext):
    def run(self):
        self.window.show()
        return self.app.exec_()

    def get_design(self):
        return self.get_resource("main_window.ui")

    @cached_property
    def window(self):
        return MainWindow(self.get_design())


def main_window():
    """
    This method load main window and load application context
    :return: None
    """
    app_ctx = AppContext()
    exit_code = app_ctx.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    """
    Main method, the application start in this code point.
    This method creates all database tables and open main window
    """
    create_tables()
    main_window()
