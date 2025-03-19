import config

# WAS JUST USING THIS TO TEST THE GENERALISED POPUP BUTTON FUNCTIONALITY

def terraform_popup(action):

  if action == 'increase': config.terraform_scalar += 1
  # Only decrease to 0 as minimum
  elif action == 'decrease': config.terraform_scalar = max(config.terraform_scalar - 1, 0)
  
  print(f'Terraform Scalar is {config.terraform_scalar}')