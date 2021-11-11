"""
Team Leaders Type
"""
exist_top_level_btns = ['Missing Vias RSF Fix DRC', 'Out of Boundary checker', 'Bumps Fixer']
tools_top_level_btns = {'PDE Release Archive':
                            ['sh("/p/mig_pde/cheetah/scripts/Projects_Release_Manager/PDE_Release_Archive.sh '
                             '/p/mig_pde/cheetah/scripts/Projects_Release_Manager/Application.py")',
                             'Add Project Release to Intel\'s archive']}

top_level_sections = {'Tool': tools_top_level_btns}

"""
Archive Type
"""
archive_btns = {'AP_M15 to AP_M17': ['REL_APM15_TO_APM17()', 'Changes all AP_M15 in level 0 to AP_M17'],
                'Metal Stack 15': ['MS15_Migration()', 'Executes the metal stack 15 migration automation'],
                'Metal Stack 17': ['MS17_Migration()', 'Executes the metal stack 17 migration automation'],
                'Find VIA13 in Hierarchy': ['CCSFindUniqueCellNames()', 'Detect VIA13 in cell hier'],
                'WSP Pwr and Gnd': ['MISetSigType(\'("power" "ground"))', 'Set power and ground for active metal WSPs'],
                'WSP No_Wire': ['MISetSigType(\'("No Wiretype"))', 'Set WPS on active metals to No Wiretype'],
                'WSP Show_All': ['MISetSigType(nil)', 'Show all WSP types, no filtering'],
                }

archive_sections = {'Archive': archive_btns}

'''
All tabs
'''
tab_types_custom = {"Top Level": top_level_sections, 'Archive': archive_sections}
tab_types_exists_buttons = {'Top Level': exist_top_level_btns}

'''
Tooltip dictionary
'''
tab_types_extra_info = {'Top Level': {'TEST': {'tooltip': 'Tools for Top level users'}},
                        'Archive': {'Archive': {'tooltip': 'Old tools and actions that are no longer in need'}}
                        }
