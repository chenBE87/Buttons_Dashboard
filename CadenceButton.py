import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QSizePolicy, QMenu, QAction, QColorDialog, QMessageBox, \
    QLineEdit, QInputDialog, QWidget

import Global

DEFAULT_BCK_COLOR = "lightGray"


class CadenceButton(QPushButton):
    """
    CadenceButton
   ---------------
    Represent application button   
    """

    # Signals
    remove_button_event = pyqtSignal(QPushButton)
    start_moving_event = pyqtSignal(QPushButton)
    stop_moving_event = pyqtSignal(QPushButton)
    cancel_moving_event = pyqtSignal(QPushButton)
    save_button_event = pyqtSignal(QPushButton)
    copy_btn_event = pyqtSignal(QPushButton)
    """
    Function - __init__ ( Constructor )
    
    Brief - init buttons display and functionality.

    Parameters - 
                    editable : bool    - indicates if the box is editable.
                    txt      : str     - text to implement in the button.
                    parent   : Qwidget - button's responsible widget ( default = None ).

    Description - 
                    1. Initiate class variables.
                    2. Initiate button label that displays button's text.
                    3. Set policies.
                    4. Set button's style ( GUI representation ).
    """

    def __init__(self, editable, tab_name: str, txt: str, command: str, tooltip: str, color=DEFAULT_BCK_COLOR,
                 parent=None):
        super().__init__(parent)

        # Initiate class variables.
        self.__is_on_move = False
        self.__mouse_curr_pos = None
        self.system_command = command
        self.description = tooltip
        self.title = txt
        self.button_color = color
        self.current_color = color
        self.editable = editable
        self.tab_name = tab_name
        self.setObjectName(txt)

        # Initiate button label that displays button's text.
        self.lbl = QLabel(txt)
        self.lbl.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lbl.setWordWrap(True)
        self.lbl.setWindowFlag(Qt.FramelessWindowHint)
        self.lbl.setAttribute(Qt.WA_NoSystemBackground)
        self.lbl.setAttribute(Qt.WA_TranslucentBackground)
        self.lbl.setStyleSheet(f'color: black; font-size: {Global.label_font_size}px;')
        layout = QHBoxLayout(self)
        layout.addWidget(self.lbl, 0, Qt.AlignCenter)

        # Set policies.
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # Set button's style ( GUI representation ).
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.set_background_color(color)
        btn_size = Global.btn_size
        self.setMinimumSize(btn_size, btn_size)
        self.resize(btn_size, btn_size)
        if tooltip != '':
            self.setToolTip(tooltip)
        #QToolTip.setFont(QFont('SansSerif', 15))
        #QToolTip.setStyleSheet('background-color:rgb(241,234,167)')

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                           Getters/Setters                                #
    #                                                                          #
    ############################################################################

    def set_is_on_move(self, flag):
        self.__is_on_move = flag

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
                    1. If button is on 'move' mode:
                        1.1. get mouse 'x' and 'y' positions.
                        1.2. move button to position (x - 4, y - 45) 
                             (the constant numbers are for fixing the button location to be aligned to the mouse arrow).
                    2. Else, if one of the other existed buttons is on move:
                        1.1. invoke this method on the button that is on 'move' mode
    """

    def mouseMoveEvent(self, ev: QMouseEvent):
        if self.__is_on_move:
            x = (ev.windowPos().toPoint().x())
            y = (ev.windowPos().toPoint().y())
            self.move(x - 4, y - 35)

        elif Global.btn_on_move is not None:
            Global.btn_on_move.mouseMoveEvent(ev)

    """
    Function - mousePressEvent ( override function )
    
    Brief - method to invoke when mouse button has been clicked

    Parameters -    ev: QMouseEvent - mouse event parameters.

    Description - 
                    1. When left Button pressed:
                        1.1. If there isn't any button on 'move' mode, then invoke button's 'click' function
                        1.2. Else, emit 'stop_moving_event' signal 
                    2. When right button pressed:
                        2.1. If there isn't any button on 'move' mode, then invoke 'right menu'
                        2.2. Else, emit 'cancel_moving_event' signal
    """

    def mousePressEvent(self, ev: QMouseEvent):
        self.__mouse_curr_pos = ev
        if ev.button() == Qt.LeftButton:
            if Global.btn_on_move is None:

                if self.system_command.startswith('/usr/bin/'):
                    os.system(self.system_command)

                else:
                    os.write(3, bytes(self.system_command.encode()))
                super().mousePressEvent(ev)
            else:
                self.stop_moving_event.emit(self)
        elif ev.button() == Qt.RightButton:
            if Global.btn_on_move is None:
                self.right_menu()
            else:
                self.cancel_moving_event.emit(Global.btn_on_move)

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
        if Global.btn_on_move is None:
            # Create menu and menu buttons.
            menu = QMenu('Edit Options')
            move_action = QAction('Move Button', self, triggered=self.start_moving)
            color_action = QAction('Change Color', self, triggered=self.set_color)
            default_color_action = QAction('Set Default Color', self, triggered=self.set_default_color)
            remove_action = QAction('Remove Button', self, triggered=self.remove_button)
            rename_action = QAction('Rename Button', self, triggered=self.rename_button)
            change_procedure_action = QAction('Change Procedure', self, triggered=self.change_procedure)
            change_description_action = QAction('Change Description', self, triggered=self.change_description)
            add_to_user_section = QAction('Add To User Section', self, triggered=self.add_to_user_section)

            # Add menu buttons to the menu variable.
            if self.editable:
                menu.addAction(move_action)
                menu.addSeparator()
                menu.addAction(rename_action)
                menu.addAction(change_description_action)
                menu.addAction(change_procedure_action)
                menu.addSeparator()
                menu.addAction(remove_action)
                menu.addSeparator()
                menu.addAction(color_action)
                menu.addAction(default_color_action)
            elif self.tab_name == "Default":
                menu.addSeparator()
                menu.addAction(add_to_user_section)

            # Show menu.
            menu.exec_(QCursor.pos())

    def add_to_user_section(self):
        self.copy_btn_event.emit(self)


    """
        Function - rename_button

        Brief - Rename button name.

        Parameters -    NONE.
        """

    def rename_button(self):
        text, ok_pressed = QInputDialog.getText(QWidget(),
                                                'Rename button "' + self.lbl.text() + '"',
                                                "New Button Name",
                                                QLineEdit.Normal, self.title)
        if ok_pressed and text != '':
            self.title = text
            self.lbl.setText(text)
            self.save_button_event.emit(self)

    """
        Function - change_procedure

        Brief - Change button procedure.

        Parameters -    NONE.
        """

    def change_procedure(self):
        text, ok_pressed = QInputDialog.getText(QWidget(),
                                                'Change procedure for"' + self.lbl.text() + '"',
                                                "New Button Procedure",
                                                QLineEdit.Normal, self.system_command)
        if ok_pressed and text != '':
            self.system_command = text
            self.save_button_event.emit(self)

    """
        Function - change_procedure

        Brief - Change button procedure.

        Parameters -    NONE.
        """

    def change_description(self):
        text, ok_pressed = QInputDialog.getText(QWidget(),
                                                'Change procedure "' + self.lbl.text() + '"',
                                                "New Button Description",
                                                QLineEdit.Normal, self.description)
        if ok_pressed and text != '':
            self.description = text
            self.setToolTip(self.description)
            self.save_button_event.emit(self)

    """
        Function - set_color

        Brief - Set new background color.

        Parameters -    NONE.
        """

    def set_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_background_color(color.name())
            self.save_button_event.emit(self)

    """
        Function - set_color

        Brief - Set default background color ( light grey ).

        Parameters -    NONE.
        """

    def set_default_color(self):
        self.set_background_color(DEFAULT_BCK_COLOR)
        self.save_button_event.emit(self)

    """
        Function - remove_button

        Brief - remove and delete button, if user approve it.

        Parameters -    NONE.
        
        """

    def remove_button(self):
        ret = QMessageBox.question(QWidget(),
                                   'Remove Button',
                                   'Are you sure you want to delete button "' + self.lbl.text() + '" ?',
                                   QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.remove_button_event.emit(self)

    """
            Function - set_background_color

            Brief - Set button's background color.

            Parameters -    
                            color : str - color to set in background.

            """

    def set_background_color(self, color):
        self.current_color = color
        self.setStyleSheet(
            'QPushButton{ background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 white, stop: 0.7 '
            ''+color+', stop:1 white);'
            'border: 1px solid black;'  # outline
            'border-radius: ' + str(Global.btn_border) + 'px;}'  # corners
            'QPushButton::pressed{background-color:white;}'
            'QToolTip{ font-size:13px;background-color:rgb(241,234,167)}'

        )

    """
        Function - start_moving

        Brief - pre steps before button entered to 'move' mode.

        Parameters -    NONE.

        Description - 
                        1. Set buttons '__is_on_move' flag to True.
                        2. Enable button to track mouse operation ( move, press,...).
                        3. Emit 'start_moving_event' signal.
                        4. Invoke mouseMoveEvent method.
        """

    def start_moving(self):
        # Set buttons '__is_on_move' flag to True.
        self.__is_on_move = True

        # Enable button to track mouse operation ( move, press,...).
        self.setMouseTracking(True)

        # Emit 'start_moving_event' signal.
        self.start_moving_event.emit(self)

        # Invoke mouseMoveEvent method.
        self.mouseMoveEvent(self.__mouse_curr_pos)

    ############################################################################
    #                                                                          #
    #                                                                          #
    #                           Miscellaneous                                  #
    #                                                                          #
    ############################################################################

    def __str__(self):
        return 'Button(name={})'.format(self.lbl.text())

    def set_bold(self, to_bold):
        """
        Set Button name "bold" status
        :param to_bold: True if button font will be bold. False if not
        """
        font_weight = 'bold' if to_bold else 'normal'
        self.lbl.setStyleSheet(f'font-weight: {font_weight};color: black; font-size: {Global.label_font_size}px;')
