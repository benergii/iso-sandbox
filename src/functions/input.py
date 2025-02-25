from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# LOADING IN ALL OUR SETUP VARIABLES
import config

# 'Special' keys here - such as arrow keys, anything non-alphanumeric basically
def special_keys(key, x, y):

  global camera_offset

  if key == GLUT_KEY_UP:
    config.camera_offset[1] -= (config.unit_width ** 2) * (1 / 3)
  elif key == GLUT_KEY_DOWN:
    config.camera_offset[1] += (config.unit_width ** 2) * (1 / 3)
  elif key == GLUT_KEY_LEFT:
    config.camera_offset[0] += (config.unit_width ** 2) * (1 / 2)
  elif key == GLUT_KEY_RIGHT:
    config.camera_offset[0] -= (config.unit_width ** 2) * (1 / 2)

  print(f'Camera Offset is: {config.camera_offset}')
  
  glutPostRedisplay()