import pygame
import numpy as np

RADIUS = 10
POINT_COLOR = 'red'

def distance(a, b):
    ax, ay = a
    bx, by = b
    return np.sqrt((ax-bx)**2 + (ay-by)**2)

class Program:
    def __init__(self, width, height):
        pygame.init()

        self.window = pygame.display.set_mode((width, height))
        self.window.fill((255, 255, 255))

        self.points = []
        self.selection: int = -1
        self.already_pressed = False
        self.must_quit = False


    def run(self):
        while not self.must_quit:
            self.loop()

    def interpolate(self, a, b, t):
        x1, y1 = a
        x2, y2 = b
        return (x1*(1-t) + x2*t, y1*(1-t) + y2*t)

    def redraw(self):
        self.window.fill('white')
        if len(self.points) == 0:
            return
        for p in self.points:
            pygame.draw.circle(self.window, POINT_COLOR, p, radius=RADIUS)
        for t in np.linspace(0, 1, 1_000):
            for i in range(0, len(self.points)-2, 2):
                p1 = self.points[i]
                p2 = self.points[i+1]
                p3 = self.points[i+2]
                q1 = self.interpolate(p1, p2, t)
                q2 = self.interpolate(p2, p3, t)
                b = self.interpolate(q1, q2, t)
                pygame.draw.circle(self.window, 'black', b, radius=2)
        """ Other way
        for t in np.linspace(0, 1, 1_000):
            q = self.points
            while len(q) > 1:
                new_q = []
                for p1, p2 in zip(q, q[1:]):
                    x1, y1 = p1
                    x2, y2 = p2
                    new_q.append((x1*(1-t) + x2*t, y1*(1-t) + y2*t))
                q = new_q
            pygame.draw.circle(self.window, 'black', q[0], radius=2)
        """

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(self.points)
                self.must_quit = True

    def loop(self):
        self.handle_events()

        btn1, *_ = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if not self.already_pressed and btn1:
            self.already_pressed = True
            for i, p in enumerate(self.points):
                if distance(p, mouse_pos) <= RADIUS:
                    # If clicking a point, select it
                    self.selection = i
                    break
            else:
                # If not clicking a point, then save it and draw it
                self.points.append(mouse_pos)
                self.redraw()
        elif btn1 and self.selection != -1:
            # If point selected, move it and redraw
            self.points[self.selection] = mouse_pos
            self.redraw()
        elif not btn1:
            self.already_pressed = False
            self.selection = -1

        pygame.display.update()

if __name__ == '__main__':
    program = Program()
    program.run()
