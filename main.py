import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
import Global
import subprocess
import os
import argparse


def main():

    parser = argparse.ArgumentParser(description='Dashboard of buttons for encapsulating command as action button.')
    parser.add_argument('-dir', help='Directory where the extra files are located.',
                        dest='directory', type=str, required=True)
    args = parser.parse_args()
    current_exit_code = Global.REBOOT_CODE
    while current_exit_code == Global.REBOOT_CODE:
        Global.init_shared_globals(args.directory)
        app = QApplication(sys.argv)
        Global.screen_height = QApplication.desktop().screenGeometry().height()
        main_window = MainWindow()
        main_window.show()
        current_exit_code = app.exec()
        app = None


if __name__ == "__main__":
    main()
