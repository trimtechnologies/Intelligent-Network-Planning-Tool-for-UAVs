import itur
import itur.models.itu676 as itu676
import itur.models.itu835 as itu835
import numpy as np
import matplotlib.pyplot as plt

# Define atmospheric parameters

# Water vapor density (g/m3)
rho_wet = 7.5 * itur.u.g / itur.u.m**3 # Standard
rho_dry = 0 * itur.u.g / itur.u.m**3    # Dry

# Atmospheric pressure (hPa)
P = 1013.25 * itur.u.hPa

# Absolute temperature (K)
T = 15 * itur.u.deg_C

# Define frequency logspace parameters
N_freq = 1000
# Frequency(GHz)
fs = np.linspace(0, 1000, N_freq)

# Compute the attenuation values
att_wet = itu676.gamma_exact(fs, P, rho_wet, T)
att_dry = itu676.gamma_exact(fs, P, rho_dry, T)

# Plot the results
plt.figure()
plt.plot(fs, att_wet.value, 'b--', label='Wet atmosphere')
plt.plot(fs, att_dry.value, 'r', label='Dry atmosphere')
plt.xlabel('Frequency [GHz]')
plt.ylabel('Specific attenuation [dB/km]')
plt.yscale('log')
plt.xscale('linear')
plt.xlim(0, 1000)
plt.ylim(1e-3, 1e5)
plt.legend()
plt.grid(which='both', linestyle=':', color='gray', linewidth=0.3, alpha=0.5)
plt.grid(which='major', linestyle=':', color='black')
plt.title('FIGURE 1. - Specific attenuation due to atmospheric gases,\n '
          'calculated at 1 GHz intervals, including line centres')
plt.tight_layout()
plt.show()

###############################################################################
#                  Specific attenuation at different altitudes                #
###############################################################################

# Define atmospheric parameters

# Height (km)
hs = np.array([0, 5, 10, 15, 20]) * itur.u.km

# Define frequency logspace parameters
N_freq = 2001
# Frequency(GHz)
fs = np.linspace(50, 70, N_freq)

# Plot the results
plt.figure()

# Loop over heights and compute values
for h in hs:
    rho = itu835.standard_water_vapour_density(h)
    P = itu835.standard_pressure(h)
    T = itu835.standard_temperature(h)

    # estimate the specific attenuation using the line-by-line method
    # described in Annex 1 of the recommendation.
    atts = itu676.gamma_exact(fs * itur.u.GHz, P, rho, T)
    plt.plot(fs, atts.value, label='Altitude {0} km'.format(h.value))

plt.xlabel('Frequency [GHz]')
plt.ylabel('Specific attenuation [dB/km]')
plt.yscale('log')
plt.xscale('linear')
plt.xlim(50, 70)
plt.ylim(1e-3, 1e2)
plt.legend()
plt.grid(which='both', linestyle=':', color='gray', linewidth=0.3, alpha=0.5)
plt.grid(which='major', linestyle=':', color='black')
plt.title('FIGURE 2. - Specific attenuation in the range 50-70 GHz at the\n'
          ' altitudes indicated, calculated at intervals of 10 MHz\n'
          ' including line centers (0, 5, 10 15, 20) km')
plt.tight_layout()
plt.show()

###############################################################################
#               Comparison of line-by-line and approximate method             #
###############################################################################
# Define atmospheric parameters

# Elevation angle (degrees)
el = 90

# Water vapor density (g/m3)
rho = 7.5 * itur.u.g / itur.u.m**3

# Atmospheric pressure (hPa)
P = 1013.25 * itur.u.hPa

# Absolute temperature (K)
T = 15 * itur.u.deg_C

# Define frequency logspace parameters
N_freq = 350
fs = np.linspace(0, 350, N_freq)

# Loop over frequencies and compute values
atts_approx = itu676.gaseous_attenuation_slant_path(fs, el, rho, P, T,  mode='approx')
atts_exact = itu676.gaseous_attenuation_slant_path(fs, el, rho, P, T, mode='exact')

# Plot the results
plt.figure()
plt.plot(fs, atts_approx.value, 'b--', label='Approximate method Annex 2')
plt.plot(fs, atts_exact.value, 'r', label='Exact line-by-line method')
plt.xlabel('Frequency [GHz]')
plt.ylabel('Attenuation [dB]')
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.grid(which='both', linestyle=':', color='gray', linewidth=0.3, alpha=0.5)
plt.grid(which='major', linestyle=':', color='black')
plt.title('Comparison of line-by-line method to approximate method')
plt.tight_layout()
plt.show()