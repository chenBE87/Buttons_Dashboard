import os
import sys

from PyQt5.QtWidgets import QMainWindow, QAction, QScrollArea, QTabWidget, QLineEdit, QDialog, \
    QInputDialog, QMessageBox, QShortcut
from MainFrame import MainFrame
from PyQt5.QtGui import QPalette, QMouseEvent, QKeySequence
from PyQt5.QtCore import QCoreApplication, Qt
from CadenceButton import CadenceButton
from SingleOptionChooseDialog import ChooseSection, ChooseTabType, RemoveTabType

import Global
import _pickle as pickle


class MainWindow(QMainWindow):
    """
    MainWindow
   ---------------
    Application's main window
    """

    """
    Function - __init__ ( Constructor )

    Brief - init main window display and functionality.

    Parameters - 
                    parent   : Qwidget - button's responsible widget ( default = None ).

    Description - 
                    1. Initiate class variables.
                    2. Create Initiate UI.
                    3. Display window.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_frame = None
        self.tabs = None
        self.bold_buttons = None
        self.tab_scrolls = []
        self.frames = []
        self.frames_scroll_areas = []
        self.msg = QMessageBox()
        self.init_ui()
        self.shortcut_open = QShortcut(QKeySequence('Alt+O'), self)
        self.shortcut_open.activated.connect(lambda: self.toggle_current_tab_sections(True))
        self.shortcut_open = QShortcut(QKeySequence('Alt+C'), self)
        self.shortcut_open.activated.connect(lambda: self.toggle_current_tab_sections(False))

    """
    Function - init_ui

    Brief - Initiating windows user interface ( UI ).

    Description - 
                    1. Create menu bar.
                    2. Create tab menu.
                    3. Set window's style ( GUI representation ).
    """

    def init_ui(self):
        # Create menu bar.
        self.set_menu_bar()

        # Create tab menu.
        self.tabs = QTabWidget()
        self.add_tab()
        self.add_tab("User")
        sys.path.insert(0, Global.path_to_additional_files)
        from TabTypes import tab_types_extra_info
        for title in tab_types_extra_info.keys():
            btn_set = self.create_btn_set(title)
            self.add_tab(title, btn_set)
        #self.load_custom_tabs()
        self.tabs.tabBarClicked[int].connect(self.resize_tab_window)

        if Global.bold_all_btns:
            self.bold_buttons.setChecked(True)
            self.bold_all_btns(to_save=False)
        else:
            self.bold_buttons.setChecked(False)

        self.setCentralWidget(self.tabs)

        # Set window's style ( GUI representation ).
        self.tabs.setBackgroundRole(QPalette.Base)
        workarea = os.getenv("WORKAREA").split("/")[-1]
        self.setWindowTitle(f'Side Menu 1.6 - Workarea: {workarea}')
        self.setFixedSize((Global.btn_size + 15) * Global.number_of_btn_in_row, self.height())
        self.tabs.widget(0).widget().resize_window_height()

    def set_menu_bar(self):
        """
        Set window's menu bar
        """
        action_menu = self.menuBar().addMenu('Actions')
        settings_menu = self.menuBar().addMenu('Settings')
        help_menu = self.menuBar().addMenu('Help')
        exit_action = QAction('Exit', self, triggered=self.close)
        #add_tab = QAction('Add new tab', self, triggered=self.add_new_tab)
        #remove_tab = QAction('Remove tab', self, triggered=self.remove_tab)
        add_section = QAction('Add New Section to User tab', self, triggered=self.add_section)
        coll_section = QAction('Open Sections', self, triggered=lambda: self.toggle_current_tab_sections(True))
        decoll_section = QAction('Close Sections', self, triggered=lambda: self.toggle_current_tab_sections(False))
        change_btn_num = QAction('Change Buttons Number in a Row', self, triggered=self.change_num_of_btns)
        self.bold_buttons = QAction('Bold All Buttons', self, triggered=lambda: self.bold_all_btns(), checkable=True)
        change_btn_size = QAction('Change Buttons Size', self, triggered=self.change_btns_size)
        action_menu.addAction(add_section)
        #tab_actions = action_menu.addMenu('Custom Tabs')
        #tab_actions.addActions([add_tab, remove_tab])
        coll_decoll_menu = action_menu.addMenu('Open/Close Sections')
        coll_decoll_menu.addActions([coll_section, decoll_section])
        action_menu.addAction(exit_action)
        settings_menu.addActions([change_btn_num,change_btn_size, self.bold_buttons])
        help_menu.addAction(QAction('Go to Wiki page', self, triggered=self.help_page))

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                             Window's GUI                                 #
    #                                                                          #
    ############################################################################
    """
    Function - resize_tab_window

    Brief - Resize tab window.
    
    Parameters  -
                    index: int - tab index to resize. 

    """

    def resize_tab_window(self, index):
        self.tabs.widget(index).widget().resize_window_height()
        self.tabs.setCurrentIndex(index)

    """
    Function - toggle_current_tab_sections

    Brief - Open/Close all section in the current tab ( except the first tab in the "Default" section ).

    Parameters  -
                    to_open: bool - True to open all section. False to close. 

    """
    def toggle_current_tab_sections(self, to_open):
        sections = self.tabs.currentWidget().widget().sections
        for idx in range(0, sections.count()):
            section = sections.itemAt(idx).widget()
            if section.get_section_title() != " ":
                if to_open and section.checked:
                    section.collapse()
                elif not to_open and not section.checked:
                    section.decollapse()

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                             Menu Bar Actions                             #
    #                                                                          #
    ############################################################################
    """
    Function - add_section

    Brief - Add section to "User" tab.

    Description - 
                    1. Open input text window to enter new section name
                    2. Only when Ok button pressed, and text field not empty:
                        2.1. Section will be added to "user" tab.
                        2.2. Resize "User" tab window.
    """

    def add_section(self):
        text, ok_pressed = QInputDialog.getText(self, "Get text", "New Section Name", QLineEdit.Normal, "")
        if ok_pressed and text != '':
            self.frames[1].add_section(text, self.frames[1].sections.count())
            self.tabs.currentWidget().widget().resize_window_height()
            self.save_buttons(self.frames[1].tab_name)

    def change_btns_size(self):
        """
        Change size of all buttons in the tool. size will be saved to next time the tool will be load
        :return:
        """
        num, ok_pressed = QInputDialog.getInt(self, "Side Menu", "Buttons Size (65 - 95):",
                                              Global.btn_size, 65, 95, 1)
        if ok_pressed and num != Global.btn_size:
            Global.btn_size = num
            Global.label_font_size = Global.btn_size_attributes[Global.btn_size]['font-size']
            Global.btn_border = Global.btn_size_attributes[Global.btn_size]['border']
            QCoreApplication.exit(Global.REBOOT_CODE)
            Global.save_configurations()

    """
    Function - add_section

    Brief - Add section to "User" tab.

    Description - 
                    1. Open input text window to enter new section name
                    2. Only when Ok button pressed, and text field not empty:
                        2.1. Section will be added to "user" tab.
                        2.2. Resize "User" tab window.
    """
    def bold_all_btns(self, to_save=True):
        to_bold = True if self.bold_buttons.isChecked() else False
        for frame in self.frames:
            for idx in range(0, frame.sections.count()):
                for btn in frame.sections.itemAt(idx).widget().get_buttons():
                    btn.set_bold(to_bold)
        Global.bold_all_btns = to_bold
        if to_save:
            Global.save_configurations()

    """
    Function - add_new_tab

    Brief - Select tab to add to window

    """
    def add_new_tab(self, title):
        title, ok = QInputDialog.getText(self, 'Add Tab', 'Enter new tab name:')
        if ok and title != "":
            options = []
            sys.path.insert(0, Global.path_to_additional_files)
            from TabTypes import tab_types_exists_buttons, tab_types_custom
            for t in tab_types_custom.keys():
                if t not in options:
                    options.append(t)
            for t in tab_types_exists_buttons.keys():
                if t not in options:
                    options.append(t)
            res = ChooseTabType(options, title)
            if res.exec_() == QDialog.Accepted:
                tab_type = res.scatter_variable[0]
                # Create tab menu.
                btn_set = self.create_btn_set(tab_type)
                self.add_tab(title, btn_set)
                self.save_buttons(title)

    """
        Function - help_page

        Brief - Opens the tool's Wiki page

        """

    def help_page(self):
        os.system("/usr/bin/firefox https://wiki.ith.intel.com/x/aB-1bQ &")

    """
        Function - change_num_of_btns

        Brief - Change number of buttons to display in row.
                The function also save this setting in a file for loading it in the next time.

        """

    def change_num_of_btns(self):
        num, ok_pressed = QInputDialog.getInt(self, "Side Menu", "Number of buttons in a row (5 - 15):",
                                              Global.number_of_btn_in_row, 5, 15, 1)
        if ok_pressed and num != Global.number_of_btn_in_row:
            Global.number_of_btn_in_row = num
            QCoreApplication.exit(Global.REBOOT_CODE)
            Global.save_configurations()

    """
        Function - remove_tab

        Brief - Remove selected custom tab from window

            """
    def remove_tab(self):
        options = {}
        for idx in range(self.tabs.count()):
            if self.tabs.tabText(idx) not in ["Default", "User"]:
                options[self.tabs.tabText(idx)] = idx
        if not options:
            QMessageBox.critical(self, "Remove tab", "There are no custom tabs that can be removed!")
        else:
            res = RemoveTabType(options.keys())
            if res.exec_() == QDialog.Accepted:
                tab = res.scatter_variable[0]
                self.remove_tab_from_menu(options[tab])

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                             Tabs Management                              #
    #                                                                          #
    ############################################################################
    """
        Function - remove_tab_from_menu

        Brief - remove tab from window, by index

        Parameters  -
                        tab_index: int - index of the tab to remove. 

        Description - 
                        1. Remove all section in the tab
                        2. remove tab from window
                        3. Remove tab's configuration file
                        4. Prepare window
                            4.1. Display first tab
                            4.2. Correct window size
        """
    def remove_tab_from_menu(self, tab_index: int):
        tab_title = self.tabs.tabText(tab_index)
        tab_content = self.tabs.widget(tab_index).widget()
        while tab_content.sections.count() != 0:
            tab_content.sections.itemAt(0).widget().remove_section(by_force=True)
        # for child in tab_content.children():
        #    child.setParent(None)
        #    child.deleteLater()
        self.tabs.removeTab(tab_index)
        tab_title = tab_title.replace(" ", ".f10.")
        self.frames.remove(self.frames[tab_index])
        self.frames_scroll_areas.remove(self.frames_scroll_areas[tab_index])
        if os.path.exists(os.path.expanduser(f"~/{tab_title}_btns.pickle")):
            os.system(f'rm {os.path.expanduser(f"~/{tab_title}_btns.pickle")}')
        if tab_index == self.tabs.currentIndex():
            self.tabs.setCurrentIndex(0)

        self.resize_tab_window(self.tabs.currentIndex())

    """
    Function - enable_specific_tab

    Brief - Enable only 1 tab to be activated.

    Parameters  -
                    widget: QWidget - tab to enable. 
                    
    Description - 
                    1. Disable all tabs, except the tab that contains the widget
    """

    def enable_specific_tab(self, widget):

        for i in range(self.tabs.count()):
            if self.tabs.widget(i).widget() != widget:
                self.tabs.setTabEnabled(i, False)

    """
    Function - enable_all_tabs

    Brief - Enable all tabs.

    """

    def enable_all_tabs(self):
        for i in range(self.tabs.count()):
            self.tabs.setTabEnabled(i, True)

    def load_custom_tabs(self):
        """
        Load custom tabs from files when starting up the tool
        """
        for dir_name in os.listdir(os.path.expanduser(f"~/")):
            if dir_name.find("_btns.pickle") != -1 and dir_name not in ['User_btns.pickle', 'Default_btns.pickle']:
                title = str(dir_name.split("_btns.pick")[0]).replace(".f10.", " ")
                self.add_tab(title)

    def add_tab(self, title=None, btn_set=None):
        """
        Adding tabs to tabs list, so it will displayed in tool's window
        :param title: Tab's title
        :param btn_set: Tab's buttons set ( for Default tab no button set needed )
        """
        if not title:
            title = "Default"
            self.frames.append(MainFrame(False))
        elif title == "User":
            self.frames.append(MainFrame(True, title, btn_set=btn_set))
        else:
            self.frames.append(MainFrame(False, title, btn_set=btn_set))
        self.frames_scroll_areas.append(QScrollArea())
        self.frames_scroll_areas[-1].setWidgetResizable(True)
        self.frames_scroll_areas[-1].setWidget(self.frames[-1])
        self.frames_scroll_areas[-1]. \
            setStyleSheet('background: qlineargradient(x1:0, y1:0, x1:1, y1:1,stop:0 white,'
                          'stop: 0.3 rgb(129,129,129),stop:0.5 rgb(150,150,150), stop:0.6 rgb(129,129,129), stop:1 white)')
        self.tabs.addTab(self.frames_scroll_areas[-1], title)

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                             Mouse Events                                 #
    #                                                                          #
    ############################################################################

    """
    Function - mouseMoveEvent ( override function )

    Brief - Invoked when mouse movement has been detected.

    Parameters -    ev: QMouseEvent - mouse event parameters.

    Description - 
                    1. If any button is on 'move' mode, then activate this button's method "mouseMoveEvent"
    """

    def mouseMoveEvent(self, ev: QMouseEvent):
        if Global.btn_on_move is not None:
            Global.btn_on_move.mouseMoveEvent(ev)


    ############################################################################
    #                                                                          #
    #                                                                          #
    #                           Buttons Methods                                #
    #                                                                          #
    ############################################################################

    """
                Function - add_btn_to_section

                Brief - Add button to chosen section

                Parameters:
                            btn   : btn to add in the chosen section

                """

    def add_btn_to_section(self, btn: CadenceButton):
        frame = [f for f in self.frames if f.tab_name == "User"][0]
        sections_titles = []
        for idx in range(0, frame.sections.count()):
            sections_titles.append(frame.sections.itemAt(idx).widget().get_section_title())
        w = ChooseSection(sections_titles, btn.title)
        if w.exec_() == QDialog.Accepted:
            for idx in range(0, frame.sections.count()):
                if frame.sections.itemAt(idx).widget().get_section_title() == w.scatter_variable[0]:
                    coll = frame.sections.itemAt(idx).widget()
                    btn = frame.create_button(btn.title, btn.system_command, btn.description,
                                              coll, btn.current_color)
                    coll.add_next_widget(btn)
                    self.save_buttons("User")

    """
            Function - save_buttons

            Brief - Save tab's buttons and sections set in a file, for loading it in the next time.
            From each button it will get the buttons name,function,description, and color.

            Parameters:
                        tab_title   : str - title of the tab to save its buttons

            """

    def save_buttons(self, tab_title):
        if tab_title != "Default":
            for frame in self.frames:
                if frame.tab_name == tab_title:
                    save_dictionary = {}

                    for idx in range(0, frame.sections.count()):
                        section = frame.sections.itemAt(idx).widget()
                        save_dictionary[section.get_section_title()] = {}
                        for btn in section.get_buttons():
                            if tab_title != "Default":
                                save_dictionary[section.get_section_title()][btn.title] = [btn.system_command,
                                                                                           btn.description,
                                                                                           btn.current_color]
                            else:
                                save_dictionary[section.get_section_title()][btn.title] = btn.current_color
                    tab_title = tab_title.replace(" ", ".f10.")
                    btn_file_path = f'{Global.path_to_save}/{tab_title}_btns.pickle'
                    if not os.path.exists(btn_file_path):
                        os.system(f' touch {btn_file_path}')
                    with open(btn_file_path, 'wb') as f:
                        pickle.dump(save_dictionary, f)

    def create_btn_set(self, tab_type):
        """
        Create buttons set for custom tabs
        :param tab_type: string of the tab type to create for it buttons set
        :return: buttons set
        """
        sys.path.insert(0, Global.path_to_additional_files)
        from TabTypes import tab_types_exists_buttons, tab_types_custom, tab_types_extra_info
        from defaultF10 import default_buttons_dict
        btn_set = {}
        if tab_type in tab_types_exists_buttons.keys():
            for btn_name in tab_types_exists_buttons[tab_type]:
                is_found = False
                for idx in range(0, self.frames[0].sections.count()):
                    section = self.frames[0].sections.itemAt(idx).widget()
                    for btn in section.get_buttons():
                        if btn.title == btn_name:
                            if section.get_section_title() not in btn_set.keys():
                                btn_set[section.get_section_title()] = {'tooltip': '', 'buttons': {}}
                                if 'tooltip' in default_buttons_dict[section.get_section_title()].keys():
                                    btn_set[section.get_section_title()]['tooltip'] = \
                                        default_buttons_dict[section.get_section_title()]['tooltip']
                                if 'color' in default_buttons_dict[section.get_section_title()].keys():
                                    btn_set[section.get_section_title()]['color'] = \
                                        default_buttons_dict[section.get_section_title()]['color']

                            btn_set[section.get_section_title()]['buttons'][btn_name] = [btn.system_command,
                                                                                         btn.description]
                            is_found = True
                            break
                    if is_found:
                        break
        if tab_type in tab_types_custom.keys():
            for section_name in tab_types_custom[tab_type].keys():
                if section_name not in btn_set.keys():
                    btn_set[section_name] = {'tooltip': '', 'buttons': {}}
                    if 'tooltip' in tab_types_extra_info[tab_type][section_name].keys():
                        btn_set[section_name]['tooltip'] = tab_types_extra_info[tab_type][section_name]['tooltip']
                    if 'color' in tab_types_extra_info[tab_type][section_name].keys():
                        btn_set[section_name]['color'] = \
                            tab_types_extra_info[tab_type][section_name]['color']
                for btn_name in tab_types_custom[tab_type][section_name].keys():
                    btn_set[section_name]['buttons'][btn_name] = tab_types_custom[tab_type][section_name][btn_name]
        return btn_set
