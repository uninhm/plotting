import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

def coords(center, angle, length):
    x, y = center
    return (x+length*np.sin(angle), y-length*np.cos(angle))

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.grid(False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

ax.axis((-.5, .5, -.5, .5))

length = 0.20
center = (0, 0.2)
angle = 3
angular_velocity = 0
g = 9.8
delta_t = 1/60
air_res = 0.7

x, y = coords(center, angle, length)
point, = ax.plot([x], [y], 'bo')
line,  = ax.plot([center[0], x], [center[1], y])

def update(_frame):
    global angle, angular_velocity

    for i in range(20):
        new_angle = angle + angular_velocity*delta_t/20
        angular_velocity += (-air_res*angular_velocity - g/length*np.sin(angle))*delta_t/20
        angle = new_angle

    x, y = coords(center, angle, length)
    point.set_data([x], [y])
    line.set_data([center[0], x], [center[1], y])

    return (line, point)

anim = animation.FuncAnimation(fig, update, frames=600)

anim.save("test.mp4", writer=animation.FFMpegWriter(fps=60))
plt.close()
