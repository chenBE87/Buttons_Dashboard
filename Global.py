import sys
import os
import _pickle as pickle


"""
Globals
---------------
Contains global variables
"""

btn_on_move = None
btn_section = None
btn_index = None
number_of_btn_in_row = None
all_buttons_dict = None
max_btn_in_row = None
REBOOT_CODE = None
screen_height = 0
default_buttons_descriptions = None
tab_types_custom = None
tab_types_exists_buttons = None
label_font_size = None
bold_all_btns = None
btn_size = None
btn_border = None
btn_font_size = None
btn_size_attributes = None
btn_width = None
btn_height = None
path_to_save = ""
path_to_additional_files = ""

"""
Function - init_shared_globals

Brief - Initiate global variables.

"""


def init_shared_globals(default_f10_path: str):
    """
    Initiate shared global variables
    :param default_f10_path: path to files with information to set in the tool
    """
    global btn_on_move
    global btn_section
    global btn_index
    global number_of_btn_in_row
    global all_buttons_dict
    global max_btn_in_row
    global REBOOT_CODE
    global screen_height
    global tab_types_custom
    global tab_types_exists_buttons
    global label_font_size
    global bold_all_btns
    global btn_size
    global btn_border
    global btn_width
    global btn_size_attributes
    global btn_height
    global path_to_save
    global path_to_additional_files

    path_to_save = f'{os.getenv("WORKAREA")}/F10'
    if not os.path.isdir(path_to_save):
        os.system(f'mkdir {path_to_save}')
    path_to_additional_files = default_f10_path
    btn_size_attributes = {65: {'border': 27, 'font-size': 8, 'width factor': 75, 'height factor': 70},
                           66: {'border': 27, 'font-size': 8, 'width factor': 76, 'height factor': 70},
                           67: {'border': 27, 'font-size': 8, 'width factor': 79, 'height factor': 70},
                           68: {'border': 28, 'font-size': 8, 'width factor': 80, 'height factor': 70},
                           69: {'border': 28, 'font-size': 8, 'width factor': 81, 'height factor': 70},
                           70: {'border': 28, 'font-size': 8, 'width factor': 82, 'height factor': 70},
                           71: {'border': 29, 'font-size': 9, 'width factor': 83, 'height factor': 70},
                           72: {'border': 29, 'font-size': 10, 'width factor': 85, 'height factor': 70},
                           73: {'border': 29, 'font-size': 10, 'width factor': 86, 'height factor': 70},
                           74: {'border': 30, 'font-size': 10, 'width factor': 89, 'height factor': 70},
                           75: {'border': 30, 'font-size': 10, 'width factor': 90, 'height factor': 70},
                           76: {'border': 30, 'font-size': 10, 'width factor': 90, 'height factor': 70},
                           77: {'border': 30, 'font-size': 10, 'width factor': 91, 'height factor': 70},
                           78: {'border': 32, 'font-size': 10, 'width factor': 92, 'height factor': 70},
                           79: {'border': 32, 'font-size': 11, 'width factor': 93, 'height factor': 70},
                           80: {'border': 32, 'font-size': 11, 'width factor': 94, 'height factor': 70},
                           81: {'border': 32, 'font-size': 11, 'width factor': 95, 'height factor': 70},
                           82: {'border': 33, 'font-size': 11, 'width factor': 97, 'height factor': 70},
                           83: {'border': 33, 'font-size': 12, 'width factor': 98, 'height factor': 70},
                           84: {'border': 33, 'font-size': 12, 'width factor': 99, 'height factor': 70},
                           85: {'border': 34, 'font-size': 12, 'width factor': 101, 'height factor': 70},
                           86: {'border': 34, 'font-size': 12, 'width factor': 102, 'height factor': 70},
                           87: {'border': 34, 'font-size': 12, 'width factor': 103, 'height factor': 70},
                           88: {'border': 35, 'font-size': 12, 'width factor': 104, 'height factor': 70},
                           89: {'border': 35, 'font-size': 12, 'width factor': 105, 'height factor': 70},
                           90: {'border': 35, 'font-size': 12, 'width factor': 107, 'height factor': 70},
                           91: {'border': 36, 'font-size': 13, 'width factor': 108, 'height factor': 70},
                           92: {'border': 36, 'font-size': 13, 'width factor': 109, 'height factor': 70},
                           93: {'border': 36, 'font-size': 13, 'width factor': 110, 'height factor': 70},
                           94: {'border': 36, 'font-size': 13, 'width factor': 111, 'height factor': 70},
                           95: {'border': 37, 'font-size': 13, 'width factor': 112, 'height factor': 70},
                           }

    screen_height = 0
    REBOOT_CODE = -321
    btn_size = 70
    label_font_size = btn_size_attributes[btn_size]['font-size']
    btn_border = btn_size_attributes[btn_size]['border']
    btn_width = btn_size_attributes[btn_size]['width factor']
    btn_height = btn_size_attributes[btn_size]['height factor']
    bold_all_btns = False
    btn_on_move = None
    btn_section = None
    btn_index = None
    number_of_btn_in_row = 5
    sys.path.insert(0, default_f10_path)
    import defaultF10
    all_buttons_dict = defaultF10.default_buttons_dict
    file = f'{path_to_save}/Side_Menu_Config.pickle'
    if os.path.isfile(file):
        with open(file, "rb") as f:
            config_dict = pickle.load(f)
            if 'NUM_OF_BUTTONS' in config_dict.keys():
                number_of_btn_in_row = config_dict['NUM_OF_BUTTONS']
            if 'BOLD_BTNS' in config_dict.keys():
                bold_all_btns = config_dict['BOLD_BTNS']
            if 'BTNS_SIZE' in config_dict.keys():
                btn_size = config_dict['BTNS_SIZE']
                label_font_size = btn_size_attributes[btn_size]['font-size']
                btn_border = btn_size_attributes[btn_size]['border']
                btn_width = btn_size_attributes[btn_size]['width factor']
                btn_height = btn_size_attributes[btn_size]['height factor']


def save_configurations():
    global number_of_btn_in_row
    global bold_all_btns
    global btn_size
    global btn_size_attributes
    file = f'{path_to_save}/Side_Menu_Config.pickle'
    config_dict = {'NUM_OF_BUTTONS': number_of_btn_in_row, 'BOLD_BTNS': bold_all_btns, 'BTNS_SIZE': btn_size}
    if not os.path.exists(file):
        os.system(f' touch {file}')
    with open(os.path.expanduser(file), "wb") as f:
        pickle.dump(config_dict, f)


