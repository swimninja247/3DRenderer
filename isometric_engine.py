import wireframe
import pygame


class ProjectionViewer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (0, 0, 0)
        self.wireframes = {}
        self.wireframe_names = []
        self.current_wireframe = 0
        self.display_nodes = True
        self.display_edges = True
        self.node_color = (255, 255, 255)
        self.edge_color = (200, 200, 200)
        self.current_node_color = (255, 0, 0)
        self.current_edge_color = (255, 50, 50)
        self.node_radius = 4

    def run(self):
        """ Create a pygame screen until it is closed.
        """
        key_commands = {
            pygame.K_LEFT: [False, lambda x: x.translate(dx=-1)],
            pygame.K_RIGHT: [False, lambda x: x.translate(dx=1)],
            pygame.K_DOWN: [False, lambda x: x.translate(dy=1)],
            pygame.K_UP: [False, lambda x: x.translate(dy=-1)],
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
        if self.current_wireframe == len(self.wireframe_names) - 1:
            self.current_wireframe = 0
        else:
            self.current_wireframe += 1

    def add_wireframe(self, name, wireframe):
        """ Add a named wireframe object.
        """
        self.wireframes[name] = wireframe
        self.wireframe_names.append(name)

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
                                           edge.start.coordinates[0:2],
                                           edge.stop.coordinates[0:2], 1)
                else:
                    for edge in frame.edges:
                        pygame.draw.aaline(self.screen, self.edge_color,
                                           edge.start.coordinates[0:2],
                                           edge.stop.coordinates[0:2], 1)

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
cube3 = wireframe.make_cube(100)
cube4 = wireframe.make_cube(100)
cube5 = wireframe.make_cube(100)
cube6 = wireframe.make_cube(100)
cube7 = wireframe.make_cube(100)
cube8 = wireframe.make_cube(100)

pv = ProjectionViewer(1158, 752)

pv.add_wireframe('cube1', cube1)
pv.add_wireframe('cube2', cube2)
pv.add_wireframe('cube3', cube3)
pv.add_wireframe('cube4', cube4)
pv.add_wireframe('cube5', cube5)
pv.add_wireframe('cube6', cube6)
pv.add_wireframe('cube7', cube7)
pv.add_wireframe('cube8', cube8)

for frame in pv.wireframes:
    pv.wireframes[frame].scale(1.1)
    print("Initialized {}".format(frame))

pv.run()
