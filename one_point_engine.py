import wireframe
import pygame
import numpy as np

""" make it so
"""


class ProjectionViewer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (0, 0, 0)
        self.wireframes = {'camera': 'camera'}
        self.wireframe_names = ['camera']
        self.current_wireframe = 0
        self.display_nodes = True
        self.display_edges = True
        self.node_color = (255, 255, 255)
        self.edge_color = (200, 200, 200)
        self.current_node_color = (255, 0, 0)
        self.current_edge_color = (255, 50, 50)
        self.node_radius = 4
        self.fov = 1000
        self.camera_coord = np.array([width/2, height/2])

    def run(self):
        """ Create a pygame screen until it is closed.
        """
        key_commands = {
            pygame.K_LEFT: [False, lambda x: x.translate(dx=-1)],
            pygame.K_RIGHT: [False, lambda x: x.translate(dx=1)],
            pygame.K_DOWN: [False, lambda x: x.translate(dy=1)],
            pygame.K_UP: [False, lambda x: x.translate(dy=-1)],
            pygame.K_RETURN: [False, lambda x: x.translate(dz=1)],
            pygame.K_RSHIFT: [False, lambda x: x.translate(dz=-1)],
            pygame.K_EQUALS: [False, lambda x: x.scale(1.001)],
            pygame.K_MINUS: [False, lambda x: x.scale(0.999)],
            pygame.K_w: [False, lambda x: x.rotate_x(0.01)],
            pygame.K_s: [False, lambda x: x.rotate_x(-0.01)],
            pygame.K_a: [False, lambda x: x.rotate_y(0.01)],
            pygame.K_d: [False, lambda x: x.rotate_y(-0.01)]}
        running = True
        print(self.current_wireframe)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_commands:
                        key_commands[event.key][0] = True
                    elif event.key == pygame.K_TAB:
                        self.cycle_selection()
                elif event.type == pygame.KEYUP:
                    if event.key in key_commands:
                        key_commands[event.key][0] = False
            for key in key_commands:
                if key_commands[key][0]:
                    key_commands[key][1](
                        self.wireframes[self.wireframe_names[
                            self.current_wireframe]])
            self.display()
            pygame.display.flip()

    def cycle_selection(self):
        """ Changes current selection to next in dictionary.
        """
        if self.current_wireframe == len(self.wireframe_names) - 1:
            self.current_wireframe = 0
        else:
            self.current_wireframe += 1

    def add_wireframe(self, name, wireframe):
        """ Add a named wireframe object to the dictionary.
        """
        self.wireframes[name] = wireframe
        self.wireframe_names.append(name)

    def render(self, node):
        rendered = node.coordinates[0:2] * self.fov / node.coordinates[2]
        rendered += self.camera_coord
        return rendered

    def display(self):
        """ Draw wireframes to screen.
        """

        self.screen.fill(self.background)

        for frame in self.wireframes.values():
            if self.display_edges:
                if frame == self.wireframes[self.wireframe_names[
                            self.current_wireframe]]:
                    for edge in frame.edges:
                        pygame.draw.aaline(self.screen,
                                           self.current_edge_color,
                                           self.render(edge.start),
                                           self.render(edge.stop), 1)
                else:
                    for edge in frame.edges:
                        pygame.draw.aaline(self.screen, self.edge_color,
                                           self.render(edge.start),
                                           self.render(edge.stop), 1)

            if self.display_nodes:
                if frame == self.wireframes[self.wireframe_names[
                            self.current_wireframe]]:
                    for node in frame.nodes:
                        pygame.draw.circle(self.screen,
                                           self.current_node_color,
                                           [int(i) for i in node.coordinates[
                                               :2]],
                                           self.node_radius, 0)
                else:
                    for node in frame.nodes:
                        pygame.draw.circle(self.screen, self.node_color,
                                           [int(i) for i in node.coordinates[
                                               :2]],
                                           self.node_radius, 0)


cube1 = wireframe.make_cube(100)
cube2 = wireframe.make_cube(100)
pv = ProjectionViewer(1158, 752)
pv.display_nodes = False
pv.add_wireframe('cube1', cube1)
pv.add_wireframe('cube2', cube2)

for frame in pv.wireframes:
    if isinstance(frame, wireframe.Wireframe):
        pv.wireframes[frame].scale(1.1)
    print("Initialized {}".format(frame))

pv.run()
