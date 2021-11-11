"""
defaultF10

This file holds all the default F10 buttons for "Data" "Tool" and "Misc" sections


"""

general_buttons = {'LoadAll': ['load(strcat(IfxKifBlkProps->path "/cdn/env/loadall.il"))', 'MIG Aces Loadall tool'],
                   'N5 Workflow': ['/usr/bin/firefox https://wiki.ith.intel.com/x/GdHCaw &','Open N5 Workflow in Wiki']}

data_buttons = {'Hierarchy Copy': ['GGHierCopyRenameMain()', 'Hierarchy Copy and Rename'],

                'Bindkey Wiki': ['/usr/bin/firefox https://wiki.ith.intel.com/display/PDMO/Virtuoso+Bind+keys &',
                                'open Virtuoso Bindkey Wiki'],
                'HV terms Report': ['hvtermReport()', 'Creating HV terms report form CDL'],
                'Layout Note': ['Layout_Note()', 'Open the Layout Note GUI'],
                'Data Base Naming Validation': ['Check_Validity()', 'Verifies the validity of cells in the hierarchy'],
                }

tool_buttons = {'Tap LUP check': ['ESDLUP_RSFfix()', 'Update RSF for ESD LUP Run, to be used on majority check.'],
                'Missing Vias RSF Fix DRC': ['MissingViasRSFFixM17()', 'Custom DRC runset that checks: missing vias, '
                                                                       'pin coming out of its drawing, min size of '
                                                                       'via1-4 on wider metal'],
                'Out of Boundary checker': ['ShapesOutOfPRB()',
                                            'Checks if any shapes are sitting outsidef the cell\'s PrBoundary'],
                'Instances Net Relations': ['RELInstRelationsGUI()',
                                            'opens a GUI showing all the net-relations in current Schematic View, '
                                            'allows excel output.'],
                'Shared Nets': ['SharedNets()',
                                'In Schematic View: Shows net relations between 2 instances,'
                                ' allows excel output, bus drawing.'],
                'DRC Boundary Checker': ['RELPreDRCFlow()',
                                         'Runs a Pre DRC Flow boundary check, Applies rules 1 & 6, and checks rule 2'],
                'Revert Boundary Status': ['RELPostDRCFlow()',
                                           'Runs a Post DRC Flow, Removes Fill, suggests GR removing, if the GR is '
                                           'removed applies rules 1 & 6.'],
                'HP Surround Cells': ['RELHPSurr()', 'Generating HP GR Cells by selecting the relevant MAIN cells'],
                'HD Surround Cells': ['RELHDSurr()', 'Generating HD GR Cells by selecting the relevant MAIN cells'],
                'Delete Redundant Cells': ['GGFindDeleteRedundantCells()', 'Find Redundant Cells and delete them'],
                'Rule Check to CSV': ['/usr/bin/xterm -T \"Rule Check to CSV\" '
                                      '-e \"echo /p/mig_pde/cheetah/scripts/RELRuleCheck2Csv.py;'
                                      '/p/mig_pde/cheetah/scripts/RELRuleCheck2Csv.py ;tcsh\" &',
                                      '<nobr>Convert rule checks to CSV files.</nobr>'
                                      '<br>NOTE:Xterm will be raised to enter '
                                      'the command with your needed arguments.'],
                'Flatten & Uniquify': ['/usr/bin/xterm -T \"Flatten & Uniquify\" '
                                       '-e \"echo $PROJ_TOOLS/dsa_utils/latest/lv_utils/fu.pl;'
                                       '$PROJ_TOOLS/dsa_utils/latest/lv_utils/fu.pl ;tcsh\" &',
                                       '<nobr>Flatten and uniquify files.</nobr>'
                                       '<br>NOTE:Xterm will be raised to enter '
                                       'the command with your needed arguments.'],
                'Abstract': ['/usr/bin/xterm -T \"Abstract\" -e \"cd $WORKAREA;abstract &;'
                             '/usr/bin/firefox https://wiki.ith.intel.com/x/_9DDb &;tcsh\" &',
                             'Open Abstract GUI in new Xterm + Open Abstract Wiki Page'],
                'Pins Manager': ['RELComparePins()', 'Pin management tool'],
                'Grow Path': ['GGFindWiresSelectBbox()', 'Extends wires from Sub-Cells'],
                'Fast Fill': ['_AAMetalFillMenu()', 'Fast fill base on Active WSP'],

                'Trace and save nets': ['ORTraceAndSaveNets()', 'Trace, Mark And Save nets'],
                'Advanced Tree': ['RELAdvTree()', 'a GUI for the advanced tree tool.'],
                'Push Pop': ['push_pop_route_form_display()',
                             'Pushing and Poping (Promoting) routes to Down/Up/Top levels.'],
                'XOR CellView': ['cv_compare()', 'Utility that compare 2 layouts or OAS files'],

                'Bumps Fixer': ['displayBumpsFixer()',
                                'Fixed pins & labels at the top label according to the Bump CellView'],
                'Net Resistance Calculator': ['netResistanceCalculatorGUI()',
                                              'a tool that calculates resistance and IDC Max in Layout or manually.'],
                'Simple Route': ['simpleRoute()', 'Create wires to connect between 2 wires in the same net.'],
                'Remove Floating Nets': ['RELDeleteFloaters()', 'Removes floating nets'],
                'OneLV GUI': ['OneLV()', 'OneLV GUI']
                }

misc_buttons = {'Open Original F10': ['RELSideMenu()', 'Open the original F10'],
                'Create pin from Sch': ['pushWireToLayoutPin()', 'Create pin from Sch'],
                'Pin and Label Rename': ['RELPinRenaming()', 'Finds and replaces text in selected pins and labels'],
                'Promote Pins': ['MERPromotePinsToTopGUI()', 'Toggle Snapping method'],
                'Toggle Solid': ['toggle()', 'Toggle layer to solid color'],
                'Save Positioning': ['saveWindowsPositions()',
                                     'Saves the current windows (CIW, Schematic, Layout) positioning in home dir'],
                'Delete All Markers': ['geDeleteAllMarker(geGetEditCellView() nil nil nil)',
                                       'Delete all markers from CellView'],
                'Toggle fb1 grid visibility': ['pteSetVisible("Grids;Snap Patterns;Local Grids;fb1" !pteIsVisible('
                                               '"Grids;Snap Patterns;Local Grids;fb1" "Grids") "Grids")',
                                               'Toggles the visibility of the fb1 grid'],
                'Check color': ['preSaveTrigger(geGetEditCellView()', 'Check color'],
                'Toggle mid ruler': ['envSetVal("graphic" "displayRulerMiddlePoint" \'boolean !envGetVal("graphic" '
                                     '"displayRulerMiddlePoint\"))', 'Toggle state of mid ruler measure'],

                'Remove markers of CO cells': ['RELRemoveCheckedOutMarkers()',
                                               'Removes all markers your checkout cells'],
                'Quick Oasis Export': ['RELOasis()',
                                       'Runs a quick Oasis export - with an option to ignore missing cells.'],
                'Zoom to Coordinate': ['GGZoomToCoord()', 'Zoom to Coordinates'],
                'Remove Ghosts': ['ABremoveGhosts()', 'Remove steiners/routs Ghosts'],
                'Real time on off toggle': ['mgc_calibre_realtime_set_option("RealTimeEnabled" '
                                            '!mgc_calibre_realtime_get_option("RealTimeEnabled"))',
                                            '!mgc_calibre_realtime_get_option("RealTimeEnabled"))',
                                            'Toggle the real time Calibre menu'],
                'Toggle WSP': ['pteSetVisible("Grids;Snap Patterns;Width Spacing Grids" !pteIsVisible("Grids;Snap '
                               'Patterns;Width Spacing Grids" "Grids") "Grids")',
                               'Toggles the visibility of the WSP Grids'],

                'Add Drawings to Pins': ['RELAddPinDrawings()', 'Add a Pin Drawing on every pin with purpose pin.'],

                'Full Color Check': ['FullColorCheck()', 'Runs a full color check on level 0. Unlocks All -> Updates '
                                                         'Colors -> Locks All'],
                'Delete Rulers': ['leHiClearMeasurementInHier()', 'Hierarchical delete rulers from memory'],
                'Bring back CIW': ['BringBackCIW()', 'Bring back CIW'], }

default_buttons_dict = {' ': {'tooltip': '', 'buttons': general_buttons, 'color': "#A569BD"},
                        'Data': {'tooltip': 'Scripts for getting information', 'buttons': data_buttons,
                                 'color': "#EB984E"},
                        'Misc': {'tooltip': 'CAD made tools', 'buttons': misc_buttons, 'color': "#2980B9"},
                        'Tool': {'tooltip': 'Cadence made tools.', 'buttons': tool_buttons, 'color': "#2ECC71"}}
