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
# Below is suuuuper arbitrary, just space-filling to PoC movement
def build_object_list():

  points_1 = [
    [5, 5],
    [5, 6],
    [6, 6],
    [6, 5],
    [11, 5],
    [11, 11],
    [5, 11]
  ]

  translated_points_1 = []

  for n in points_1:
    translated_points_1.append(iso_translater(*n))

  points_2 = [
    [11, 5],
    [11, 11],
    [5, 11],
    [5, 5],
    [5, 6],
    [6, 6],
    [6, 5],
  ]

  points_2 = list(reversed(points_2))
  
  translated_points_2 = []

  for n in points_2:
    translated_points_2.append(iso_translater(*n))

  return [
    {
      'name': 'orb',
      'color': (1, 0, 0),
      'path': translated_points_1,
      'speed': 0.8,
      'lastKnownSegment': 0,
      'lastKnownPosition': translated_points_1[0]
    }, {
      'name': 'orb',
      'color': (0, 0, 1),
      'path': translated_points_2,
      'speed': 1.2,
      'lastKnownSegment': 0,
      'lastKnownPosition': translated_points_2[0]
    }
  ]