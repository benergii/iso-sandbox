from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .tools import add_vectors, is_point_in_quad, normalise_pixel_coords

# LOADING IN ALL OUR SETUP VARIABLES
import config

# Handle the mouse hovering mechanics
def mouse_hover_mechanics(x, y):

  # Convert pixel coords to normalised (-1, 1) coords
  gl_x, gl_y = normalise_pixel_coords(x, y)

  for cell in config.gameboard:

    # Preparing cell vertices for area intersection detection
    v1 = add_vectors(cell['v1'], config.camera_offset)
    v2 = add_vectors(cell['v2'], config.camera_offset)
    v3 = add_vectors(cell['v3'], config.camera_offset)
    v4 = add_vectors(cell['v4'], config.camera_offset)

    if is_point_in_quad((gl_x, gl_y), v1, v2, v3, v4):
      
      config.interaction_cell = cell