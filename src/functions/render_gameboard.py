from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import config

from .tools import add_vectors

def render_grid(gameboard):

  # Need to reverse the gameboard to render from back-to-front
  for cell in reversed(gameboard):

    # Rendering the walls of each cell
    glColor(0.5, 0.5, 0.5)
    glBegin(GL_POLYGON)
    glVertex2f(cell['v4'][0] + config.camera_offset[0], cell['v4'][1] + config.camera_offset[1])
    glVertex2f(cell['v4'][0] + config.camera_offset[0], cell['v4'][1] - cell['height'] + config.camera_offset[1])
    glVertex2f(cell['v1'][0] + config.camera_offset[0], cell['v1'][1] - cell['height'] + config.camera_offset[1])
    glVertex2f(cell['v2'][0] + config.camera_offset[0], cell['v2'][1] - cell['height'] + config.camera_offset[1])
    glVertex2f(cell['v2'][0] + config.camera_offset[0], cell['v2'][1] + config.camera_offset[1])
    glEnd()
    
    # Rendering the actual cell surface
    glColor(*cell['color'])
    glBegin(GL_QUADS)
    for n in range(4):
      glVertex2f(*add_vectors(cell[f'v{n + 1}'], config.camera_offset))
    glEnd()

    # Rendering the grid around the cell
    glColor(0, 0, 1, 0.5)
    # Thicker grid if mouse is hovered over it
    glLineWidth(3) if config.interaction_cell == cell else glLineWidth(0.5)
    glBegin(GL_LINE_LOOP)
    for n in range(4):
      glVertex2f(*add_vectors(cell[f'v{n + 1}'], config.camera_offset))
    glEnd()