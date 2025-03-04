from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from copy import deepcopy

from .tools import rotate_coordinates

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

    print('Starting rotation')

    # ROTATION IS TRICKY - BUT THIS IS HOW IT NEEDS TO BE DONE
    # As it is infinitely better to store the coords as iso in the gameboard var, rather than convert on every frame render

    for cell in config.gameboard:
      
      # Storing v1 as will be overwriting it in loop
      # Need to deepcopy as taking item from dictionary
      v1 = deepcopy(cell['v1'])
      for n in [4, 3, 2, 1]:

        iso_x, iso_y = rotate_coordinates(*v1) if n == 1 else rotate_coordinates(*cell[f'v{n}'])

        # NOW WE WRITE BACK TO THE CELL
        # Using this 'if' condition as 4 % 4 = 0. We need it to be 4
        if n == 3:
          cell['v4'][0] = iso_x
          cell['v4'][1] = iso_y
        else:
          cell[f'v{(n + 1) % 4}'][0] = iso_x
          cell[f'v{(n + 1) % 4}'][1] = iso_y
    
    # Also need to rotate all the object paths and current positions
    for object in config.objects:

      # Approach for this (since is a list) is to just append a new blank list then overwrite the old one
      rotated_path = []
      for n in range(len(object['path'])):
        rotated_path.append(rotate_coordinates(*object['path'][n]))
      
      object['path'] = rotated_path

      # Now do the Current Position as well
      object['lastKnownPosition'] = rotate_coordinates(*object['lastKnownPosition'])
    
    # Need to run a full rotation pattern on the camera_offset config variable too
    config.camera_offset = [*rotate_coordinates(*config.camera_offset)]
    
    # Update the rotation integer to tell game which sprites to render
    config.rotation_integer = (config.rotation_integer + 1) % 4
    
    # Now, in order for rendering to work, we need to sort the gameboard array in descending coord order
    # As we need the farthest cells to render first
    config.gameboard = sorted(config.gameboard, key = lambda t: (t['v1'][1],t['v1'][0]), reverse = True)
    print('Rotation complete')
    print(f'Now rendering sprites of rotation integer {config.rotation_integer}')