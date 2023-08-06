import numpy as np


def dispersion_delay(fstart, fstop, DM = 0):

    """
    Simply computes the delay (in seconds) due to dispersion.The output will be, respectively, a scalar or a list of delays.
    """


    delay = 4148808.0 * DM * (1 / fstart ** 2 - 1 / fstop ** 2) / 1000

    return delay

def dedisperse_array(array, DM, freq, dt, ref_freq = "top"):
    """
    Dedisperse a dynamic spectrum array accoring to a DM and a reference frequency (top, central, bottom) of the bandwidth
    """

    k_DM = 1. / 2.41e-4
    dedisp_data = np.zeros_like(array)

    # pick reference frequency for dedispersion
    if ref_freq == "top":
        reference_frequency = freq[0]
    elif ref_freq == "center":
        center_idx = len(freq) // 2
        reference_frequency = freq[center_idx]
    elif ref_freq == "bottom":
        reference_frequency = freq[-1]
    else:
        print "`ref_freq` not recognized, using 'top'"
        reference_frequency = freq[0]

    shift = (k_DM * DM * (reference_frequency**-2 - freq**-2) / dt).round().astype(int)
    for i,ts in enumerate(array):
        dedisp_data[i] = np.roll(ts, shift[i])
    return dedisp_data
