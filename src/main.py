import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# LOADING IN ALL OUR SETUP VARIABLES
import config

from functions.render_gameboard import render_grid
from functions.input import special_keys, normal_keys, mouse_motion, mouse_click, mouse_dragging

# ------------------------------------------ #
#          | Initialisation Stage |
#          ------------------------

def init():

  # Background Color of play window
  glClearColor(0.1, 0.1, 0.1, 1)
    
  # Allow for image transparency when rendering textures
  glEnable(GL_BLEND)
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

#  ------------------------------------------ # 
#           | Scene Drawing Stage |
#           -----------------------

def draw_scene():

  glClear(GL_COLOR_BUFFER_BIT)

  render_grid()

  glutSwapBuffers()

# -------------------------------------------- #
#         | Building runtime stage |
#         --------------------------

def main():

  # Initialise window
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
  glutInitWindowSize(config.window_x, config.window_y)
  glutCreateWindow('Iso Sandbox')
  init()

  # Render stuff
  glutDisplayFunc(draw_scene)
  glutSpecialFunc(special_keys)
  glutKeyboardFunc(normal_keys)
  glutPassiveMotionFunc(mouse_motion)
  glutMouseFunc(mouse_click)
  glutMotionFunc(mouse_dragging)

  # Start the loop of the game
  glutMainLoop()

# -------------------------------------------- #
#                | Executing |
#                -------------

if __name__ == '__main__':
  main()