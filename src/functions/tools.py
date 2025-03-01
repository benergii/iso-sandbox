import config

# Translate cartesian coordinates to isometric coordinates
def iso_translater(x, y):

  iso_x = (x * config.unit_width - y * config.unit_width) * (config.unit_width / 2)
  iso_y = (x * config.unit_width + y * config.unit_width) * (config.unit_width / 3)

  return iso_x, iso_y

# Translate isometric coordinates to cartesian coordiniates
def cartesian_translater(iso_x, iso_y):
    
  x = (iso_x / (config.unit_width / 2) + iso_y / (config.unit_width / 3)) / (2 * config.unit_width)
  y = (iso_y / (config.unit_width / 3) - iso_x / (config.unit_width / 2)) / (2 * config.unit_width)
    
  return x, y

# Rotate coordinates (by converting them from iso to cart, applying a cart rotation, then converting back to iso)
def rotate_coordinates(iso_x, iso_y):

  cart_x, cart_y = cartesian_translater(iso_x, iso_y)

  orig_x = cart_x
  cart_x = -1 * cart_y
  cart_y = orig_x

  iso_x_rotated, iso_y_rotated = iso_translater(cart_x, cart_y)

  return iso_x_rotated, iso_y_rotated

# I have no reason to need these - but might be useful
def add_vectors(v1, v2):
  return [
    v1[0] + v2[0],
    v1[1] + v2[1]
  ]

def multiply_vectors(v1, v2):

  return [
    v1[0] * v2[0],
    v1[1] * v2[1]
  ]