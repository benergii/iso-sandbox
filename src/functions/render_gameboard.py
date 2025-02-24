from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def render_grid(gameboard):

  # Need to reverse the gameboard to render from back-to-front
  for cell in reversed(gameboard):

    # Rendering the walls of each cell
    glColor(0.5, 0.5, 0.5)
    glBegin(GL_POLYGON)
    glVertex2f(*cell['v4'])
    glVertex2f(cell['v4'][0], cell['v4'][1] - cell['height'])
    glVertex2f(cell['v1'][0], cell['v1'][1] - cell['height'])
    glVertex2f(cell['v2'][0], cell['v2'][1] - cell['height'])
    glVertex2f(*cell['v2'])
    glEnd()
    
    # Rendering the actual cell surface
    glColor(*cell['color'])
    glBegin(GL_QUADS)
    for n in range(4):
      glVertex2f(*cell[f'v{n + 1}'])
    glEnd()

    # Rendering the grid around the cell
    glColor(0, 0, 1)
    glBegin(GL_LINE_LOOP)
    for n in range(4):
      glVertex2f(*cell[f'v{n + 1}'])
    glEnd()