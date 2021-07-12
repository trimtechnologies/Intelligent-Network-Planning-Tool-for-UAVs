import itur
import matplotlib.pyplot as plt
import numpy as np

# f = 1 * itur.u.GHz  # Link Frequency (GHz) 22.5
el = 60  # Elevation angle constant 60 degrees
rr = 30  # Rain rate (mm/h)
tau = 45  # Polarization tilt angle relative to the horizontal (degrees). Tau = 45 deg for circular polarization)

data_x = np.linspace(1, 100, 200)
data_y = []
for f in data_x:
    y = itur.models.itu838.rain_specific_attenuation(rr, f, el, tau)
    data_y.append(y.value/10)
    print(f)

plt.plot(data_x, data_y)
plt.ylabel('Specific attenuation from rain (dB/km)')
plt.xlabel('Frequency')
plt.show()