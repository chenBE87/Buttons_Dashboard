import _pickle as pickle
import os

from PyQt5.QtCore import QPoint, pyqtSlot, QObject, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

import Global
from CadenceButton import CadenceButton, DEFAULT_BCK_COLOR
from Section import Section

TITLE_HEIGHT_FACTOR = 55


class MainFrame(QWidget):
    """
    MainFrame
   ---------------
    Represent tab's content
    """

    """
    Function - __init__ ( Constructor )

    Brief - init buttons display and functionality.

    Parameters - 
                    editable : bool    - indicates if the box is editable.
                    parent   : Qwidget - button's responsible widget ( default = None ).

    Description - 
                    1. Initiate class variables.
                    2. Create sections holder.
                    3. Create default buttons.
                    4. Set button's attributes.
    """

    def __init__(self, editable, tab_name="Default", parent=None, btn_set=None):
        super().__init__(parent)

        # Initiate class variables.
        self.last_max_btns = 0
        self.editable = editable
        self.tab_name = tab_name

        # Create sections holder.
        self.sections = QVBoxLayout()
        self.sections.setAlignment(Qt.AlignTop)
        self.sections.setSizeConstraint(self.sections.SetMinAndMaxSize)

        # Create default buttons.
        self.set_buttons(btn_set)

        # Set button's attributes.
        self.setLayout(self.sections)
        self.resize_window_height()




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
            Global.btn_on_move.move(ev.globalPos())

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                             Buttons Methods                              #
    #                                                                          #
    ############################################################################
    """
    Function    - create_button

    Brief       - Create button and connect its signals

    Parameters  -    
                    title   : str     - button's name
                    section : Section - the section that will have the button.
                    
    Returns     - The created button.

    Description - 
                    1. Create button.
                    2. Connect button's signals
    """

    def create_button(self, title, command, tooltip, section: Section, color=DEFAULT_BCK_COLOR):
        # Create button.
        btn = CadenceButton(self.editable, self.tab_name, title, command, tooltip, color, self)

        # Connect button's signals
        btn.stop_moving_event.connect(self.replace_buttons)
        btn.start_moving_event.connect(self.button_start_moving)
        btn.remove_button_event.connect(section.remove_button)
        btn.cancel_moving_event.connect(self.replace_buttons)
        btn.save_button_event.connect(self.save_buttons)
        if not self.editable:
            btn.copy_btn_event.connect(self.add_to_section)
        btn.set_bold(Global.bold_all_btns)
        return btn

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                             Section's Methods                            #
    #                                                                          #
    ############################################################################
    """
    Function    - rebuild_empty_section

    Brief       - Rebuild the input section, if its grid is empty.

    Parameters  -    
                    section : Section     - section to rebuild, if needed.

    Returns     - if section rebuild, then the new section. Else, the input section.

    Description - Due to GUI limitation, if section is empty and already displayed, then added button will not be
                  display as expected. Therefore, the system need to remove and add again the section,
                  for displaying the new button.
    """

    def rebuild_empty_section(self, section: Section):
        if section.get_grid().isEmpty():
            index = self.sections.indexOf(section)
            coll_title = section.toggle_button.text()
            self.remove_section(section)
            section = self.add_section(coll_title, index)
        return section

    """
    Function    - add_section

    Brief       - Add new section to tab.

    Parameters  -    
                    title : str - section title.
                    index : int - index to insert the section.

    Returns     - The created section.

    Description - 
                    1. Create grid.
                    2. Create section.
                    3. Connect section's signals.
                    4. Insert grid into the section.
                    5. Insert section to the section holder.
                    6. Collapse section.
    """

    def add_section(self, title, index):
        # Create grid.
        grid = QVBoxLayout()
        grid.setSpacing(1)
        grid.setContentsMargins(5, 2, 5, 2)
        grid.setAlignment(Qt.AlignTop)

        # Create section.
        section = Section(self, self.editable, title)

        # Connect section's signals.
        section.cancel_moving_event.connect(self.replace_buttons)
        section.stop_moving_event.connect(self.drop_btn_in_section)
        section.add_exist_button_event.connect(self.create_existing_button)
        section.add_new_button_event.connect(self.create_new_button)
        section.remove_section_event.connect(self.remove_section)
        section.section_renamed_event.connect(self.save_buttons)
        section.move_section_event.connect(self.move_section)
        section.button_deleted.connect(self.save_buttons)

        # Insert grid into the section.
        section.set_grid(grid)

        # Insert section to the section holder.
        self.sections.insertWidget(index, section)

        # Collapse section.
        if not section.checked:
            section.collapse(1)
        return section

    """
    Function    - rearrange_section

    Brief       - Recreate section. Because API limitation, sometimes  when editing the buttons in a section, it will
                  not represent the buttons well. This method will delete and recreate the section, for display all 
                  buttons, as expected.

    Parameters  -    
                    section : Section - section to rearrange.

    Returns     - The new section section.

    Description - 
                    1. Create grid.
                    2. Create section.
                    3. Connect section's signals.
                    4. Insert grid into the section.
                    5. Insert section to the section holder.
                    6. Collapse section.
    """
    def rearrange_section(self, section: Section):
        all_btns = []
        index = self.sections.indexOf(section)
        title = section.toggle_button.text()
        btn = section.remove_last_widget()
        while btn:
            all_btns.append(btn)
            btn = section.remove_last_widget()
        all_btns.reverse()
        # Create grid.
        grid = QVBoxLayout()
        grid.setSpacing(10)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setAlignment(Qt.AlignTop)

        # Create section.
        section = Section(self, self.editable, title)

        # Connect section's signals.
        section.cancel_moving_event.connect(self.replace_buttons)
        section.stop_moving_event.connect(self.drop_btn_in_section)
        section.add_exist_button_event.connect(self.create_existing_button)
        section.add_new_button_event.connect(self.create_new_button)
        section.remove_section_event.connect(self.remove_section)
        section.section_renamed_event.connect(self.save_buttons)
        section.move_section_event.connect(self.move_section)

        # Insert grid into the section.
        section.set_grid(grid)

        # Insert section to the section holder.
        self.sections.takeAt(index).widget().deleteLater()
        self.sections.insertWidget(index, section)
        for btn in all_btns:
            btn.remove_button_event.connect(section.remove_button)
            section.add_next_widget(btn)
        section.collapse(1)
        return section


    ############################################################################
    #                                                                          #
    #                                                                          #
    #                                Searches                                  #
    #                                                                          #
    ############################################################################
    """
    Function    - find_row_and_grid

    Brief       - Find button's section, grid and row.

    Parameters  -    
                    required_btn : QPushButton - button to search its grid and row.

    Returns     - Button's section, grid and row.
    """

    def find_btn_parents(self, required_btn: QPushButton):
        for i in range(self.sections.count()):
            section = self.sections.itemAt(i).widget()
            # if type(item) == Section:
            grid = section.get_grid()
            for j in range(grid.count()):
                row = grid.itemAt(j).layout()
                for k in range(row.count()):
                    btn = row.itemAt(k).widget()
                    if type(btn) == CadenceButton and required_btn == btn:
                        return section, grid, row

    """
        Function    - find_section_by_grid

        Brief       - Find section by its grid.

        Parameters  -    
                        grid : QVBoxLayout - grid to find its section.

        Returns     - grid's section.
        """

    def find_section_by_grid(self, grid: QVBoxLayout):
        for i in range(self.sections.count()):
            item = self.sections.itemAt(i).widget()
            if type(item) == Section:
                if grid == item.get_grid():
                    return item

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                             Miscellaneous                                #
    #                                                                          #
    ############################################################################
    """
        Function    - setMouseTracking ( override )

        Brief       - Set in all application mouse tracking to 'flag' value.

        Parameters  -    
                        flag : bool - value to assign.

        Description - The method contain sub method which go through all children and assign the 'flag' value to the 
                      setMouseTracking method.
        """

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    """
        Function    - resize_window_height

        Brief       - resize windows height according to the number of section in the tab.


        Description - 
                        1. Resize main window.
                        2. Resize tab.
                        3. Reset sections layout.
                        4. Update changes in tab
                        5. Update changes in main window  
        """

    def resize_window_height(self):
        total_height = 0
        screen_height_factor = 0.9
        for i in range(self.sections.count()):
            num_of_rows = self.sections.itemAt(i).widget().get_grid().count()
            if total_height + TITLE_HEIGHT_FACTOR - Global.screen_height*screen_height_factor < 0:
                total_height += TITLE_HEIGHT_FACTOR
            for j in range(0, num_of_rows):
                if total_height + Global.btn_height - Global.screen_height*screen_height_factor < 0:
                    total_height += Global.btn_height
        total_height = max(total_height, 300)
        self.window().setFixedSize(Global.btn_width*Global.number_of_btn_in_row, total_height)
        self.setFixedSize(Global.btn_width*Global.number_of_btn_in_row, total_height)
        self.setLayout(self.sections)
        self.update()
        self.window().update()
        if self.sections.count() > 0:
            checked = self.sections.itemAt(0).widget().checked
            self.sections.itemAt(0).widget().decollapse()
            self.sections.itemAt(0).widget().collapse()
            if checked:
                self.sections.itemAt(0).widget().decollapse()

    def set_buttons(self, btn_set):
        """
        set default/custom sections and buttons for tab.
        :param btn_set: list of buttons set for placing in the frame.

        Description:
            1. If this frame is not editable & tab name is "Default", then the buttons will be created
               from the defaultF10 file.
            2. If btn_set is None and frame config file exists, than the burrons set will be extracted from it.
            3. If btn_set is not None it will be used as buttons set
            4. If step 1-3 not processed, frame will not be set with buttons
            5. Setting buttons:
                5.1 Creating each section
                5.2 Creating buttons for each section

        """
        title = self.tab_name.replace(" ", ".f10.")
        if not self.editable and self.tab_name == "Default":
            btns_to_create = Global.all_buttons_dict

        elif not btn_set and os.path.isfile(f'{Global.path_to_save}/{title}_btns.pickle'):
            with open(f'{Global.path_to_save}/{title}_btns.pickle', "rb") as f:
                btns_to_create = pickle.load(f)
        else:
            btns_to_create = btn_set if btn_set else {}
        if not btns_to_create:
            self.add_section("Default Section", self.sections.count())
        else:
            for (key, val) in btns_to_create.items():
                coll = self.add_section(key, self.sections.count())
                if self.tab_name != "User" and 'tooltip' in val.keys() and val['tooltip'] != '':
                    coll.set_tooltip(val['tooltip'])

                buttons = val['buttons'] if self.tab_name != "User" else val
                for name, props in buttons.items():
                    if not self.editable:
                        color = 'lightGray'
                        if isinstance(val, dict) and 'color' in val.keys():
                            color = val['color']
                    else:
                        color = DEFAULT_BCK_COLOR if len(props) == 2 else props[2]
                    btn = self.create_button(name, props[0], props[1], coll, color)

                    coll.add_next_widget(btn)

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                                Slots                                     #
    #                                                                          #
    ############################################################################

    @pyqtSlot(CadenceButton)
    def add_to_section(self, btn: CadenceButton):
        """
        A callback to add ( copy ) button from "Default" Section to "User" Section
        :param btn: button to copy
        """
        self.window().add_btn_to_section(btn)


    """
        Function    - replace_buttons

        Brief       - Replace between the 'on move' button and the input button.
        
        Parameters  -
                       btn: QPushButton - button to switch with the 'on move' button.   


        Description -   1. set mouseOnTracking variable to False in all widgets.
                        2. Enable all tabs.
                        3. When the input button is the 'on move' button then
                           the 'on move' button will return its original place.
                        4. In other case the buttons will be switched.
                        5. Set the 'is_on_move' attribute of the 'on move' button to false.
                        6. Reset global variables to None:
                            6.1. btn_on_move
                            6.2  btn_grid
                        7. save frame's buttons in file.
        """

    @pyqtSlot(QPushButton)
    def replace_buttons(self, btn: QPushButton):
        self.setMouseTracking(False)
        self.window().enable_all_tabs()

        if btn == Global.btn_on_move:
            # same button , move to original place
            section = Global.btn_section
            section.add_button_at(Global.btn_index[0], Global.btn_index[1], Global.btn_on_move)
            self.rearrange_section(section)
        else:

            section, grid, row = self.find_btn_parents(btn)
            if section == Global.btn_section:
                # replace buttons in same grid
                section.switch_btn_with_moved_btn(btn)
                self.rearrange_section(section)
            else:
                # replace buttons in different grids
                src_section = Global.btn_section
                try:
                    Global.btn_on_move.remove_button_event.disconnect()
                except Exception:
                    pass
                Global.btn_on_move.remove_button_event.connect(section.remove_button)
                btn.remove_button_event.disconnect()
                btn.remove_button_event.connect(src_section.remove_button)

                dst_index = section.get_button_cell_index(btn)
                section.remove_button_at(dst_index[0], dst_index[1])
                section.add_button_at(dst_index[0], dst_index[1], Global.btn_on_move)
                src_section.add_button_at(Global.btn_index[0], Global.btn_index[1], btn)
                self.rearrange_section(src_section)
                self.rearrange_section(section)
        Global.btn_on_move.set_is_on_move(False)
        Global.btn_on_move = None
        Global.btn_section = None
        self.resize_window_height()
        self.save_buttons()

    """
        Function    - button_start_moving

        Brief       - Prepare system to 'button on move' status, which means one of the button is in 'move' state.

        Parameters  -
                       btn: QPushButton - button that will enter to 'move' state.   


        Description - 
                        1. Disable all other tabs in the application.
                        2. Collapse all sections in tab.
                        3. Assign to the Global variable btn_index the index of the input tab.
                        4. Remove the input button from its section.
                        5. Set all widget's mouseTracking attribute to True.
                        6. Set Global variables:
                            6.1 Input button assigned to btn_on_move.
                            6.2 Input button's grid assigned to btn_grid
                        
        """

    @pyqtSlot(CadenceButton)
    def button_start_moving(self, btn: CadenceButton):
        # Disable all other tabs in the application.
        self.window().enable_specific_tab(self)

        # Collapse all sections in tab.
        for i in range(self.sections.count()):
            item = self.sections.itemAt(i).widget()
            if type(item) == Section:
                if not item.checked:
                    item.collapse(1)
        # Assign to the Global variable btn_index the index of the input tab.
        section, grid, row = self.find_btn_parents(btn)
        Global.btn_index = section.get_button_cell_index(btn)

        # Remove the input button from its section.
        section.remove_specific_button(btn)
        section = self.rearrange_section(section)
        section.save_current_buttons_array()
        self.resize_window_height()
        btn.setParent(self)
        btn.show()
        # Set all widget's mouseTracking attribute to True.
        self.setMouseTracking(True)
        self.window().setMouseTracking(True)

        # Set Global variables
        Global.btn_on_move = btn
        Global.btn_section = section

    def save_buttons(self):
        """
        Saves the current main fram instance's buttons and sections
        """
        self.window().save_buttons(self.tab_name)

    """
        Function    - drop_btn_in_section

        Brief       - Add the 'on move' button to the input section.

        Parameters  -
                       point       :  QPoint  - Position to enter the button.
                       dst_section :  Section - section to drop the button.


        Description -   1. set mouseOnTracking variable to False in all widgets.
                        2. Enable all tabs.
                        3. reconnect signal 'remove_button_event' to the input section's method.
                        4. implement the button in the place which related to the input point.
                           the 'on move' button will return its original place.
                        5. Set the 'is_on_move' attribute of the 'on move' button to false.
                        6. Reset global variables to None:
                            6.1. btn_on_move
                            6.2  btn_grid

        """

    @pyqtSlot(QPoint, Section)
    def drop_btn_in_section(self, point: QPoint, dst_section: Section):
        self.setMouseTracking(False)
        self.window().enable_all_tabs()
        dst_section = self.rebuild_empty_section(dst_section)
        #Global.btn_on_move.remove_button_event.disconnect()
        Global.btn_on_move.remove_button_event.connect(dst_section.remove_button)
        grid = dst_section.get_grid()
        has_implemented = False
        for row_index in range(grid.count()):

            if not has_implemented:
                row = grid.itemAt(row_index).layout()
                bottom = row.geometry().bottom() + 20
                if point.y() <= bottom:
                    for col_index in range(row.count()):
                        if not has_implemented:
                            btn = row.itemAt(col_index).widget()
                            right = btn.geometry().right()
                            if point.x() <= right:
                                dst_section.add_button_at(row_index, col_index, Global.btn_on_move)
                                has_implemented = True
                    if not has_implemented:
                        dst_section.add_button_at(row_index, grid.itemAt(row_index).layout().count(), Global.btn_on_move)
                        has_implemented = True
        if not has_implemented:
            dst_section.add_next_widget(Global.btn_on_move)
        Global.btn_on_move.set_is_on_move(False)
        Global.btn_on_move = None
        Global.btn_section = None
        self.rearrange_section(dst_section)
        self.resize_window_height()
        self.save_buttons()

    """
        Function    - create_existing_button

        Brief       - Create new button from default buttons list.

        Parameters  -
                       title   :  str  - button title.
                       section :  Section - section to add the button.


        Description -   1. Rebuild the section if it is empty.
                        2. Create the new button.
                        3. Add it to the section.
                        4. Resize application's height.
                        5. save frame's buttons in file.

        """

    @pyqtSlot(str, str, str, QWidget)
    def create_existing_button(self, title: str, command, tooltip, section: Section):
        # Rebuild the section if it is empty.
        section = self.rebuild_empty_section(section)

        # Create the new button.
        btn = self.create_button(title, command, tooltip, section)

        # Add it to the section.
        section.add_next_widget(btn)

        # Resize application's height.
        if section.get_grid().count() > 1:
            self.rearrange_section(section)
            self.resize_window_height()
        self.save_buttons()

    """
        Function    - create_new_button

        Brief       - Create button that is not from default buttons list.

        Parameters  -
                       btn_params   :  list  - buttons parameters to build it ( name, description, procedure to invoke).
                       section :  Section - section to add the button.


        Description -   1. Rebuild the section if it is empty.
                        2. Add description to the buttons descriptions dictionary.
                        3. Create the button.
                        4. Add to button the requested procedure.
                        5. Add button to section.
                        5. Resize application's height.
                        6. save frame's buttons in file.

        """

    @pyqtSlot(list, QWidget)
    def create_new_button(self, btn_params: list, section: Section):
        # Rebuild the section if it is empty.
        section = self.rebuild_empty_section(section)

        # Add description to the buttons descriptions dictionary.
        #Global.all_buttons_desc[btn_params[0]] = btn_params[1]
        # Create the button.
        btn = self.create_button(btn_params[0], btn_params[1], btn_params[2], section)

        # Add to button the requested procedure.
        #btn.system_command = btn_params[2]

        # Add button to section.
        section.add_next_widget(btn)

        # Resize application's height.
        if section.get_grid().count() > 1:
            self.rearrange_section(section)
            self.resize_window_height()
        self.save_buttons()

    """
        Function    - remove_section

        Brief       - remove the requested section from tab.

        Parameters  -
                       section :  Section - section to remove.
        """

    @pyqtSlot(QWidget)
    def remove_section(self, section: Section):
        self.sections.takeAt(self.sections.indexOf(section))
        section.setParent(None)
        section.deleteLater()
        self.resize_window_height()
        self.save_buttons()

    """
            Function    - move_section

            Brief       - move section to different place in the frame
            
            Parameters  -
                       section      :  Section  - section to change place.
                       direction    :  str - the direction to place the section (Up, Down, Top, Bottom).
            """
    @pyqtSlot(QWidget, str)
    def move_section(self, section: Section, direction: str):
        index = self.sections.indexOf(section)
        if direction == "Up":
            if index != 0:
                self.sections.takeAt(index)
                self.sections.insertWidget(index - 1, section)
        elif direction == "Down":
            if index != self.sections.count() - 1:
                self.sections.takeAt(index)
                self.sections.insertWidget(index + 1, section)
        elif direction == "First":
            if index != 0:
                self.sections.takeAt(index)
                self.sections.insertWidget(0, section)
        elif direction == "Last":
            if index != self.sections.count() - 1:
                self.sections.takeAt(index)
                self.sections.insertWidget(self.sections.count(), section)
        self.save_buttons()
