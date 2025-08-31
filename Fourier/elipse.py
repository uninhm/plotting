import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

class Circle:
    def __init__(self, n, coef, parent=None):
        self.parent = parent
        self.coef = coef
        self.n = n
        if parent != None:
            self.center = parent.calc_tip(0)
        else:
            self.center = np.complex128(0, 0)
        self.patch = plt.Circle((0, 0), radius=np.abs(self.coef), fill=False)
        self.line, = plt.plot([], [])
        self.update(0)

    def calc_tip(self, t):
        return self.center + self.coef * np.exp(self.n * 2j * np.pi * t)

    def update(self, t):
        tip = self.calc_tip(t)
        self.patch.center = (self.center.real, self.center.imag)
        self.line.set_data([self.center.real, tip.real], [self.center.imag, tip.imag])

def sequence(n):
    return range(-n, n+1)

N = 1
N_FRAMES = 600

def elipse(t):
    a = 2
    b = 1
    return a*np.cos(2*np.pi*t) + 1j*b*np.sin(2*np.pi*t)

fig, ax = plt.subplots()

ax.set_aspect("equal")
ax.grid(True)

ax.axis((-2.5, 2.5, -1.5, 1.5))

t = np.linspace(0, 1, N_FRAMES)
el = elipse(t)
x = np.real(el)
y = np.imag(el)
plt.plot(x, y)

c = {}
for n in sequence(N):
    f = lambda t: np.exp(-2j*np.pi*n*t)*elipse(t)
    z = f(t)
    c[n] = np.trapezoid(z, x=t)

print(c)

line, = ax.plot([], [])
circles = []
for n in sequence(N):
    parent = circles[-1] if len(circles) > 0 else None
    circle = Circle(n, c[n], parent)
    ax.add_patch(circle.patch)
    circles.append(circle)

x, y = [], []
def update(frame):
    t = frame/N_FRAMES
    for circle in circles:
        if circle.parent != None:
            circle.center = circle.parent.calc_tip(t)
            circle.update(t)
        else:
            circle.update(t)
    x.append(circles[-1].calc_tip(t).real)
    y.append(circles[-1].calc_tip(t).imag)
    line.set_data(x, y)
    return line, *(c.patch for c in circles), *(c.line for c in circles)

anim = animation.FuncAnimation(fig, update, frames=N_FRAMES, blit=True)

anim.save("test.mp4", writer=animation.FFMpegWriter(fps=60))
plt.close()
