import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

N = 1
N_FRAMES = 600

def elipse(t):
    a = 2
    b = 1
    return a*np.cos(2*np.pi*t) + 1j*b*np.sin(2*np.pi*t)

def integrate_from_0_to_1(f):
    delta_t = 0.00001
    t = 0
    res = 0
    while t < 1:
        res += f(t)*delta_t
        t += delta_t
    return res

fig, ax = plt.subplots()

ax.set_aspect("equal")

ax.axis((-2.5, 2.5, -1.5, 1.5))

t = np.linspace(0, 1, N_FRAMES)
el = elipse(t)
x = np.real(el)
y = np.imag(el)

line, = ax.plot([], [])

def update(frame):
    line.set_data(x[:frame], y[:frame])
    return line,

anim = animation.FuncAnimation(fig, update, frames=N_FRAMES)

anim.save("test.mp4", writer=animation.FFMpegWriter(fps=60))
plt.close()
