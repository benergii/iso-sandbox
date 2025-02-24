import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

from functions.iso_gameboard import build_iso_gameboard
from functions.render_gameboard import render_grid

window_x = 800
window_y = 600
unit_width = 0.4
gameboard_dimensions = [3, 3]

# ------------------------------------------ #
#          | Initialisation Stage |
#          ------------------------

# Unit height needs to correspond with the iso-transformed unit width
unit_height = (unit_width ** 2) * (2 / 6)

# Building the game board
gameboard = build_iso_gameboard(gameboard_dimensions, unit_width, unit_height)

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

  render_grid(gameboard)

  glutSwapBuffers()

# -------------------------------------------- #
#         | Building runtime stage |
#         --------------------------

def main():

  # Initialise window
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
  glutInitWindowSize(window_x, window_y)
  glutCreateWindow('Iso Sandbox')
  init()

  # Render stuff
  glutDisplayFunc(draw_scene)

  # Start the loop of the game
  glutMainLoop()

# -------------------------------------------- #
#                | Executing |
#                -------------

if __name__ == '__main__':
  main()