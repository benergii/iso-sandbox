from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .camera_operations import move_camera, rotate_camera
from .mouse_operations import mouse_hover_mechanics, mouse_click_mechanics, mouse_drag_mechanics

# 'Special' keys here - such as arrow keys, anything non-alphanumeric basically
def special_keys(key, x, y):

  move_camera(key)
  
  glutPostRedisplay()

# 'Normal' keys here - think alphanumeric type beat
def normal_keys(key, x, y):

  rotate_camera(key)
  
  glutPostRedisplay()

# Mouse motion will probs all go in here
def mouse_motion(x, y):

  mouse_hover_mechanics(x, y)

  glutPostRedisplay()

# Mouse Click
def mouse_click(button, state, x, y):

  mouse_click_mechanics(button, state, x, y)

  glutPostRedisplay()

# Mouse Dragging
def mouse_dragging(x, y):

  mouse_drag_mechanics(x, y)

  glutPostRedisplay()