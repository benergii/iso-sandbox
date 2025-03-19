import config

# WAS JUST USING THIS TO TEST THE GENERALISED POPUP BUTTON FUNCTIONALITY

def terraform_popup(action):

  if action == 'increase': config.terraform_scalar += 1
  elif action == 'decrease': config.terraform_scalar -= 1
  
  print(f'Terraform Scalar is {config.terraform_scalar}')