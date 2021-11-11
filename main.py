import sys
sys.path.insert(1, '/usr/intel/pkgs/python3/3.7.4/modules/r1/lib/python3.7/site-packages/')
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
import Global
import subprocess
import os
import argparse


def main():
    workarea = os.getenv("WORKAREA").split("/")[-1]
    window_id = subprocess.run(['/usr/intel/bin/xdotool', 'search', '--name', f'Side Menu.*{workarea}'],
                               stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    if window_id != "":
        os.system(f'/usr/intel/bin/xdotool windowactivate {window_id}')
    else:
        parser = argparse.ArgumentParser(description='Dashboard of buttons for encapsulating command as action button.')
        parser.add_argument('-dir', help='Directory where the extra files are located ( defaultF10 & TabFiles ).',
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
