from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import config

from .tools import add_vectors, find_vector_midpoint

# ------------------------------------------ #

# RENDERING WITH A DICTIONARY PATTERN INSTEAD
def render_with_dictionary():

  # Fist let's compile a list of ALL elements we need to render - cells and objects
  # Let's create a 'type' to define whether they're a cell (0) or an object (1)
  # And also a 'key' which we use to retrieve them from their relevant list/dicts

  # Cells are in a dict - so follow this pattern
  
  # NB: need to obtain the highest vertex of the cell, so use base-4 arithmetic to cycle in reverse direction to rotation
  highest_vertex = (2 - config.rotation_integer) % 4

  all_elements = [{
    'type': 0,
    'key': n,
    'coord': config.gameboard[n][f'v{highest_vertex}']
    } for n in config.cell_render_order
  ]

  # Objects are still in a list of dicts (might change this at some point)
  for n in range(len(config.objects)):

    all_elements.append({
      'type': 1,
      'key': n,
      'coord': config.objects[n]['lastKnownPosition']
    })

  # Sort em all!!
  all_elements = sorted(all_elements, key = lambda t: (t['coord'][1], t['coord'][0], t['type']), reverse = True)

  # Now for each element...
  for element in all_elements:

    # If they're a cell...
    if element['type'] == 0:
      
      # Then render a cell!
      cell = config.gameboard[element['key']]

      # Rendering the walls of each cell
      # Vertices need to cycle depending on which point of rotation we are at
      # So doing some modular stuff to account for that
      vertex_order = [
        (3 - config.rotation_integer) % 4,
        (0 - config.rotation_integer) % 4,
        (1 - config.rotation_integer) % 4
      ]

      glColor(0.5, 0.5, 0.5)
      glBegin(GL_POLYGON)
      glVertex2f(*add_vectors(cell[f'v{vertex_order[0]}'], [0, cell['height']], config.camera_offset))
      glVertex2f(*add_vectors(cell[f'v{vertex_order[0]}'], config.camera_offset))
      glVertex2f(*add_vectors(cell[f'v{vertex_order[1]}'], config.camera_offset))
      glVertex2f(*add_vectors(cell[f'v{vertex_order[2]}'], config.camera_offset))
      glVertex2f(*add_vectors(cell[f'v{vertex_order[2]}'], [0, cell['height']], config.camera_offset))
      glEnd()

      # Rendering the actual cell surface
      glColor(*cell['color'])
      glBegin(GL_QUADS)
      for n in range(4):
        glVertex2f(*add_vectors(cell[f'v{n}'], [0, cell['height']], config.camera_offset))
      glEnd()

      # Rendering the grid around the cell
      glColor(0, 0, 1, 0.5)
      glLineWidth(3) if config.interaction_cell == element['key'] else glLineWidth(0.5) # Thicker grid if mouse hover
      glBegin(GL_LINE_LOOP)
      for n in range(4):
        glVertex2f(*add_vectors(cell[f'v{n}'], [0, cell['height']], config.camera_offset))
      glEnd()

      # OBJECT RENDERING
      # For now just going to render straight lines...
      if cell['objectOnCell']:

        if cell['objectOnCell']['type'] == 'line':
          start_vertex = find_vector_midpoint(cell['v3'], cell['v0'])
          end_vertex = find_vector_midpoint(cell['v1'], cell['v2'])

          glColor(0, 0, 1)
          glLineWidth(3)
          glBegin(GL_LINE_LOOP)
          glVertex2f(*add_vectors(start_vertex, [0, cell['height']], [0, cell['objectHeight']], config.camera_offset))
          glVertex2f(*add_vectors(end_vertex, [0, cell['height']], [0, cell['objectHeight']], config.camera_offset))
          glEnd()

    # Else, if they're an object...
    elif element['type'] == 1:

      # You guessed it skipper - render an object!
      # It's really that easy!
      object = config.objects[element['key']]

      # For now I'm just rendering a super basic quad around a point - just to PoC this
      glColor(*object['color'])
      glBegin(GL_QUADS)
      glVertex2f(*add_vectors(object['lastKnownPosition'], [-0.01, -0.01], [0, object['height']], config.camera_offset))
      glVertex2f(*add_vectors(object['lastKnownPosition'], [0.01, -0.01], [0, object['height']], config.camera_offset))
      glVertex2f(*add_vectors(object['lastKnownPosition'], [0.01, 0.01], [0, object['height']], config.camera_offset))
      glVertex2f(*add_vectors(object['lastKnownPosition'], [-0.01, 0.01], [0, object['height']], config.camera_offset))
      glEnd()


def render_hud():

  for button_index in list(config.hud_buttons.keys()):

    button = config.hud_buttons[button_index]

    # Render button background
    glColor(1, 0.7, 0.7) if config.user_data['mode'] == button['buttonName'] else glColor(1, 1, 1)
    glBegin(GL_QUADS)
    for n in range(4):
      glVertex2f(*button[f'v{n}'])
    glEnd()

    # Render button outline
    glColor(0.4, 0.4, 0.4)
    glLineWidth(0.5)
    glBegin(GL_LINE_LOOP)
    for n in range(4):
      glVertex2f(*button[f'v{n}'])
    glEnd()



def render_popup_windows():
  
  if config.user_data['mode'] != None:

    window_to_render = config.popup_windows[config.user_data['mode']]

    # Render the panel for the buttons to sit on
    glColor(window_to_render['color'])
    glBegin(GL_QUADS)
    for n in range(4):
      glVertex2f(*window_to_render[f'v{n}'])
    glEnd()

    # Render each button + outline on top of the panel
    for button in config.popup_windows[config.user_data['mode']]['buttons']:

      glColor(1, 1, 1)
      glBegin(GL_QUADS)
      for n in range(4):
        glVertex2f(*button[f'v{n}'])
      glEnd()

      glColor(0.4, 0.4, 0.4)
      glLineWidth(0.5)
      glBegin(GL_LINE_LOOP)
      for n in range(4):
        glVertex2f(*button[f'v{n}'])
      glEnd()