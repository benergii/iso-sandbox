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
interaction_cell = None

# ------------- HUD ------------- #

# Top bar boxes
hud_icon_x = 0.07
hud_icon_y = hud_icon_x * window_x / window_y

# Actual HUD button array
hud_buttons = build_hud(['terraform', 'constructPath'])

# Dictate which 'mode' the user is in
user_data = {
  'mode': None
}

# Popup windows stored in a dict as well (for now)

popup_definition = [
  {
    'name': 'constructPath',
    'buttons': [
      'left',
      'straight',
      'right'
    ]
  }, {
    'name': 'terraform',
    'buttons': [
      'increase',
      'decrease',
    ]
  }
]

popup_windows = build_popup_windows(popup_definition)

# ------- TESTING OBJECT MOVEMENT ------- #
objects = []



# ----------------------------------- CONSTRUCTION -----------------------------------
# NB: Might be able to get away w not putting this in the Config, but doing so for now

construction_cell = None