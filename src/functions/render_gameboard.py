from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import config

from .tools import add_vectors

def render_grid():

  # Need to reverse the gameboard to render from back-to-front
  for cell in config.gameboard:

    # Rendering the walls of each cell
    glColor(0.5, 0.5, 0.5)
    glBegin(GL_POLYGON)
    glVertex2f(*add_vectors(cell['v4'], [0, cell['height']], config.camera_offset))
    glVertex2f(*add_vectors(cell['v4'], config.camera_offset))
    glVertex2f(*add_vectors(cell['v1'], config.camera_offset))
    glVertex2f(*add_vectors(cell['v2'], config.camera_offset))
    glVertex2f(*add_vectors(cell['v2'], [0, cell['height']], config.camera_offset))
    glEnd()
    
    # Rendering the actual cell surface
    glColor(*cell['color'])
    glBegin(GL_QUADS)
    for n in range(4):
      glVertex2f(*add_vectors(cell[f'v{n + 1}'], [0, cell['height']], config.camera_offset))
    glEnd()

    # Rendering the grid around the cell
    glColor(0, 0, 1, 0.5)
    # Thicker grid if mouse is hovered over it
    glLineWidth(3) if config.interaction_cell == cell else glLineWidth(0.5)
    glBegin(GL_LINE_LOOP)
    for n in range(4):
      glVertex2f(*add_vectors(cell[f'v{n + 1}'], [0, cell['height']], config.camera_offset))
    glEnd()