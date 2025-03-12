from copy import deepcopy

from .tools import add_vectors, find_vector_midpoint

import config

# Global vars used only in the construction process
temp_cells_constructed_on = []
temp_path = []

# Might use this to decide directions for next construction block
direction_mapper = [
  (1, 0),
  (0, 1),
  (-1, 0),
  (0, -1)
]
construction_direction = 0

def place_first_piece_of_line():

  global temp_cells_constructed_on, temp_path

  # If no current pieces have been placed yet then place the first piece
  if len(temp_cells_constructed_on) == 0:

    # Add a line object to the cell being clicked on
    config.gameboard[config.interaction_cell]['objectOnCell'] = {
      'type': 'line',
      'orientation': construction_direction
    }

    config.gameboard[config.interaction_cell]['objectHeight'] = 0

    # Log the clicked cell as the first cell being constructed on
    temp_cells_constructed_on.append(config.interaction_cell)

    # Write first coordinate to the temp object path
    temp_path.append(find_vector_midpoint(config.gameboard[config.interaction_cell]['v3'], config.gameboard[config.interaction_cell]['v0']))

    # Now dictate that the next cell being constructed on is x/y +- 1 away from the interaction cell
    config.construction_cell = tuple(add_vectors(config.interaction_cell, direction_mapper[construction_direction]))

    # Let's see if any of that functionally worked...
    print(config.gameboard[config.interaction_cell])
    print(temp_cells_constructed_on)
    print(temp_path)
    print(f'Interaction Cell index is: {config.interaction_cell}')
    print(f'Construction Cell index is: {config.construction_cell}')


# Pretty much the same pattern as above but with the construction_cell being used as reference rather than interaction_cell
def place_next_piece_of_line(line_direction):

  global temp_cells_constructed_on, temp_path, construction_direction

  if len(temp_cells_constructed_on) != 0:

    # Line orientation == construction direction for left turns
    # Line orientation == construction direction + 1 for right turns
    # On the assumption that direction(0) = (1, 0) and rotates counterclockwise per each increment
    # And orientation of the corner made by direction(0) -> direction(1) is also orientation(0), and also rotates counterclockwise
    # Worst description of that ever lmao, but draw it out on paper if you ever forget - that's how I just figured it out

    if line_direction == 'left':
      line_type = 'turn'
      line_orientation = construction_direction
      # Update the construction direction to reflect the direction provided in function
      construction_direction = (construction_direction + 1) % 4

    elif line_direction == 'right':
      line_type = 'turn'
      line_orientation = (1 + construction_direction) % 4
      # Update the construction direction to reflect the direction provided in function
      construction_direction = (construction_direction - 1) % 4

    # else - drawing a straight line, which is trivially of orientation == direction
    else:
      line_type = 'line'
      line_orientation = construction_direction

    config.gameboard[config.construction_cell]['objectOnCell'] = {
      'type': line_type,
      'orientation': line_orientation
    }

    config.gameboard[config.construction_cell]['objectHeight'] = 0

    temp_cells_constructed_on.append(config.construction_cell)

    # increment the construction cell to the next one
    config.construction_cell = tuple(add_vectors(config.construction_cell, direction_mapper[construction_direction]))

    print(config.gameboard[config.construction_cell])
    print(temp_cells_constructed_on)
    print(temp_path)
    print(config.construction_cell)