from time import time

from .tools import get_magnitude, get_unit_vector

import config

last_snapped_time = time()

# Update all object positions based on paths, velocities, last positions, and time elapsed
def update_object_positions():
    global last_snapped_time

    for object in config.objects:

        # Store the stuff I need - just makes the next steps easier
        current_position = object['lastKnownPosition']
        current_segment = object['lastKnownSegment']
        current_height = object['lastKnownHeight']
        path = object['path']
        height_path = object['height']
        speed = object['speed']
        n_points = len(path)


        # First, let's see if this object needs to be rendered on the next path segment
        dist_left_current_segment = get_magnitude(current_position, path[(current_segment + 1) % n_points])
        height_change_left_current_segment = height_path[(current_segment + 1) % n_points] - current_height
        dist_to_travel = (time() - last_snapped_time) * speed

        # Case 1: this increment will keep the object along the current path segment
        if dist_to_travel <= dist_left_current_segment:
            unit_vector = get_unit_vector(current_position, path[(current_segment + 1) % n_points])
            object['lastKnownPosition'] = [
                current_position[0] + unit_vector[0] * dist_to_travel,
                current_position[1] + unit_vector[1] * dist_to_travel
            ]
            # Incrementing height by the % of the path left which is being travelled
            object['lastKnownHeight'] += height_change_left_current_segment * (dist_to_travel / dist_left_current_segment)
        
        # Case 2: this increment completes a segment and needs to roll to the next one
        else:
            # Increment segment integer by 1 (within base of # coordinates)
            current_segment = (current_segment + 1) % n_points
            # Assume last segment complete - subtract the dist left in current segment from the dist to travel
            dist_to_travel -= dist_left_current_segment
            # New start point - start of next segment
            next_segment_start = path[current_segment]
            # New unit vector - for next segment
            unit_vector = get_unit_vector(next_segment_start, path[(current_segment + 1) % n_points])

            object['lastKnownPosition'] = [
                next_segment_start[0] + unit_vector[0] * dist_to_travel,
                next_segment_start[1] + unit_vector[1] * dist_to_travel,
            ]
            # In order to do height, need to calculate % of next path we are going to travel, and apply to the height delta
            dist_next_segment = get_magnitude(next_segment_start, path[(current_segment + 1) % n_points])
            height_change_next_segment = height_path[(current_segment + 1) % n_points] - height_path[current_segment]
            object['lastKnownHeight'] = height_path[current_segment] + height_change_next_segment * (dist_to_travel / dist_next_segment)

            # Update object to ensure it knows it's on the next segment
            object['lastKnownSegment'] = current_segment

    # Update last_snapped_time after all objects are processed
    last_snapped_time = time()
