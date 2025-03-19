import config


def terraform_popup(action):

  if action == 'increase': config.terraform_scalar += 1
  elif action == 'decrease': config.terraform_scalar -= 1
  
  print(f'Terraform Scalar is {config.terraform_scalar}')

def test_popup(action):

  print(action)