from .tools import add_vectors, find_vector_midpoint

import config

# Might use this to decide directions for next construction block
direction_mapper = [
  (1, 0),
  (0, 1),
  (-1, 0),
  (0, -1)
]
construction_direction = 0

current_height = None
button_sequence = []

# Use the 'z' key to rotate the orientation of the starting line
def rotate_starting_piece():

  global construction_direction

  # Only perform rotation if we're in construct_path mode, and we haven't built any line segments yet
  if config.user_data['mode'] == 'construct_path' and len(config.temp_cells_constructed_on) == 0:
    # Keep it in base 4 arithmetic please!!!
    construction_direction = (construction_direction + 1) % 4
    
    print(f'Initial piece orientation has changed to: {construction_direction}')

# YEAH BRO LETS DO COLLISION DETECTION!!!
def collision_detection():

  # Cases we need to account for:
  if (
    # 1: construction cell already has an object on it at the current construction height
    config.gameboard[config.construction_cell]['objectHeight'] == current_height
    # 2: construction cell is higher than current piece attempting to build
    or config.gameboard[config.construction_cell]['height'] > current_height
  ):
    config.can_you_build_here = False
    print('CANT BUILD HERE BRO!!!')
  else:
    config.can_you_build_here = True


# Logic for not finishing the path - if the user clicks on one of the other HUD buttons before completion
def kill_the_path_early():

  global construction_direction, button_sequence

  # First - clear all the cells which lines were placed on
  # This pattern was an EXCELLENT idea - good on you for thinking of it early
  for cell_index in config.temp_cells_constructed_on:

    config.gameboard[cell_index]['objectOnCell'] = None
    config.gameboard[cell_index]['objectHeight'] = None
  
  # Then just reset all the construction vars back to default
  config.temp_cells_constructed_on = []
  config.temp_path = []
  config.temp_height = []
  config.construction_cell = None
  construction_direction = 0
  button_sequence = []

  print('PATH HAS BEEN TERMINATED EARLY')

# Logic for completing the path - for when the construction engine meets up with the start of the path!
def complete_line_construction():

  global construction_direction, button_sequence

  # Actions for completion of path:
  # 1. write entry to the 'objects' dictionary
  # 2. clear the config.temp_cells_constructed_on and config.temp_path global variables
  # 3. clear the construction_cell config variable
  # 4. set the user_data mode to NoneType

  config.objects.append({
    'name': 'object1',
    'color': (1, 0, 0),
    'path': config.temp_path,
    'height': config.temp_height,
    'speed': 0.2,
    'lastKnownSegment': 0,
    'lastKnownPosition': config.temp_path[0],
    'lastKnownHeight': config.temp_height[0]
  })

  config.temp_path = []
  config.temp_cells_constructed_on = []
  config.temp_height = []
  config.construction_cell = None
  config.user_data['mode'] = None
  construction_direction = 0
  button_sequence = []

  print('LINE IS NOW COMPLETE')


def place_first_piece_of_line():

  global current_height

  # If no current pieces have been placed yet then place the first piece
  if len(config.temp_cells_constructed_on) == 0:

    # Setting up the localised construction variables
    button_sequence.append('straight')
    current_height = config.gameboard[config.interaction_cells[0]]['height']

    # Add a line object to the cell being clicked on
    config.gameboard[config.interaction_cells[0]]['objectsOnCell'].append({
      'type': 'straight',
      'orientation': construction_direction,
      'height': current_height
    })

    # Log the clicked cell as the first cell being constructed on
    config.temp_cells_constructed_on.append(config.interaction_cells[0])

    # Write first coordinate to the temp object path
    config.temp_path.append(
      find_vector_midpoint(
        add_vectors(config.gameboard[config.interaction_cells[0]]['v2'], [0, current_height]),
        add_vectors(config.gameboard[config.interaction_cells[0]]['v0'], [0, current_height])
      )
    )

    # Write current height to temp height array
    config.temp_height.append(current_height)

    # Now dictate that the next cell being constructed on is x/y +- 1 away from the interaction cell
    config.construction_cell = tuple(add_vectors(config.interaction_cells[0], direction_mapper[construction_direction]))

    # Let's see if any of that functionally worked...
    print(config.temp_cells_constructed_on)
    print(config.temp_path)

    # NOW LETS SEE IF THE NEXT MOVE IS ALLOWED
    collision_detection()

# Need a little function to block construction if attempting to build below land
def z_axis_collision_detection(action):

  # Return True if user is trying to build down below construction cell height
  return action == 'down' and config.gameboard[config.construction_cell]['height'] >= current_height

# Pretty much the same pattern as above but with the construction_cell being used as reference rather than interaction_cell
def construct_path_popup(action):

  global construction_direction, current_height, button_sequence

  if len(config.temp_cells_constructed_on) != 0:

    # Let's write in the 'delete' button first
    if action == 'delete':

      # 1. Set current height to last recorded temp height
      current_height = config.temp_height[-1]
      
      # 2. Set construction cell to the last cell constructed on
      #    OR IF DELETING THE FIRST PIECE THEN JUST WIPE IT OUT
      config.construction_cell = None if len(config.temp_cells_constructed_on) == 1 else config.temp_cells_constructed_on[-1]

      # 3. Set construction direction to what it was at prior placement
      if button_sequence[-1] == 'left': construction_direction = (construction_direction - 1) % 4
      elif button_sequence[-1] == 'right': construction_direction = (construction_direction + 1) % 4

      # 4. Wipe out the object on the cell
      config.gameboard[config.temp_cells_constructed_on[-1]]['objectsOnCell'].pop()

      # 5. Pop the last entries from the Config arrays + button sequence
      config.temp_cells_constructed_on.pop()
      config.temp_height.pop()
      config.temp_path.pop()
      button_sequence.pop()

      # 6. Run collision detection on updated construction cell
      collision_detection()
    
    else:

      if config.can_you_build_here and z_axis_collision_detection(action) == False:

        # Line orientation == construction direction for left turns
        # Line orientation == construction direction + 1 for right turns
        # On the assumption that direction(0) = (1, 0) and rotates counterclockwise per each increment
        # And orientation of the corner made by direction(0) -> direction(1) is also orientation(0), and also rotates counterclockwise
        # Worst description of that ever lmao, but draw it out on paper if you ever forget - that's how I just figured it out

        print(f'BUTTON PRESSED: {action}')

        if action == 'left':
          line_type = 'turn'
          line_orientation = construction_direction
          # Update the construction direction to reflect the direction provided in function
          construction_direction = (construction_direction + 1) % 4

        elif action == 'right':
          line_type = 'turn'
          line_orientation = (1 + construction_direction) % 4
          # Update the construction direction to reflect the direction provided in function
          construction_direction = (construction_direction - 1) % 4

        # UP BUTTON
        elif action == 'up':
          line_type = 'straightToSlope' if button_sequence[-1] != 'up' else 'slope'
          line_orientation = construction_direction

        # DOWN BUTTON
        elif action == 'down':
          line_type = 'slopeToStraight' if button_sequence[-1] != 'down' else 'slope'
          line_orientation = (construction_direction + 2) % 4

        # else - drawing a straight line, which is trivially of orientation == direction
        elif action == 'straight':
          if button_sequence[-1] == 'down':
            line_type = 'straightToSlope'
            line_orientation = (construction_direction + 2) % 4
          elif button_sequence[-1] == 'up':
            line_type = 'slopeToStraight'
            line_orientation = construction_direction
          else:
            line_type = 'straight'
            line_orientation = construction_direction

        # Adding the line object to the cell
        config.gameboard[config.construction_cell]['objectsOnCell'].append({
          'type': line_type,
          'orientation': line_orientation,
          'height': current_height
        })

        # Continuing to add to the list of cells constructed on - so we can wipe them out if exit partway through
        config.temp_cells_constructed_on.append(config.construction_cell)

        # Adding the new point to the temp path
        config.temp_path.append(
          find_vector_midpoint(
            add_vectors(config.gameboard[config.construction_cell]['v2'], [0, current_height]),
            add_vectors(config.gameboard[config.construction_cell]['v0'], [0, current_height])
          )
        )

        # Write current height to temp height array
        config.temp_height.append(current_height)

        # Increment the working height if up/down arrows have been pressed
        if action == 'down': current_height -= config.unit_height
        elif action == 'up': current_height += config.unit_height

        print(f'{action} line placed on cell {config.construction_cell}')

        # increment the construction cell to the next one
        config.construction_cell = tuple(add_vectors(config.construction_cell, direction_mapper[construction_direction]))

        # Log the button pressed - important for deletion of pieces
        button_sequence.append(action)

        # Is the line complete? If so, let's kill this!
        if (
          config.temp_cells_constructed_on[0] == config.construction_cell
          and construction_direction == config.gameboard[config.construction_cell]['objectsOnCell'][-1]['orientation']
        ):
          complete_line_construction()

        # If not - then let's see if the next piece is possible to build on 
        else:
          collision_detection()

      # What happens if you fail collision tests
      else:
        print('CANT BUILD THAT HERE TRY AGAIN')