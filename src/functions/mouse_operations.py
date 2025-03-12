from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .tools import add_vectors, is_point_in_quad, normalise_pixel_coords

# LOADING IN ALL OUR SETUP VARIABLES
import config

# Some dummy variables to handle mouse mechanics
click_position = None
is_dragging = False

# Handle the mouse hovering mechanics
def mouse_hover_mechanics(x, y):

  # Convert pixel coords to normalised (-1, 1) coords
  gl_x, gl_y = normalise_pixel_coords(x, y)

  config.interaction_cell = None

  for cell_index in config.cell_render_order:

    cell = config.gameboard[cell_index]

    # Preparing cell vertices for area intersection detection
    v1 = add_vectors(cell['v1'], [0, cell['height']], config.camera_offset)
    v2 = add_vectors(cell['v2'], [0, cell['height']], config.camera_offset)
    v3 = add_vectors(cell['v3'], [0, cell['height']], config.camera_offset)
    v4 = add_vectors(cell['v4'], [0, cell['height']], config.camera_offset)

    if is_point_in_quad((gl_x, gl_y), v1, v2, v3, v4):
      
      config.interaction_cell = cell

# Handle the mouse clicking mechanics
def mouse_click_mechanics(button, state, x, y):

  global click_position, is_dragging

  # Convert pixel coords to normalised OpenGL coords
  gl_x, gl_y = normalise_pixel_coords(x, y)

  # Handling left click
  if button == GLUT_LEFT_BUTTON:

    if state == GLUT_DOWN:
      click_position = [gl_x, gl_y]

      # First - are we clicking on a HUD button?
      for button_index in list(config.hud_buttons.keys()):
        button = config.hud_buttons[button_index]

        if is_point_in_quad((gl_x, gl_y), button['v1'], button['v2'], button['v3'], button['v4']):

          print(f'Clicked on the {button['buttonName']} button')

          # Below allows for toggling on buttons - if you're already in Terraform then exit Terraform
          if config.user_data['mode'] == button['buttonName']:
            config.user_data['mode'] = None
          else:
            config.user_data['mode'] = button['buttonName']
      
      # Then we handle all the other stuff (at this stage just for terraforming)

      is_dragging = True
      print(f'Mouse Clicked at: {click_position}')
    
    elif state == GLUT_UP:
      click_position = None
      is_dragging = False
      print(f'Mouse unclicked at: [{gl_x}, {gl_y}]')

# Handle the mouse being click-dragged on screen
def mouse_drag_mechanics(x, y):

  global click_position, is_dragging

  # Normalise mouse coords
  gl_x, gl_y = normalise_pixel_coords(x, y)

  # Only activate a 'dragging' motion if the mouse has clicked down, and if the user mode is 'terraform'
  if is_dragging and config.user_data['mode'] == 'terraform':
    
    # Using int(division) instead of floor division, as floor division passes 0 at twice the rate for neg numbers
    units_dragged = int((gl_y - click_position[1]) / config.unit_height) * config.unit_height

    # If you ever drag up or down by one unit...
    if units_dragged != 0:

      # Then update the height of the cell!
      config.interaction_cell['height'] += units_dragged
      click_position = [gl_x, gl_y]