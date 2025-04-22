from functions.build_objects import (
  build_iso_gameboard,
  build_hud,
  build_popup_windows
)

# BRAND NEW PATTER JUST DROPPED
# STORE ALL YOUR CONSTANTS IN THIS CONFIG FILE
# THAT WAY YOU CAN LOAD THEM INTO ANY FUNCTION FILE YOU LIKE

window_x = 1024
window_y = 768
unit_width = 0.4
gameboard_dimensions = [11, 11]

# Unit height needs to correspond with the iso-transformed unit width
unit_height = (unit_width ** 2) * (2 / 6)

# ASSUMING ALL GAME BOARDS ARE SQUARE FOR NOW - CAMERA OFFSET IS JUST UNIT HEIGHT x X DIMENSION
# UNIT HEIGHT ADDED IN RENDER PHASE
camera_offset = [0, -1 * gameboard_dimensions[0] * unit_height]

# Rotation integer ranges from 0-3 and tells the game which sprites to render
rotation_integer = 0

# ------------ CELLS ------------ #

# BUILDING THE GAMEBOARD, and the order to render the gameboard in
gameboard, cell_render_order = build_iso_gameboard()

# Empty variable to store the value of the cell we are interacting with
interaction_cells = []

# ------------- HUD ------------- #

# Top bar boxes
hud_icon_x = 0.07
hud_icon_y = hud_icon_x * window_x / window_y

# Actual HUD button array
hud_buttons = build_hud(['terraform', 'construct_path'])

# Dictate which 'mode' the user is in
user_data = {
  'mode': None
}

# Popup windows stored in a dict as well (for now)

popup_definition = [
  {
    'name': 'construct_path',
    'buttons': [
      [
        'left',
        'straight',
        'right'
      ], [
        'downSteep',
        'down',
        'up',
        'upSteep'
      ], [
        'delete'
      ]
    ]
  }, {
    'name': 'terraform',
    'buttons': [
      [
        'decrease',
        'increase',
      ]
    ]
  }
]

popup_windows = build_popup_windows(popup_definition)

# ------- TESTING OBJECT MOVEMENT ------- #
objects = []



# ----------------------------------- CONSTRUCTION -----------------------------------
# NB: Might be able to get away w not putting this in the Config, but doing so for now
# UPDATE: CANT GET AWAY WITH NOT PUTTING IT IN THE CONFIG - AS NEED TO ROTATE PATH COORDS WITH CAMERA ROTATION

construction_cell = None
temp_cells_constructed_on = []
temp_path = []
temp_height = []
can_you_build_here = True




# TESTING SHIT

terraform_scalar = 0