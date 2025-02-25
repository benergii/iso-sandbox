from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Translate cartesian coordinates to isometric coordinates
def iso_translater(x, y, unit_width):

  iso_x = (x * unit_width - y * unit_width) * (unit_width / 2)
  iso_y = (x * unit_width + y * unit_width) * (unit_width / 3)

  return iso_x, iso_y

# Center all cells around a provided cell index
def center_gameboard(cells, center_cell_index):

  pivot_point = cells[center_cell_index]['v1']

  for cell in cells:
    
    for n in range(4):
      cell[f'v{n + 1}'] = [
        cell[f'v{n + 1}'][0] - pivot_point[0],
        cell[f'v{n + 1}'][1] - pivot_point[1]
      ]

# Building a list of dictionaries for iso game board
def build_iso_gameboard(board_dimensions, unit_width, unit_height):

  # PLEASE BE AWARE: GAMEBOARDS WITH ODD TOTAL AREAS WORK BEST
  # IE 11 x 11 vs 10 x 10

  board_x = board_dimensions[0]
  board_y = board_dimensions[1]

  cells = []

  for x in range(board_x):
    for y in range(board_y):
      
      v1_x, v1_y = iso_translater(x, y, unit_width)
      v2_x, v2_y = iso_translater(x + 1, y, unit_width)
      v3_x, v3_y = iso_translater(x + 1, y + 1, unit_width)
      v4_x, v4_y = iso_translater(x, y + 1, unit_width)

      cells.append({
        'v1': [v1_x, v1_y],
        'v2': [v2_x, v2_y],
        'v3': [v3_x, v3_y],
        'v4': [v4_x, v4_y],
        'height': unit_height,
        'color': (1, 1, 1),
        'objectOnCell': None,
        'objectHeight': None
      })
  
  center_gameboard(cells, (board_x * board_y) // 2)

  return cells