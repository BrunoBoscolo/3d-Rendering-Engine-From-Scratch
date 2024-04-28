import numpy as np
from math import *

class polygon_math:

    def calculate_polygon_mean_position(vertex_list):
        vertices_array = np.array(vertex_list)

        # Calculate the center coordinate
        center_coordinate = np.mean(vertices_array, axis=0)

        return tuple(center_coordinate)

class vertex_math:
    
    def apply_3d_rotation_matrix(x_angle: int, y_angle: int, z_angle: int, vertex: list[int,int,int]) -> list:
        cos_x = cos(radians(x_angle))
        cos_y = cos(radians(y_angle))
        cos_z = cos(radians(z_angle))

        sin_x = sin(radians(x_angle))
        sin_y = sin(radians(y_angle))
        sin_z = sin(radians(z_angle))

        rotation_matrix = np.array([
            [cos_y*cos_z,                      -cos_y*sin_z,                      sin_y],
            [sin_x*sin_y*cos_z+cos_x*sin_z, cos_x*cos_z-sin_x*sin_y*sin_z, -sin_x*cos_y],
            [-cos_x*sin_y*cos_z+sin_x*sin_z, cos_x*sin_y*sin_z+sin_x*cos_z, cos_x*cos_y]
        ])

        coordinates = np.dot(rotation_matrix, np.array(vertex))
    
        return coordinates.tolist()
    
    def get_rotated_vertices(vertex_list:list, x_angle:int, y_angle:int, z_angle:int) -> list:
            rotated_list = []
            for vertex in vertex_list:
                rotated_list.append(vertex_math.apply_3d_rotation_matrix(x_angle, y_angle, z_angle, vertex))

            return rotated_list
    
    def calculate_ray_angles(vertex_a:list[int,int,int], vertex_b:list[int,int,int]):

        xA, yA, zA = vertex_a
        xB, yB, zB = vertex_b

        distance = abs(zB-zA)

        deltax = xB-xA
        deltay = yB-yA

        theta_xy = atan2(deltax, distance)
    
        # Calculate the angle in the X-Z plane
        theta_xz = atan2(deltay, distance)
        
        return theta_xy, theta_xz

    def get_vertex_deviation_angles(reference_vertex:list[int,int,int], vertex_list:list):
        deviated_angles = []
        for vertex in vertex_list:
            deviated_angle_x, deviated_angle_y = vertex_math.calculate_ray_angles(reference_vertex, vertex)
            deviated_angles.append([deviated_angle_x,deviated_angle_y])

class weak_perspective_projection:

    def translate_vertex_list_position(x:int, y:int, vertex_list: list[int,int]) -> list:
        translated_list = []
        for vertex in vertex_list:
            x0, y0 = vertex
            x1 = x0+x
            y1 = y0+y
            translated_list.append([x1,y1])
        return translated_list

    def calculate_x_intersection_point(x_coordinate:int, z_coordinate:int, focal_length:int) -> int:
        x_projected = (focal_length*x_coordinate)/(focal_length+z_coordinate)
        return x_projected

    def calculate_y_intersection_point(y_coordinate:int, z_coordinate:int, focal_length:int) -> int:
        y_projected = (focal_length*y_coordinate)/(focal_length+z_coordinate)
        return y_projected
    
    def get_projected_coordinates(vertex: list[int, int, int], focal_length:int) -> list[int, int]:
        x, y, z = vertex

        x_projected = weak_perspective_projection.calculate_x_intersection_point(x, z, focal_length)
        y_projected = weak_perspective_projection.calculate_y_intersection_point(y, z, focal_length)

        return [x_projected, y_projected]
    
    def get_projected_list(vertex_list:list, focal_length:int) -> list:
        projected_list = []
        for vertex in vertex_list:
            projected_list.append(weak_perspective_projection.get_projected_coordinates(vertex, focal_length))

        return projected_list

    

    
    