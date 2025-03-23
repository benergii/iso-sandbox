import config

# TERRAFORM POPUP
# Note that the below is following a generalised popup pattern, whereby the function name has to be 'mode'_popup(action)
# This keeps all popup management very simple

def terraform_popup(action):

  if action == 'increase': config.terraform_scalar += 1
  elif action == 'decrease': config.terraform_scalar -= 1
  
  print(f'Terraform Scalar is {config.terraform_scalar}')


# The actual function to drag the cells up and down
# Yeah we're modularising things baby!!

def terraform_cells(units_dragged):

  # First, let's store the min and max heights of the land being dragged
  cell_heights = [config.gameboard[cell_index]['height'] for cell_index in config.interaction_cells]
  min_cell_height = min(cell_heights); max_cell_height = max(cell_heights)

  for cell_index in config.interaction_cells:

    if (
       # Positive units_dragged should only affect cells with height equal to the minimum height
      (units_dragged > 0 and config.gameboard[cell_index]['height'] == min_cell_height)
      or
      # Conversely, negative units_dragged should do the same with maximum height``
      (units_dragged < 0 and config.gameboard[cell_index]['height'] == max_cell_height)
    ):
        config.gameboard[cell_index]['height'] = max(config.gameboard[cell_index]['height'] + units_dragged, config.unit_height)