from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from random import randint

from .tools import iso_translater

# LOADING IN ALL OUR SETUP VARIABLES
import config

# Building a list of dictionaries for iso game board
def build_iso_gameboard():

  # JUST SOME COLOURS TO MAKE IT ALL A BIT NICER TO LOOK AT
  gameboard_colors = [
    (0.7, 0.9, 0.7),
    (0.6, 0.85, 0.6),
    (0.75, 0.92, 0.75),
    (0.68, 0.88, 0.68),
    (0.72, 0.93, 0.72),
    (0.65, 0.87, 0.65),
    (0.78, 0.95, 0.78),
    (0.7, 0.89, 0.7),
    (0.62, 0.84, 0.62),
    (0.74, 0.91, 0.74),
]

  # PLEASE BE AWARE: GAMEBOARDS WITH ODD TOTAL AREAS WORK BEST
  # IE 11 x 11 vs 10 x 10

  board_x = config.gameboard_dimensions[0]
  board_y = config.gameboard_dimensions[1]

  cells = {}

  for x in range(board_x):
    for y in range(board_y):
      
      v1_x, v1_y = iso_translater(x, y)
      v2_x, v2_y = iso_translater(x + 1, y)
      v3_x, v3_y = iso_translater(x + 1, y + 1)
      v4_x, v4_y = iso_translater(x, y + 1)

      cells[(x, y)] = {
        'v0': [v1_x, v1_y],
        'v1': [v2_x, v2_y],
        'v2': [v3_x, v3_y],
        'v3': [v4_x, v4_y],
        'height': config.unit_height,
        'color': gameboard_colors[randint(0, len(gameboard_colors) - 1)],
        'objectOnCell': None,
        'objectHeight': None
      }

  # Now return the cells dictionary, as well as the list in which to render the cells
  # Might change this method in the near future but for now this be how we doing this
  return cells, list(reversed(cells.keys()))


# Building a dictionary for the HUD buttons, based on a list of button names

def build_hud(button_names):

  button_dict = {}

  for n in range(len(button_names)):

    x_pos = config.hud_icon_x * n

    button_dict[button_names[n]] = {
      'buttonName': button_names[n],
      'v0': (-1 + x_pos, 1 - config.hud_icon_y),
      'v1': (-1 + x_pos + config.hud_icon_x, 1 - config.hud_icon_y),
      'v2': (-1 + x_pos + config.hud_icon_x, 1),
      'v3': (-1 + x_pos, 1)
    }
  
  return button_dict

# Building a dictionary of popup windows, based on a list of popup definitions

def build_popup_windows(popup_definition):

  popup_dict = {}

  for popup in popup_definition:

    popup_name = popup['name']

    popup_dict[popup_name] = {
      'buttons': []
    }

    # Need to figure out how many buttons the popup is to have - so as to centre them in the screen
    n_buttons = len(popup['buttons'])
    button_starting_x = -1 * n_buttons * config.hud_icon_x / 2

    # For each of the buttons the popup is to have...
    for button in popup['buttons']:

      # Put them in the dictionary
      popup_dict[popup_name]['buttons'].append({
        'name': button,
        'v0': (button_starting_x, 0.8 - config.hud_icon_y),
        'v1': (button_starting_x + config.hud_icon_x, 0.8 - config.hud_icon_y),
        'v2': (button_starting_x + config.hud_icon_x, 0.8),
        'v3': (button_starting_x, 0.8)
      })

      # Then indent the x-position, ready for the next one!
      button_starting_x += config.hud_icon_x

    # The main window the buttons are to sit in - basically just button perimeters with a 0.01 buffer around edges
    popup_dict[popup_name]['v0'] = (-1 * n_buttons * config.hud_icon_x / 2 - 0.01, 0.79 - config.hud_icon_y)
    popup_dict[popup_name]['v1'] = (n_buttons * config.hud_icon_x / 2 + 0.01, 0.79 - config.hud_icon_y)
    popup_dict[popup_name]['v2'] = (n_buttons * config.hud_icon_x / 2 + 0.01, 0.81)
    popup_dict[popup_name]['v3'] = (-1 * n_buttons * config.hud_icon_x / 2 - 0.01, 0.81)

    popup_dict[popup_name]['color'] = (0.8, 0.8, 0.8)

  return popup_dict