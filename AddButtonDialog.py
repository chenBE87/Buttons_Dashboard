from PyQt5.QtWidgets import QVBoxLayout, QLabel, QListWidget, QAbstractItemView, QDialogButtonBox, QDialog, QLineEdit, \
    QHBoxLayout, QRadioButton, QButtonGroup, QMessageBox
from PyQt5.QtCore import Qt
import Global


class AddButtonDialog(QDialog):
    """
    AddButtonDialog
   ---------------
    Dialog window for adding new button
    """

    # Class constants
    NEW_BTN_INDEX = 1
    EXIST_BTN_INDEX = 2

    """
    Function - __init__ ( Constructor )

    Brief - init window display and functionality.

    Parameters - 
                    items    : list          - list of default buttons
                    editable : section_title - section title, which the button will be added.
                    parent   : Qwidget       - window's responsible widget ( default = None ).

    Description - 
                    1. Initiate main layout and variables.
                    2. Create the radio buttons. set "Checked" the first button.
                    3. Set the radio buttons group.
                    4. Set the widgets for the "Select from exist" option.
                    5. Set the widgets for the "Select from new" option.
                    6. Set the Dialog window's buttons.
                    7. Organize the widget in the window.
                    8. Display the "Select from exist" widgets.
                    9. Set window's style ( GUI representation ).
                    10. Connect dialog buttons to method.
    """

    def __init__(self, section_title, parent=None):
        super().__init__(parent)

        # Initiate main layout and variables.
        self.output_variables_list = None
        self.section_title = section_title
        self.default_btns = {}
        for title in Global.all_buttons_dict.keys():
            for key, val in Global.all_buttons_dict[title]['buttons'].items():
                self.default_btns[key] = val
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignTop)

        # Create the radio buttons. set "Checked" the first button.
        self.radio_btn_exist = QRadioButton("Select from existing buttons")
        self.radio_btn_exist.setChecked(True)

        self.radio_btn_new = QRadioButton("Create new button")

        # Set the radio buttons group.
        self.radio_btn_layout = QHBoxLayout()
        self.radio_btn_layout.addWidget(self.radio_btn_exist)
        self.radio_btn_layout.addWidget(self.radio_btn_new)

        self.radio_btn_group = QButtonGroup(self)
        self.radio_btn_group.addButton(self.radio_btn_exist, self.EXIST_BTN_INDEX)
        self.radio_btn_group.addButton(self.radio_btn_new, self.NEW_BTN_INDEX)
        self.radio_btn_group.buttonClicked[int].connect(self.radio_btn_selected)

        # Set the widgets for the "Select from exist" option.
        self.exist_btn_lbl = QLabel('Select button for section {} :'.format(section_title))

        self.variable_list = QListWidget()
        self.variable_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.variable_list.addItems(self.default_btns.keys())
        self.variable_list.clicked.connect(self.display_btn_description)

        self.descLabel = QLabel('Button\'s description: ')
        self.funcDesc = QLineEdit('')
        self.funcDesc.setReadOnly(True)

        self.btn_desc_set = QHBoxLayout()
        self.btn_desc_set.addWidget(self.descLabel)
        self.btn_desc_set.addWidget(self.funcDesc)

        # Set the widgets for the "Select from new" option.
        self.new_btn_lbl = QLabel('Create new button for section {} :'.format(section_title))

        self.new_btn_name_set = QHBoxLayout()
        self.new_btn_name_lbl = QLabel('New button\'s name: ')
        self.new_btn_name_input = QLineEdit('')
        self.new_btn_name_set.addWidget(self.new_btn_name_lbl)
        self.new_btn_name_set.addWidget(self.new_btn_name_input)

        self.new_btn_proc_set = QHBoxLayout()
        self.new_btn_proc_lbl = QLabel('New button\'s procedure: ')
        self.new_btn_proc_input = QLineEdit('')
        self.new_btn_proc_set.addWidget(self.new_btn_proc_lbl)
        self.new_btn_proc_set.addWidget(self.new_btn_proc_input)

        self.new_btn_desc_set = QHBoxLayout()
        self.new_btn_desc_lbl = QLabel('New button\'s description: ')
        self.new_btn_desc_input = QLineEdit('')
        self.new_btn_desc_set.addWidget(self.new_btn_desc_lbl)
        self.new_btn_desc_set.addWidget(self.new_btn_desc_input)

        # Set the Dialog window's buttons.
        dialog_button = QDialogButtonBox()
        dialog_button.setOrientation(Qt.Horizontal)
        dialog_button.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        # Organize the widget in the window.
        lay.addLayout(self.radio_btn_layout)
        lay.addWidget(self.exist_btn_lbl)
        lay.addWidget(self.variable_list)
        lay.addLayout(self.btn_desc_set)
        lay.addWidget(self.new_btn_lbl)
        lay.addLayout(self.new_btn_name_set)
        lay.addLayout(self.new_btn_desc_set)
        lay.addLayout(self.new_btn_proc_set)
        lay.addWidget(dialog_button)

        # Display the "Select from exist" widgets.
        self.set_new_btn_visible_status(False)

        # Set window's style ( GUI representation ).
        self.resize(self.width() + 50, self.height())
        self.setWindowTitle("Add New Button")

        # Connect dialog buttons to method.
        dialog_button.accepted.connect(self.accept)
        dialog_button.rejected.connect(self.reject)

    """
    Function - accept ( Override )

    Brief - Callback for the "accept" button. The accept will send the variables for creating the new button.

    Description - 
                    1. If the user is in the "Select from exist" option:
                        1.1. if the user didn't choose button from list, a warning message will be displayed.
                        1.2. Else, list of variables will be sent 
                             ( list = [selected_radio_button_index, new_button_name, 
                                       new_button_procedure, new_button_description]
                             ).
                    2. Else:
                        2.1. If one of the string field, that uer needs to 
                             fill, is empty, a warning message will be displayed.
                        2.2. Else, list of variables will be sent 
                             ( list = [selected_radio_button_index, new_button_name, 
                                       new_button_procedure, new_button_description]
                             ).
    """

    def accept(self):
        if self.radio_btn_group.checkedId() == self.EXIST_BTN_INDEX:
            #self.output_variables_list = [item.text() for item in self.variable_list.selectedItems()]
            if len(self.variable_list.selectedItems()) == 0:
                QMessageBox.warning(self, 'Button not selected', 'No button has been selected !')
            else:
                #self.output_variables_list.insert(0, self.EXIST_BTN_INDEX)
                title = self.variable_list.selectedItems()[0].text()
                command = desc = ''
                for section in Global.all_buttons_dict.keys():
                    if title in Global.all_buttons_dict[section]['buttons'].keys():
                        command = Global.all_buttons_dict[section]['buttons'][title][0]
                        desc = Global.all_buttons_dict[section]['buttons'][title][1]
                        break
                self.output_variables_list = [self.EXIST_BTN_INDEX, title, command, desc]
        else:
            if self.new_btn_desc_input.text() == '' or self.new_btn_name_input.text() == '' \
                                                    or self.new_btn_proc_input.text() == '':
                QMessageBox.warning(self, 'Button not selected', 'Please fill all fields for creating new button !')
            else:
                self.output_variables_list = [self.NEW_BTN_INDEX, self.new_btn_name_input.text(),
                                              self.new_btn_proc_input.text(), self.new_btn_desc_input.text()]
        super().accept()  # <-- call parent method

    """
    Function - display_btn_description

    Brief - Callback that is invoked when selected item in the "Select From Exist" option's list changed.

    Description - 
                    1. The method will display the description of the selected button from list in "Function Description"
                       field list.
    """
    def display_btn_description(self):
        self.funcDesc.setText(self.default_btns[self.variable_list.selectedItems()[0].text()][1])

    """
    Function - radio_btn_selected

    Brief - Callback that is invoked when radio button has been selected.
    
    Parameters  -  
                    btn_id: int - selected button ID

    Description - 
                    1. The method will switch between window's options, according to the input button id:
                        1.1. "Select from exist" option.
                        1.2. "Select from new" option.
    """
    def radio_btn_selected(self, btn_id):
        set_new_visible = True
        if btn_id != self.NEW_BTN_INDEX:
            set_new_visible = False
        self.set_new_btn_visible_status(set_new_visible)
        self.set_existing_btn_visible_status(not set_new_visible)

    """
    Function - set_new_btn_visible_status

    Brief - Set visible attribute for "Select from new" option widget 

    Parameters  -  
                    status: bool - value to assign tp the setVisible method

    """
    def set_new_btn_visible_status(self, status):
        self.new_btn_lbl.setVisible(status)
        self.new_btn_name_input.setVisible(status)
        self.new_btn_name_lbl.setVisible(status)
        self.new_btn_proc_input.setVisible(status)
        self.new_btn_proc_lbl.setVisible(status)
        self.new_btn_desc_lbl.setVisible(status)
        self.new_btn_desc_input.setVisible(status)

    """
    Function - set_existing_btn_visible_status

    Brief - Set visible attribute for "Select from exist" option widget 

    Parameters  -  
                    status: bool - value to assign tp the setVisible method

    """
    def set_existing_btn_visible_status(self, status):
        self.exist_btn_lbl.setVisible(status)
        self.variable_list.setVisible(status)
        self.descLabel.setVisible(status)
        self.funcDesc.setVisible(status)
