from matplotlib.lines import Line2D
import numpy as np
from interactive_drawing import Program
import time
import pygame
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

class Circle:
    def __init__(self, n, coef, parent=None):
        self.parent = parent
        self.coef = coef
        self.n = n
        self.color = tuple(np.random.randint(256) for _ in range(3))
        if parent != None:
            self.center = parent.calc_tip(0)
        else:
            self.center = np.complex128(0, 0)

    def calc_tip(self, t):
        return self.center + self.coef * np.exp(self.n * 2j * np.pi * t)

def sequence(n):
    yield 0
    for i in range(1, n+1):
        yield i
        yield -i

N = 100
SIZE = 600
LINE_WIDTH = 5

# This program will let the user draw some Bezier curves
program = Program(SIZE, SIZE)
program.run()
max_time = (len(program.points) - 1) // 2

# This function just gives you a point in the curve(s) for any time t
@np.vectorize
def drawing(t):
    t = max_time*t
    n = int(t) % max_time
    p1 = program.points[2*n]
    p2 = program.points[2*n+1]
    p3 = program.points[2*n+2]
    q1 = program.interpolate(p1, p2, t - np.floor(t))
    q2 = program.interpolate(p2, p3, t - np.floor(t))
    b = program.interpolate(q1, q2, t - np.floor(t))
    x, y = b
    return x + 1j*y

t = np.linspace(0, 1, 1_000, endpoint=False)

# We calculate the Fourier transform
c = {}
for n in sequence(N):
    f = lambda t: np.exp(-2j*np.pi*n*t)*drawing(t)
    c[n] = np.trapezoid(f(t), x=t)

# We create a circle for each frequency between -N and N with the coefficient given by the transform
circles = []
for n in sequence(N):
    parent = circles[-1] if len(circles) > 0 else None
    circle = Circle(n, c[n], parent)
    circles.append(circle)

# Save the animation to a file using matplotlib
def save_animation():
    N_FRAMES = 600

    fig, ax = plt.subplots()

    ax.set_aspect("equal")
    ax.grid(True)

    ax.axis((0, 600, 0, 600))
    ax.yaxis.set_inverted(True)

    line, = ax.plot([], [])
    patch_dict: dict[int, patches.Circle] = {}
    line_dict: dict[int, Line2D] = {}
    for circle in circles:
        n = circle.n
        patch = patches.Circle((0, 0), radius=np.abs(circle.coef), fill=False)
        line, = plt.plot([0, 0], [0, 0])
        ax.add_patch(patch)
        patch_dict[n] = patch
        line_dict[n] = line

    x, y = [], []
    def update(frame):
        t = frame/N_FRAMES
        for circle in circles:
            if circle.parent != None:
                circle.center = circle.parent.calc_tip(t)
            patch_dict[circle.n].center = (circle.center.real, circle.center.imag)
            tip = circle.calc_tip(t)
            line_dict[circle.n].set_data([circle.center.real, tip.real], [circle.center.imag, tip.imag])
        x.append(circles[-1].calc_tip(t).real)
        y.append(circles[-1].calc_tip(t).imag)
        line.set_data(x, y)
        return line, *patch_dict.values(), *line_dict.values()

    anim = animation.FuncAnimation(fig, update, frames=N_FRAMES, blit=True)

    anim.save("test.mp4", writer=animation.FFMpegWriter(fps=60))
    plt.close()


# Then we animate the graph with pygame
window = program.window
program.must_quit = False
start = time.time()
line = []
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)
while not program.must_quit:
    program.handle_events()

    t = (time.time() - start)/10

    # Animate the circles
    window.fill('white')
    for c in circles:
        if c.parent != None:
            c.center = c.parent.calc_tip(t)
        x = c.center.real
        y = c.center.imag
        pygame.draw.circle(window, 'black', (x, y), np.abs(c.coef), 2)
        text = font.render(str(c.n), False, (0,0,0))
        window.blit(text, (x, y))
        tip = c.calc_tip(t)
        pygame.draw.line(window, c.color, (x, y), (tip.real, tip.imag), LINE_WIDTH)
    tip = circles[-1].calc_tip(t)
    line.append((tip.real, tip.imag))
    for p in line:
        pygame.draw.circle(window, 'green', p, 1)

    # Display a button at the bottom right corner
    ww, wh = window.get_size()
    rw, rh = (100, 50)
    btn = pygame.draw.rect(window, 'red', (ww-rw, wh-rh, rw, rh))

    # Center the text in the button
    text = font.render('Save', False, 'white')
    tw, th = text.get_size()
    window.blit(text, (ww-rw//2-tw//2, wh-rh//2-th//2))

    # If button clicked save the save the animation with matplotlib
    mouse_clicked, *_ = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if mouse_clicked and btn.contains(mouse_pos, (0,0)):
        save_animation()

    pygame.display.update()
