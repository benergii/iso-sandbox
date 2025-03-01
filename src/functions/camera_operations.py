from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from copy import deepcopy

from .tools import iso_translater, cartesian_translater

# LOADING IN ALL OUR SETUP VARIABLES
import config

# Using the arrow keys to move the camera around
def move_camera(key):

  # Using arrow keys to move the camera offset setup vector
  if key == GLUT_KEY_UP:
    config.camera_offset[1] -= (config.unit_width ** 2) * (1 / 3)
  elif key == GLUT_KEY_DOWN:
    config.camera_offset[1] += (config.unit_width ** 2) * (1 / 3)
  elif key == GLUT_KEY_LEFT:
    config.camera_offset[0] += (config.unit_width ** 2) * (1 / 2)
  elif key == GLUT_KEY_RIGHT:
    config.camera_offset[0] -= (config.unit_width ** 2) * (1 / 2)

# Using the spacebar to rotate the camera 90 degrees counterclockwise
def rotate_camera(key):

  if key == b' ':

    # ROTATION IS TRICKY - BUT THIS IS HOW IT NEEDS TO BE DONE
    # As it is infinitely better to store the coords as iso in the gameboard var, rather than convert on every frame render

    for cell in config.gameboard:
      print(cell)
      # Storing v1 as will be overwriting it in loop
      # Need to deepcopy as taking item from dictionary
      v1 = deepcopy(cell['v1'])
      for n in [4, 3, 2, 1]:

        # First we need to convert back to cartesian coords
        cart_x, cart_y = cartesian_translater(*v1) if n == 1 else cartesian_translater(*cell[f'v{n}'])
        print(f'Converting the {n}th vertice: {cart_x}, {cart_y}')

        # Then we need to rotate it, as per standard (x' = -y, y' = x) pattern
        original_x = cart_x
        cart_x = -1 * cart_y
        cart_y = original_x
        print(f'Rotated coordinates: {cart_x}, {cart_y}')

        # Now finally, we convert BACK to iso LOL
        iso_x, iso_y = iso_translater(cart_x, cart_y)

        # NOW WE WRITE BACK TO THE CELL
        if n == 3:
          print('Writing to the 4th vertice')
          cell['v4'][0] = iso_x
          cell['v4'][1] = iso_y
        else:
          print(f'Writing to the {(n + 1) % 4}th vertice')
          cell[f'v{(n + 1) % 4}'][0] = iso_x
          cell[f'v{(n + 1) % 4}'][1] = iso_y
      
      config.rotation_integer = (config.rotation_integer + 1) % 4
      print('Rotation complete')
      print(f'Now rendering sprites of rotation integer {config.rotation_integer}')
    
    # Now, in order for rendering to work, we need to sort the gameboard array
    config.gameboard = sorted(config.gameboard, key = lambda t: (t['v1'][1], t['v1'][0]))