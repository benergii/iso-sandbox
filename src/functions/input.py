from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .camera_operations import move_camera, rotate_camera

# LOADING IN ALL OUR SETUP VARIABLES
import config

# 'Special' keys here - such as arrow keys, anything non-alphanumeric basically
def special_keys(key, x, y):

  move_camera(key)
  
  glutPostRedisplay()

# 'Normal' keys here - think alphanumeric type beat
def normal_keys(key, x, y):

  rotate_camera(key)
  
  glutPostRedisplay()