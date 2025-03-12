from copy import deepcopy

from .tools import add_vectors

import config

# Global vars used only in the construction process
temp_cells_constructed_on = []
temp_path = []


def place_first_piece_of_line():

  global temp_cells_constructed_on, temp_path

  # If no current pieces have been placed yet then place the first piece
  if len(temp_cells_constructed_on) == 0:

    # Add a line object to the cell being clicked on
    config.gameboard[config.interaction_cell]['objectOnCell'] = {
      'type': 'line',
      'orientation': 1
    }

    config.gameboard[config.interaction_cell]['objectHeight'] = 0

    # Log the clicked cell as the first cell being constructed on
    temp_cells_constructed_on.append(config.interaction_cell)

    # Write first coordinate to the temp object path
    v4 = config.gameboard[config.interaction_cell]['v4']
    v1 = config.gameboard[config.interaction_cell]['v1']
    temp_path.append([
      (v4[0] + v1[0]) / 2,
      (v4[1] + v1[1]) / 2
    ])

    # Now dictate that the next cell being constructed on is x + 1 away from the interaction cell
    config.construction_cell = deepcopy(add_vectors(config.interaction_cell, (1, 0)))

    # Let's see if any of that functionally worked...
    print(config.gameboard[config.interaction_cell])
    print(temp_cells_constructed_on)
    print(temp_path)