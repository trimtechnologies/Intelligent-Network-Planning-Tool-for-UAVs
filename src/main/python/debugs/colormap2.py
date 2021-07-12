import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

# generate data for sphere
from numpy import pi, meshgrid, linspace, sin, cos

th, ph = meshgrid(linspace(0, pi, 25), linspace(0, 2 * pi, 51))
x, y, z = sin(th) * cos(ph), sin(th) * sin(ph), cos(th)

# define custom colormap with fixed colour and alpha gradient
# use simple linear interpolation in the entire scale
cm.register_cmap(cmap=LinearSegmentedColormap(name='alpha_gradient1',
                 colors={'red': [(0., 0, 0),
                               (1., 0, 0)],

                       'green': [(0., 0.6, 0.6),
                                 (1., 0.6, 0.6)],

                       'blue': [(0., 0.4, 0.4),
                                (1., 0.4, 0.4)],

                       'alpha': [(0., 1, 1),
                                 (1., 0, 0)]}))

# plot sphere with custom colormap; constrain mapping to between |z|=0.7 for enhanced effect
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='alpha_gradient1', vmin=-0.7, vmax=0.7, rstride=1, cstride=1, linewidth=0.5, edgecolor='b')
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_aspect('auto')

plt.show()
