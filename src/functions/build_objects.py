from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

from .tools import iso_translater, cartesian_translater

# LOADING IN ALL OUR SETUP VARIABLES
import config

# Building a list of dictionaries for iso game board
def build_iso_gameboard():

  # PLEASE BE AWARE: GAMEBOARDS WITH ODD TOTAL AREAS WORK BEST
  # IE 11 x 11 vs 10 x 10

  board_x = config.gameboard_dimensions[0]
  board_y = config.gameboard_dimensions[1]

  cells = []

  for x in range(board_x):
    for y in range(board_y):
      
      v1_x, v1_y = iso_translater(x, y)
      v2_x, v2_y = iso_translater(x + 1, y)
      v3_x, v3_y = iso_translater(x + 1, y + 1)
      v4_x, v4_y = iso_translater(x, y + 1)

      cells.append({
        'v1': [v1_x, v1_y],
        'v2': [v2_x, v2_y],
        'v3': [v3_x, v3_y],
        'v4': [v4_x, v4_y],
        'height': config.unit_height,
        'color': (1, 1, 1 / (y + 0.0001)),
        'objectOnCell': None,
        'objectHeight': None
      })

  # Need the list to always be stored in descending order - for rendering orders sake
  return list(reversed(cells))


# ------ TESTING MOVING OBJECTS ------ #
def build_object_list():

  v1_x, v1_y = iso_translater(5, 5)
  v2_x, v2_y = iso_translater(8, 5)
  v3_x, v3_y = iso_translater(8, 8)
  v4_x, v4_y = iso_translater(5, 8)

  return [
    {
      'name': 'orb',
      'path': [
        [v1_x, v1_y],
        [v2_x, v2_y],
        [v3_x, v3_y],
        [v4_x, v4_y]
      ],
      'speed': 0.5,
      'lastKnownSegment': 0,
      'lastKnownPosition': [v1_x, v1_y]
    }
  ]