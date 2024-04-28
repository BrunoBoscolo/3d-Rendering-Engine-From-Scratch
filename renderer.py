# Example file showing a basic pygame "game loop"
import pygame
import matrix_processing as mp

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class line_rendering:

    def wireframe(vertex_list:list, edges:list, focal_length:int, tx: int=0, ty: int=0):
        projected_coordinates = mp.weak_perspective_projection.get_projected_list(vertex_list, focal_length)
        translated_vertex_list = mp.weak_perspective_projection.translate_vertex_list_position(tx, ty, projected_coordinates)
        for edge in edges:
            start_coordinate = translated_vertex_list[edge[0]]
            stop_coordinate = translated_vertex_list[edge[1]]
            pygame.draw.aaline(screen, 'black', start_coordinate, stop_coordinate)
    
    def wireframe_rotated(vertex_list:list, edges:list, focal_length:int, Xa:int, Ya:int, Za:int, tx: int=0, ty: int=0):
        rotated_wireframe = mp.vertex_math.get_rotated_vertices(vertex_list, Xa, Ya , Za)
        projected_coordinates = mp.weak_perspective_projection.get_projected_list(rotated_wireframe, focal_length)
        translated_vertex_list = mp.weak_perspective_projection.translate_vertex_list_position(tx, ty, projected_coordinates)
        
        for edge in edges:
            start_coordinate = translated_vertex_list[edge[0]]
            stop_coordinate = translated_vertex_list[edge[1]]
            pygame.draw.aaline(screen, 'black', start_coordinate, stop_coordinate)

class Slider:
    def __init__(self, x, y, width, height, min_value, max_value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value
        self.text = font.render("Angle: {} degrees".format(self.value), True, WHITE)
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
        slider_fill_width = (self.value - self.min_value) / (self.max_value - self.min_value) * self.width
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, slider_fill_width, self.height))
        screen.blit(self.text, (self.x + 10, self.y + self.height + 5))

    def update_value(self, new_value):
        self.value = min(max(new_value, self.min_value), self.max_value)
        self.text = font.render("Angle: {} degrees".format(int(self.value)), True, WHITE)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
                    self.dragging = True
                    # Calculate the initial value of the slider based on the mouse position
                    relative_x = mouse_x - self.x
                    new_value = (relative_x / self.width) * (self.max_value - self.min_value) + self.min_value
                    self.update_value(new_value)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, _ = event.pos
                relative_x = mouse_x - self.x
                new_value = (relative_x / self.width) * (self.max_value - self.min_value) + self.min_value
                self.update_value(new_value)


if __name__ == '__main__':
    
    # pygame setup
    pygame.init()
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()
    running = True

    vertices = [
        [0, 0, 0], [100, 0, 0], [100, 100, 0], [0, 100, 0],
        [0, 0, 100], [100, 0, 100], [100, 100, 100], [0, 100, 100]
    ]

    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [0, 4], [1, 5], [2, 6], [3, 7],
    ]

    slider_1 = Slider(100, 100, 200, 20, 0, 360)
    slider_2 = Slider(100, 300, 200, 20, 0, 360)
    slider_3 = Slider(100, 500, 200, 20, 0, 360)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            else:
                slider_1.handle_event(event)
                slider_2.handle_event(event)
                slider_3.handle_event(event)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE
        screen.fill(BLUE)
        slider_1.draw(screen)
        slider_2.draw(screen)
        slider_3.draw(screen)

        Xa = slider_1.value
        Xy = slider_2.value
        Xz = slider_3.value

        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_vertex = [mouse_x, mouse_y, 0]

        vertex_center_position = mp.polygon_math.calculate_polygon_mean_position(vertices)
        
        anglex, angley = mp.vertex_math.calculate_ray_angles(mouse_vertex, vertex_center_position)
        
        print(f'mx: {mouse_x}, my: {mouse_y}')
        print(f'Vertex center: {vertex_center_position}')
        print(f'Angle x: {anglex} Angle y: {angley}')


        #line_rendering.wireframe(vertices, edges, 50, 300, 300)
        line_rendering.wireframe_rotated(vertices, edges, 500, anglex*10, angley*10, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        line_rendering.wireframe_rotated(vertices, edges, 500, Xa, Xy, 0, SCREEN_WIDTH/3, SCREEN_HEIGHT/3)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()