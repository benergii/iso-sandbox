import config


# I have no reason to need these - but might be useful
def add_vectors(v1, v2, v3 = [0, 0], v4 = [0, 0]):
  return [
    v1[0] + v2[0] + v3[0] + v4[0],
    v1[1] + v2[1] + v3[1] + v4[1]
  ]

def multiply_vectors(v1, v2, v3 = [0, 0]):

  return [
    v1[0] * v2[0] * v3[0],
    v1[1] * v2[1] * v3[1]
  ]

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

# Because everything in iso coords is based on a base grid, object coordinates need to have height removed and readded pre + post rotation
def rotate_coordinates_with_height_component(iso_x, iso_y, height):

  # Subtract height to project to grid coordinates
  grid_projected_coords = add_vectors([iso_x, iso_y], [0, -height])
  # Rotate the grid-projected coordinates
  rotated_projected_x, rotated_projected_y = rotate_coordinates(*grid_projected_coords)
  # Re-add the height back to the projected coordinates
  rotated_final_coords = add_vectors([rotated_projected_x, rotated_projected_y], [0, height])
  
  return rotated_final_coords[0], rotated_final_coords[1]

# Convert pixel coordinates to normalised OpenGL coordinates (between -1 and 1 on both axes)
def normalise_pixel_coords(x, y):

  gl_x = (x / config.window_x) * 2 - 1
  gl_y = 1 - (y / config.window_y) * 2

  return gl_x, gl_y

# Using Cross Product to determine whether a coordinate lies within a quad
# First we need a Cross Product function
def cross_product(p1, p2, p3):

  # Cross Product - A X B = A_x * B_y - A_y * B_x
  return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p1[1] - p3[1]) * (p2[0] - p3[0])

# Then we use it as a 'sign test' to determine intersection with area
def is_point_in_quad(point, v1, v2, v3, v4):

  # If the cross product of the vectors made from these points is less than 0, then the point is 'to the left' of the vertices
  # So if we provide the vectors in counter-clockwise order, and X-prod is all < 0, then the point must be within the area
  # Yeah linear algebra we love that shit
  b1 = cross_product(point, v1, v2) < 0
  b2 = cross_product(point, v2, v3) < 0
  b3 = cross_product(point, v3, v4) < 0
  b4 = cross_product(point, v4, v1) < 0

  # return T/F value
  return (b1 == b2) and (b2 == b3) and (b3 == b4)


# Magnitude of line between two points
def get_magnitude(v1, v2):

  return ((v2[0] - v1[0]) ** 2 + (v2[1] - v1[1]) ** 2) ** (1 / 2)

# Using magnitude to get unit vector between points
def get_unit_vector(v1, v2):

  magnitude = get_magnitude(v1, v2)

  return [(v2[0] - v1[0]) / magnitude, (v2[1] - v1[1]) / magnitude]


# Vector midpoint - useful for plotting lines on cells
def find_vector_midpoint(v1, v2):
  return [
    (v1[0] + v2[0]) / 2,
    (v1[1] + v2[1]) / 2
  ]




