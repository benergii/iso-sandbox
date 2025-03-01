from functions.iso_gameboard import build_iso_gameboard

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

# BUILDING THE GAMEBOARD
gameboard = build_iso_gameboard()