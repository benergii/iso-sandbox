from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .tools import add_vectors, is_point_in_quad, normalise_pixel_coords
from .terraform import *
from .construction import *

# LOADING IN ALL OUR SETUP VARIABLES
import config

# Some dummy variables to handle mouse mechanics
click_position = None
is_dragging = False

# Handle the mouse hovering mechanics
def mouse_hover_mechanics(x, y):

  # Convert pixel coords to normalised (-1, 1) coords
  gl_x, gl_y = normalise_pixel_coords(x, y)

  # This line is necessary to clear the hovered cells when the mouse leaves the gameboard
  config.interaction_cells = []

  # Only show hovered cells if an interaction mode is selected
  if config.user_data['mode']:

    # Detecting hover over cell, storing the cell index if hovered
    for cell_index in config.cell_render_order:

      cell = config.gameboard[cell_index]

      # Preparing cell vertices for area intersection detection
      v0 = add_vectors(cell['v0'], [0, cell['height']], config.camera_offset)
      v1 = add_vectors(cell['v1'], [0, cell['height']], config.camera_offset)
      v2 = add_vectors(cell['v2'], [0, cell['height']], config.camera_offset)
      v3 = add_vectors(cell['v3'], [0, cell['height']], config.camera_offset)

      if is_point_in_quad((gl_x, gl_y), v0, v1, v2, v3):

        cells_hovered = []

        for x in range(config.terraform_scalar + 1):
          for y in range(config.terraform_scalar + 1):
            # NB: the // division is to offset the cells hovered such that the curser is always in the middle of the spread
            cells_hovered.append((cell_index[0] + x - (config.terraform_scalar // 2), cell_index[1] + y - (config.terraform_scalar // 2)))

        config.interaction_cells = cells_hovered

# --------------------------------- MOUSE CLICK MECHANICS --------------------------------- #

def mouse_click_mechanics(button, state, x, y):

  global click_position, is_dragging

  # Convert pixel coords to normalised OpenGL coords
  gl_x, gl_y = normalise_pixel_coords(x, y)

  # Handling left click
  if button == GLUT_LEFT_BUTTON:

    if state == GLUT_DOWN:
      click_position = [gl_x, gl_y]
      print(f'Mouse Clicked at: {click_position}')

      # ---- HUD Buttons ---- #

      for button_index in list(config.hud_buttons.keys()):
        button = config.hud_buttons[button_index]

        # Check to see if user has clicked on a button
        if is_point_in_quad((gl_x, gl_y), button['v0'], button['v1'], button['v2'], button['v3']):

          print(f'Clicked on the {button['buttonName']} button')

          # If so - update the user 'mode' to reflect this
          # Accounting for toggling - ie if user is in 'teraform' and clicks it again, then clear the mode
          if config.user_data['mode'] == button['buttonName']:
            config.user_data['mode'] = None
          else:
            config.user_data['mode'] = button['buttonName']
          
          # Placeholder to kill path construction early if HUD button is clicked
          # And to reset the terraform scalar
          # I need to find a better place to put these man...
          kill_the_path_early()
          config.terraform_scalar = 0

      # ---- POPUP BUTTONS ---- #

      if config.user_data['mode']:

        for button in config.popup_windows[config.user_data['mode']]['buttons']:

          # If user has clicked on a button (by determining intersection with button vertices)...
          if is_point_in_quad((gl_x, gl_y), button['v0'], button['v1'], button['v2'], button['v3']):

            # Then perform the function dictated by {user mode}_popup, with the button name passed as argument
            globals()[f'{config.user_data['mode']}_popup'](button['name'])
      
      # ---- Bespoke actions ---- #

      if config.user_data['mode'] == 'construct_path': place_first_piece_of_line()
      elif config.user_data['mode'] == 'terraform': is_dragging = True
    
    elif state == GLUT_UP:
      click_position = None
      is_dragging = False
      print(f'Mouse unclicked at: [{gl_x}, {gl_y}]')

# --------------------------------- MOUSE DRAG MECHANICS --------------------------------- #

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
      # config.interaction_cell['height'] += units_dragged
      for cell_index in config.interaction_cells:
        config.gameboard[cell_index]['height'] += units_dragged
      click_position = [gl_x, gl_y]