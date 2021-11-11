from PyQt5.QtCore import Qt, QPropertyAnimation, QAbstractAnimation, pyqtSlot, pyqtSignal, \
    QPoint
from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtWidgets import QSizePolicy, QWidget, QScrollArea, QVBoxLayout, QMessageBox, \
    QFrame, QToolButton, QPushButton, QLayoutItem, \
    QMenu, QAction, QDialog, QInputDialog, QLineEdit, QHBoxLayout

import Global
from AddButtonDialog import AddButtonDialog
from SingleOptionChooseDialog import MoveSectionDialog


class Section(QWidget):
    """
    Section
   ---------------
    Represent application Section
    """

    # Signals
    stop_moving_event = pyqtSignal(QPoint, QWidget)
    cancel_moving_event = pyqtSignal(QPushButton)
    add_exist_button_event = pyqtSignal(str, str, str, QWidget)
    add_new_button_event = pyqtSignal(list, QWidget)
    remove_section_event = pyqtSignal(QWidget)
    section_renamed_event = pyqtSignal(QWidget)
    move_section_event = pyqtSignal(QWidget, str)
    button_deleted = pyqtSignal(QPushButton)


    """
    Function - __init__ ( Constructor )

    Brief - init section's display and functionality.

    Parameters - 
                    editable : bool    - indicates if the box is editable.
                    title    : str     - Section title ( default = "" ).
                    parent   : Qwidget - button's responsible widget ( default = None ).

    Description - 
                    1. Create collapse/de-collapse toggle button.
                    2. Create "content area" variable, for holding buttons grid.
                    3. Create toggle animation variable.
                    4. Create layout and add all objects above.
                    5. Initiate class variables.
                    6. Set box attributes.
    """

    def __init__(self, frame, editable, title="",  parent=None):

        super(Section, self).__init__(parent)

        self.setStyleSheet('background-color:rgba(0,0,0,0);')

        # Create collapse/de-collapse toggle button.
        self.toggle_button = QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet(f"QToolButton {{ border: none; font-size:13px;"
                                         f"font-weight: bold;background-color:rgba(0,0,0,0);}}")
        self.toggle_button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)
        self.toggle_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.toggle_button.customContextMenuRequested[QPoint].connect(self.right_menu)

        # Create "content area" variable, for holding buttons grid.
        self.content_area = QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.content_area.setFrameShape(QFrame.NoFrame)

        # Create toggle animation variable.

        self.decollapse_section_animation = QPropertyAnimation(self, b"minimumHeight")
        self.collapse_section_animation = QPropertyAnimation(self, b"maximumHeight")
        self.collapse_content_animation = QPropertyAnimation(self.content_area, b"maximumHeight")

        # Create layout to hold all objects above.
        self.lay = QVBoxLayout(self)
        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSizeConstraint(self.lay.SetNoConstraint)
        self.lay.addWidget(self.toggle_button)
        self.lay.addWidget(self.content_area)

        # Initiate class variables.
        self.frame = frame
        self.checked = self.toggle_button.isChecked()
        self.editable = editable
        self.__row = -1
        self.__col = 0
        self.__grid = None
        self.__buttons = []
        self.__copy_buttons = []
        self.__title = title

        # Set box attributes.
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                           Getters/Setters                                #
    #                                                                          #
    ############################################################################
    def get_buttons(self):
        return self.__buttons

    def get_section_title(self):
        return self.__title

    def get_grid(self):
        return self.__grid

    def get_current_row(self):
        return self.__row

    def get_current_column(self):
        return self.__col

    def save_current_buttons_array(self):
        self.__copy_buttons = self.__buttons.copy()

    def set_tooltip(self, tooltip):
        self.toggle_button.setToolTip(f'<div style="background-color:white;font-size:15px; width:1500px;"><nobr>{tooltip}</nobr></div>')

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                           Mouse Event                                    #
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

    """
    Function - mousePressEvent ( override function )

    Brief - Invoked when one og mouse buttons has been pressed.

    Parameters -    ev: QMouseEvent - mouse event parameters.

    Description - 
                    1. When left Button pressed:
                        1.1. If there is any button on 'move' mode, then emit 'stop_moving_event' signal.
                    2. When right button pressed:
                        2.1. If there is any button on 'move' mode, then emit 'cancel_moving_event' signal.
    """
    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() == Qt.LeftButton:
            if Global.btn_on_move is not None:
                self.stop_moving_event.emit(ev.pos(), self)
        elif ev.button() == Qt.RightButton:
            if Global.btn_on_move is not None:
                self.cancel_moving_event.emit(Global.btn_on_move)

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                           Animations                                     #
    #                                                                          #
    ############################################################################
    """
    Function - collapse

    Brief - invoke box collapse animation.

    Description - 
                    1. Change toggle button's arrow to 'Down'.
                    2. Prepare and invoke the animation.
    """
    def collapse(self, time=100):
        # Change toggle button's arrow to 'Down'.
        self.toggle_button.setArrowType(Qt.DownArrow)
        self.collapse_section_animation.setDuration(time)
        self.collapse_content_animation.setDuration(time)
        # Prepare and invoke the animation.
        self.collapse_section_animation.setDirection(QAbstractAnimation.Forward)
        self.collapse_content_animation.setDirection(QAbstractAnimation.Forward)
        self.collapse_section_animation.start()
        self.collapse_content_animation.start()
        self.checked = False

    """
        Function - decollapse

        Brief - invoke box decollapse animation.

        Description - 
                        1. Change toggle button's arrow to 'Right'.
                        2. Prepare and invoke the animation.
        """
    def decollapse(self, time=100):
        # Change toggle button's arrow to 'Right'.
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.collapse_section_animation.setDuration(time)
        self.collapse_content_animation.setDuration(time)
        # Prepare and invoke the animation.
        self.collapse_section_animation.setDirection(QAbstractAnimation.Backward)
        self.collapse_content_animation.setDirection(QAbstractAnimation.Backward)
        self.collapse_section_animation.start()
        self.collapse_content_animation.start()
        self.checked = True
    ############################################################################
    #                                                                          #
    #                                                                          #
    #                           Content Management                             #
    #                                                                          #
    ############################################################################
    """
        Function - set_grid

        Brief - Set Box grid.

        Parameters -    ev: QMouseEvent - mouse event parameters.

        Description - 
                        1. When left Button pressed:
                            1.1. If there is any button on 'move' mode, then emit 'stop_moving_event' signal.
                        2. When right button pressed:
                            2.1. If there is any button on 'move' mode, then emit 'cancel_moving_event' signal.
        """
    def set_grid(self, grid: QVBoxLayout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(grid)
        self.__grid = grid
        collapsed_height = (
                self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = grid.sizeHint().height()

        self.collapse_section_animation.setDuration(100)
        self.collapse_section_animation.setStartValue(collapsed_height)
        self.collapse_section_animation.setEndValue(collapsed_height + content_height)

        self.collapse_content_animation.setDuration(100)
        self.collapse_content_animation.setStartValue(0)
        self.collapse_content_animation.setEndValue(content_height)

        self.collapse_section_animation.setDuration(0)
        self.collapse_content_animation.setDuration(0)

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                           Grid Management                                #
    #                                                                          #
    ############################################################################
    """
        Function    - get_button_cell_index

        Brief       - Get button's row and coll, if exists in the grid.

        Parameters  -    
                        btn: QPushButton - button to search.
        
        Returns     -   (row,column) if button exists. Else, (-1,-1)

        """
    def get_button_cell_index(self, btn: QPushButton, from_copy=False):
        try:
            if from_copy:
                index = self.__copy_buttons.index(btn)
            else:
                index = self.__buttons.index(btn)
        except ValueError:
            return -1, -1
        return divmod(index, Global.number_of_btn_in_row)

    """
        Function    - add_next_item

        Brief       - Add item in the next free cell in grid.

        Parameters  -    
                        item: QLayoutItem - item to add.


        """
    def add_next_item(self, item: QLayoutItem):
        # if next row have not been created yet, create one.
        if self.__row == -1 or self.is_row_full(self.__row):
            self.add_row()
        self.__grid.itemAt(self.__row).layout().addItem(item)
        self.__col = self.__col + 1
        self.__buttons.append(item.widget())
        if self.is_row_full(self.__row):
            self.add_row()

        # set the grid again for forcing the system to be updated with the added button.
        self.set_grid(self.__grid)

    """
            Function    - is_current_row_full

            Brief       - return if the current row is full.
            

            Returns     - True if current row is full. Else, False. 

            """
    def is_row_full(self):
        return self.__col == Global.number_of_btn_in_row

    """
        Function    - remove_button_at

        Brief       - remove button in the requested row and column.

        Parameters  -    
                        row:    int - button's row.
                        column: int - buttons column

        Returns     - the removed button or 'None' if button's cell location not in range. 

        """
    def remove_button_at(self, row, column):
        all_btns = []
        button = None
        btn = self.remove_last_widget()
        is_inserted = False
        while btn:
            all_btns.append(btn)
            btn = self.remove_last_widget()
        all_btns.reverse()
        while all_btns:
            if not is_inserted and (row == 0 and column == 0) or (self.__row == row and self.__grid.itemAt(self.__row).layout().count() == column):
                button = all_btns.pop(0)
                is_inserted = True
            if all_btns:
                self.add_next_widget(all_btns.pop(0))
        self.set_grid(self.__grid)
        return button

    def remove_last_widget(self):
        """
        Remove last widget in the grid ( last widget in the last row )
        :return: The removed widget or None, if section is empty.
        """
        if self.__row >= 0:
            self.__col = self.__col - 1
            if self.__col < 0:
                self.__col = Global.number_of_btn_in_row - 1
                empty_row = self.__grid.takeAt(self.__row)
                empty_row.deleteLater()
                self.__row = self.__row - 1
                self.collapse(1)
            if self.__row >= 0:
                item = self.__grid.itemAt(self.__row).layout().takeAt(self.__col)
                self.set_grid(self.__grid)
                self.collapse()
                self.__buttons.remove(item.widget())
                return item.widget()
        return None

    """
        Function    - remove_specific_button

        Brief       - remove specific button from section.

        Parameters  -    
                        btn: QPushButton - button to remove.

        Returns     - the removed button or 'None' if button's not in section. 

        """
    def remove_specific_button(self, btn: QPushButton):
        row, col = self.get_button_cell_index(btn)
        return self.remove_button_at(row, col)

    """
        Function    - add_next_widget

         Brief       - Add widget in the next free cell in grid.

        Parameters  -    
                        widget: QWidget - widget to add. 

        """
    def add_next_widget(self, widget: QWidget):
        # if next row have not been created yet, create one.
        if self.__row == -1 or self.is_row_full():
            self.add_row()
        self.__grid.itemAt(self.__row).layout().addWidget(widget)
        self.__col = self.__col + 1
        self.__buttons.append(widget)
        if self.is_row_full():
            self.add_row()
        # set the grid again for forcing the system to be updated with the added button.
        self.set_grid(self.__grid)

    """
        Function    - add_row

         Brief       - Add row to grid.

        """
    def add_row(self):
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignLeft)
        row.setSpacing(3)
        row.setContentsMargins(3, 3, 3, 3)
        self.__grid.addLayout(row)
        self.__row = self.__row + 1
        self.__col = 0

    """
        Function    - add_button_at

         Brief       - Add button in specific grid cell.

        Parameters  -    
                        row:    int         - button's row.
                        column: int         - buttons column 
                        button: QPushButton - button to insert. 

        """
    def add_button_at(self, row, column, button: QPushButton):
        all_btns = []
        btn = self.remove_last_widget()
        while btn:
            all_btns.append(btn)
            btn = self.remove_last_widget()
        all_btns.reverse()
        while all_btns:
            if button and (row == 0 and column == 0) or self.__row == row and self.__grid.itemAt(self.__row).layout().count() == column:
                self.add_next_widget(button)
                button = None
            self.add_next_widget(all_btns.pop(0))
        if button:
            self.add_next_widget(button)
        self.set_grid(self.__grid)

    def reorder(self):
        all_btns = []
        while self.__row >= 0:
            all_btns.append(self.remove_button_at(self.__row, self.__grid.itemAt(self.__row).layout().count() - 1))
        all_btns.reverse()
        while all_btns:
            self.add_next_widget(all_btns.pop(0))

    """
        Function        - switch_btn_with_moved_btn

         Brief          - switch between buttons in the same cell.

        Parameters      -    
                            dst_btn: QPushButton - button to switch with the 'on move' button, that was originally
                            in this cell.
        
        Description     -
                            1. Get index of the button that will be switched
                            2. remove the current location of the button that is not moving now.
                            3. Add the buttons in there destination indexes.
                            4. Recreate sections buttons 

        """
    def switch_btn_with_moved_btn(self, dst_btn: QPushButton):
        moved_btn_index = Global.number_of_btn_in_row*Global.btn_index[0] + Global.btn_index[1]
        dst_btn_index = self.__copy_buttons.index(dst_btn)

        self.__copy_buttons.remove(dst_btn)
        self.__copy_buttons.insert(dst_btn_index,  Global.btn_on_move)
        self.__copy_buttons.insert(moved_btn_index, dst_btn)

        all_btns = []
        btn = self.remove_last_widget()
        while btn:
            if btn != dst_btn:
                all_btns.append(btn)
            btn = self.remove_last_widget()

        for idx, btn in enumerate(self.__copy_buttons):
            self.add_next_widget(btn)

        self.set_grid(self.__grid)

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                   Button's Right Menu Methods                            #
    #                                                                          #
    ############################################################################
    """
    Function - right_menu

    Brief - Invoke menu when right mouse button clicked, if button is editable.

    Description -   
                    1.1. if button is editable:
                        1.1. Create menu and menu buttons.
                        1.2. Add menu buttons to the menu variable.
                        1.3. Show menu.
    """
    def right_menu(self):
        if self.editable and Global.btn_on_move is None:
            # Create menu and menu buttons.
            menu = QMenu('Edit Options')
            add_action = QAction('Add Button', self, triggered=self.add_button_request)
            rename_action = QAction('Rename Section', self, triggered=self.rename)
            remove_action = QAction('Remove Section', self, triggered=self.remove_section)
            move_action = QAction('Move Section', self, triggered=self.move_section)

            # Add menu buttons to the menu variable.
            menu.addAction(move_action)
            menu.addSeparator()
            menu.addAction(add_action)
            menu.addAction(rename_action)
            menu.addSeparator()
            menu.addAction(remove_action)

            # Show menu.
            menu.exec_(QCursor.pos())

    def move_section(self):
        """
        Method to move section's location in the frame
        """
        w = MoveSectionDialog(["Up", "Down", "First", "Last"], self.toggle_button.text())
        if w.exec_() == QDialog.Accepted:
            self.move_section_event.emit(self, w.scatter_variable[0])

    """
    Function - add_button_request

    Brief    - handle 'add button' request from the right menu

    Description -   
                    1.1. if button is editable:
                        1.1. Create menu and menu buttons.
                        1.2. Add menu buttons to the menu variable.
                        1.3. Show menu.
    """
    def add_button_request(self):
        w = AddButtonDialog(self.toggle_button.text())
        if w.exec_() == QDialog.Accepted:
            if w.output_variables_list[0] == w.EXIST_BTN_INDEX:
                title = w.output_variables_list[1]
                command = w.output_variables_list[2]
                tooltip = w.output_variables_list[3]
                self.add_exist_button_event.emit(title,command,tooltip, self)
            else:
                w.output_variables_list.remove(w.output_variables_list[0])
                self.add_new_button_event.emit(w.output_variables_list, self)

    """
    Function - rename

    Brief    - rename section

    Description -   
                    1. raise dialog box to get the 'new name' string.
                    2. if Ok button pressed and the 'new name' string is not empty, section name will be replaced with
                       'new name' string value.
    """
    def rename(self):
        text, ok_pressed = QInputDialog.getText(QWidget(),
                                                'Rename section "' + self.toggle_button.text() + '"',
                                                "New Section Name:",
                                                QLineEdit.Normal, "")
        if ok_pressed and text != '':
            self.toggle_button.setText(text)
            self.__title = text
            self.section_renamed_event.emit(self)

    """
    Function - remove_section

    Brief    - remove section

    Description -   
                    1. raise question box verify the remove from user.
                    2. if Yes button pressed:
                        2.1. remove all buttons.
                        2.2. remove main layout.
                        2.3. remove toggle button and toggle animation variables.
                        2.4. emit 'remove_section_event' signal.
    """
    def remove_section(self, by_force=False):
        if not by_force:
            ret = QMessageBox.question(QWidget(),
                                       'Remove section',
                                       'Are you sure you want to delete section "' + self.toggle_button.text() + '" ?',
                                       QMessageBox.Yes | QMessageBox.No)
        else:
            ret = QMessageBox.Yes
        if ret == QMessageBox.Yes:
            while not self.__grid.isEmpty():
                item = self.remove_button_at(0, 0)
                item.setParent(None)
                item.deleteLater()
            del self.lay
            del self.content_area
            del self.toggle_button
            self.remove_section_event.emit(self)

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                                Slots                                     #
    #                                                                          #
    ############################################################################
    """
    Function - on_pressed

    Brief    - handle mouse press on toggle button. toggling between 'collapse' and 'de-collapse'.

    """
    @pyqtSlot()
    def on_pressed(self):
        if Global.btn_on_move is None and self.__title != " ":
            if self.checked:
                self.collapse()
            else:
                self.decollapse()
    """
        Function    - remove_button

         Brief      - remove specific button from section, if exist.

        Parameters  -    
                        btn: QPushButton - button to remove.
                        
        Description -
                        1. get button's row and column 
                        2. the row and column are valid, remove button from that row and column

        """
    @pyqtSlot(QPushButton)
    def remove_button(self, btn: QPushButton):
        row, col = self.get_button_cell_index(btn)
        if row >= 0 and col >= 0:
            item = self.remove_button_at(row, col)
            item.setParent(None)
            item.deleteLater()
            self.button_deleted.emit(Global.btn_on_move)
