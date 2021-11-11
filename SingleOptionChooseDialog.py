from PyQt5.QtWidgets import QVBoxLayout, QLabel, QListWidget, QAbstractItemView, QDialogButtonBox, QDialog, \
    QMessageBox
from PyQt5.QtCore import Qt


class SingleOptionChooseDialog(QDialog):
    """
    SingleOptionChooseDialog
   ---------------
    Dialog window for for choosing one item from list
    """

    """
    Function - __init__ ( Constructor )

    Brief - init window display and functionality.

    Parameters - 
                    items    : list          - list of option to choose from
                    parent   : Qwidget       - window's responsible widget ( default = None ).

    Description - 
                    1. Initiate main layout and variables.
                    2. Create List of direction.
                    3. Set the Dialog window's buttons.
                    4. Organize the widget in the window.
                    6. Connect dialog buttons to method.
    """
    def __init__(self, items, parent=None):
        super().__init__(parent)
        # Initiate main layout and variables.
        self.scatter_variable = None
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignTop)

        # Create List of direction.
        self.title_lbl = QLabel('')
        self.variable_list = QListWidget()
        self.variable_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.variable_list.addItems(items)
        self.variable_list.setCurrentRow(0)

        # Set the Dialog window's buttons.
        dialog_button = QDialogButtonBox()
        dialog_button.setOrientation(Qt.Horizontal)
        dialog_button.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        # Organize the widget in the window.
        lay.addWidget(self.title_lbl)
        lay.addWidget(self.variable_list)
        lay.addWidget(dialog_button)

        # Set window's style ( GUI representation ).
        # self.setWindowTitle('Move Section "' + section_title + '"')

        # Connect dialog buttons to method.
        dialog_button.accepted.connect(self.accept)
        dialog_button.rejected.connect(self.reject)


class MoveSectionDialog(SingleOptionChooseDialog):
    """
    MoveSectionDialog
   ---------------
    Dialog window for moving sections in tab
    """

    """
    Function - __init__ ( Constructor )

    Brief - init window display and functionality.

    Parameters - 
                    items         : list          - list of directions ( Up, Down, First, Last )
                    section_title : str - section title, which suppose to be moved.
                    parent        : Qwidget       - window's responsible widget ( default = None ).

    Description - 
                    1. Call "father" class init
                    2. Set label's string
                    3. Set window's style ( GUI representation ).
    """
    def __init__(self, items, section_title="", parent=None):
        super().__init__(items, parent)

        # Create List of direction.
        self.title_lbl.setText('Choose move option:')

        # Set window's style ( GUI representation ).
        self.setWindowTitle('Move Section "' + section_title + '"')

    def accept(self):
        self.scatter_variable = [item.text() for item in self.variable_list.selectedItems()]
        if not self.scatter_variable:
            QMessageBox.warning(self, 'Destination not selected', 'Please choose move destination !')
        else:
            super().accept()  # <-- call parent method


class ChooseSection(SingleOptionChooseDialog):
    """
    ChooseSection
   ---------------
    Dialog window for choosing section on "User" tab , for adding the copied button
    """

    """
    Function - __init__ ( Constructor )

    Brief - init window display and functionality.

    Parameters - 
                    items     : list          - list of all "User" sections
                    btn_title : str     - copied button's name.
                    parent    : Qwidget       - window's responsible widget ( default = None ).

    Description - 
                   1. Call "father" class init
                   2. Set label's string
                   3. Set window's style ( GUI representation ).
   """
    def __init__(self, items, btn_title="", parent=None):
        super().__init__(items, parent)

        # Create List of direction.
        self.title_lbl.setText(f'Choose a section from "User" tab, to move in button "{btn_title}":')

        # Set window's style ( GUI representation ).
        self.setWindowTitle(f'Copy button {btn_title} to section')

    def accept(self):
        self.scatter_variable = [item.text() for item in self.variable_list.selectedItems()]
        if not self.scatter_variable:
            QMessageBox.warning(self, 'Section not selected', 'Please choose section !')
        else:
            super().accept()  # <-- call parent method


class ChooseTabType(SingleOptionChooseDialog):
    """
    ChooseTabType
   ---------------
    Dialog window for choosing tab type, for init the new tab
    """

    """
    Function - __init__ ( Constructor )

    Brief - init window display and functionality.

    Parameters - 
                    items    : list    - list of init tab types.
                    tab_title: str     - created tab title.
                    parent   : Qwidget - window's responsible widget ( default = None ).

    Description - 
                    1. Call "father" class init
                    2. Set label's string
                    3. Set window's style ( GUI representation ).
    """
    def __init__(self, items, tab_title="", parent=None):
        super().__init__(items, parent)

        # Create List of direction.
        self.title_lbl.setText(f'Choose how to initiate the new tab "{tab_title}":')

        # Set window's style ( GUI representation ).
        self.setWindowTitle(f'Initiate tab {tab_title}')

    def accept(self):
        self.scatter_variable = [item.text() for item in self.variable_list.selectedItems()]
        if not self.scatter_variable:
            QMessageBox.warning(self, 'Tab type not selected', 'Please choose one !')
        else:
            super().accept()  # <-- call parent method


class RemoveTabType(ChooseTabType):
    """
       ChooseTabType
      ---------------
       Dialog window for choosing tab to remove
    """

    def __init__(self, items, parent=None):
        super().__init__(items, parent)

        # Create List of direction.
        self.title_lbl.setText(f'Choose tab to remove:')

        # Set window's style ( GUI representation ).
        self.setWindowTitle(f'Remove tab')


class ChooseRemoveTab(SingleOptionChooseDialog):
    """
    ChooseTabType
   ---------------
    Dialog window for choosing tab type, for init the new tab
    """

    """
    Function - __init__ ( Constructor )

    Brief - init window display and functionality.

    Parameters - 
                    items    : list    - list of init tab types.
                    tab_title: str     - created tab title.
                    parent   : Qwidget - window's responsible widget ( default = None ).

    Description - 
                    1. Call "father" class init
                    2. Set label's string
                    3. Set window's style ( GUI representation ).
    """
    def __init__(self, items, parent=None):
        super().__init__(items, parent)

        # Create List of direction.
        self.title_lbl.setText(f'Choose Tab to remove:')

        # Set window's style ( GUI representation ).
        self.setWindowTitle(f'Remove Tab')

    def accept(self):
        self.scatter_variable = [item.text() for item in self.variable_list.selectedItems()]
        if not self.scatter_variable:
            QMessageBox.warning(self, 'Tab type not selected', 'Please choose one !')
        else:
            super().accept()  # <-- call parent method