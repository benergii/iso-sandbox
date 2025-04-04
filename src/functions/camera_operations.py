from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .tools import rotate_coordinates, rotate_coordinates_with_height_component

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
def rotate_camera():

  print('Starting rotation')

  # ROTATION IS TRICKY - BUT THIS IS HOW IT NEEDS TO BE DONE
  # As it is infinitely better to store the coords as iso in the gameboard var, rather than convert on every frame render

  for cell_index in config.cell_render_order:

    # Retrieve the cell from the dictionary using the cell index
    cell = config.gameboard[cell_index]

    for n in range(4):

      iso_x, iso_y = rotate_coordinates(*cell[f'v{n}'])

      cell[f'v{n}'][0] = iso_x
      cell[f'v{n}'][1] = iso_y
    
  # Also need to rotate all the object paths and current positions
  # KEEPING IN MIND YOU NEED TO TRANSFORM THE PATHS AND POSITIONS BY THEIR HEIGHTS FIRST
  # Because iso coordinates are hard
  for object in config.objects:

    # Approach for this (since is a list) is to just append a new blank list then overwrite the old one
    rotated_path = []
    for n in range(len(object['path'])):
      # Rotation needs to be around the projection of an object to the grid base - so need to call a 'height component' rotation function
      rotated_path.append(rotate_coordinates_with_height_component(*object['path'][n], object['height'][n]))
      
    object['path'] = rotated_path

    # Now do the Current Position as well
    # Rotation needs to be around the projection of an object to the grid base - so need to call a 'height component' rotation function
    object['lastKnownPosition'] = rotate_coordinates_with_height_component(*object['lastKnownPosition'], object['lastKnownHeight'])
  
  # ALSO need to rotate any coordinates stored in a temporary path - oh my lord
  rotated_temp_path = []
  for n in range(len(config.temp_path)):
    # Rotation needs to be around the projection of an object to the grid base - so need to call a 'height component' rotation function
    rotated_temp_path.append(rotate_coordinates_with_height_component(*config.temp_path[n], config.temp_height[n]))
  config.temp_path = rotated_temp_path
    
  # Need to run a full rotation pattern on the camera_offset config variable too
  config.camera_offset = [*rotate_coordinates(*config.camera_offset)]
    
  # Update the rotation integer to tell game which sprites to render
  config.rotation_integer = (config.rotation_integer + 1) % 4
    
  # Now, in order for rendering to work, we need to sort the 'render order' array, in descending Y, then descending X within
  config.cell_render_order = sorted(config.gameboard.keys(), key = lambda t: (config.gameboard[t]['v0'][1], config.gameboard[t]['v0'][0]), reverse = True)
  print('Rotation complete')
  print(f'Now rendering sprites of rotation integer {config.rotation_integer}')