#!/usr/bin/env python
import sys
import os
import numpy as np
import astropy.units as u
import h5py
import your
from utils import dispersion_delay, dedisperse_array


class Radioburst:

    def __init__(
    self,
    id,
    telescope,
    fc,
    bw,
    type,
    mjdstart,
    duration,
    dt,
    df,
    tbursts,
    dm,
    widths,
    mask,
    data,
    ):

        self.id = id
        self.telescope = telescope
        self.fc = fc
        self.bw = bw
        self.type = type

        if type not in ["TotalIntensity", "FullStokes"]:
            raise ValueError("Data Type can be only either TotalIntensity or FullStokes...")

        self.mjdstart = mjdstart
        self.duration = duration
        self.dt = dt
        self.df = df
        self.tbursts = tbursts
        self.dm = dm
        self.widths = widths
        self.mask = mask
        self.data = data



        if mask.shape[0] < data.shape[1]:
            raise ValueError("The mask has to be with the same number of spectral channels...")

        if data.shape[0] > 4:
            raise ValueError("Data cannot contain more than four matricies...")

        if type in ["TotalIntensity"]:
            if data.shape[0] > 1:
                raise ValueError("Data in total intensity cannot contain more than a matrix...")

        if len(tbursts) != len(widths):
            raise ValueError("The number of arrival time of bursts must be equal to the number of widths...If widths are unknwon, set them to 0.")



    def header(self):

        string =  f"""


 Observational Specifics \n

 Telescope                        = {self.telescope}
 Central Frequency                = {self.fc.value} {self.fc.unit}
 Bandwidth                        = {self.bw.value} {self.bw.unit}
 \n
 Data Information \n

 Burst ID                         = {self.id}
 Data Type                        = {self.type}
 MJD of the 1st bin (topocentric) = {self.mjdstart}
 Data length                      = {self.duration.value} {self.duration.unit}
 Time resolution                  = {self.dt.value} {self.dt.unit}
 Frequency resolution             = {self.df.value} {self.df.unit}
 Data Shape (pols, chans, bins)   = {self.data.shape}

 Number of bursts in the data     = {len(self.tbursts.value)}
 Bursts time                      = {self.tbursts.value} {self.tbursts.unit}
 Dispersion Measure (DM)          = {self.dm.value} {self.dm.unit}
 Bursts temporal width            = {self.widths.value} {self.widths.unit}

        """

        return string


    def save(self, filename = None, outdir = None):

        if outdir is None:

            outdir =  os.getcwd()

        if filename is None:

            filename = f"{self.id}.frb"

        filename = os.path.join(outdir, filename)


        with h5py.File(filename, "w") as f:

            f.attrs["id"] = self.id
            f.attrs["telescope"] = self.telescope
            f.attrs["fc_v"] = self.fc.value
            f.attrs["fc_u"] = str(self.fc.unit)
            f.attrs["bw_v"] = self.bw.value
            f.attrs["bw_u"] = str(self.bw.unit)
            f.attrs["type"] = self.type
            f.attrs["mjdstart"] = self.mjdstart
            f.attrs["duration_v"] = self.duration.value
            f.attrs["duration_u"] = str(self.duration.unit)
            f.attrs["dt_v"] = self.dt.value
            f.attrs["dt_u"] = str(self.dt.unit)
            f.attrs["df_v"] = self.df.value
            f.attrs["df_u"] = str(self.df.unit)
            f.attrs["tburst_v"] = self.tbursts.value
            f.attrs["tburst_u"] = str(self.tbursts.unit)
            f.attrs["dm_v"] = self.dm.value
            f.attrs["dm_u"] = str(self.dm.unit)
            f.attrs["width_v"] = self.widths.value
            f.attrs["width_u"] = str(self.widths.unit)


            f.create_dataset("mask", data = self.mask, dtype = self.mask.dtype)
            f.create_dataset("data", data = self.data, dtype = self.data.dtype)


            f.close()



def ReadFile(filename):

    with h5py.File(filename, "r") as f:

        id = f.attrs["id"]
        telescope = f.attrs["telescope"]
        fc = f.attrs["fc_v"] * u.Unit(f.attrs["fc_u"])
        bw = f.attrs["bw_v"] * u.Unit(f.attrs["bw_u"])
        type = f.attrs["type"]
        mjdstart = f.attrs["mjdstart"]
        duration = f.attrs["duration_v"]  * u.Unit(f.attrs["duration_u"])
        dt = f.attrs["dt_v"] * u.Unit(f.attrs["dt_u"])
        df = f.attrs["df_v"] * u.Unit(f.attrs["df_u"])
        tbursts = f.attrs["tburst_v"] * u.Unit(f.attrs["tburst_u"])
        dm = f.attrs["dm_v"] * u.Unit(f.attrs["dm_u"])
        widths = f.attrs["width_v"] * u.Unit(f.attrs["width_u"])

        mask = np.array(f["mask"])

        data = np.array(f["data"])

        burst = Radioburst(id, telescope, fc, bw, type, mjdstart, duration, dt, df, tbursts, dm, widths, mask, data)

        return burst


def MakeFile(filename, tcand, DM, timewin, boxcar = 256, ngulp = 8192, sigma = 5, telescope = "SRT", type = "TotalIntensity", outdir = None, id = "burst", name = None):

    """

    Read a filterbank or a psrfits (this one not fully tested) file and it makes a .frb file

    param tcand : time in seconds of the candidate

    param boxcar : boxcar width of the candidate considered when the code grab the data

    param ngulp : number of spectral to consider to make the RFI excision

    param DM : DM to dedisperse the data

    param timewin : window in ms to grab the data around the burst

    """

    print("Reading File...")

    filfile = your.Your(filename)

    tsamp     = filfile.your_header.native_tsamp
    nsamp     = filfile.your_header.native_nspectra
    nchan     = filfile.your_header.native_nchans
    foff      = filfile.your_header.foff
    fch0      = filfile.your_header.fch1
    tstartobs = filfile.your_header.tstart

    bw = nchan * foff
    fc = fch0 + bw/2
    obslen = nsamp*tsamp

    freqs = np.arange(fc - bw / 2, fc + bw / 2, foff)
    times = np.linspace(0,obslen,int(nsamp))
    channels = np.arange(nchan)

    Delta_t = np.abs(dispersion_delay(freqs[-1],freqs[0], dms = candDM))

    print("Maximum dispersion delay", Delta_t , " s")


    tstart  = tcand - 1.0 * Delta_t + boxcar * tsamp
    tstop   = tcand + 1.0 * Delta_t + boxcar * tsamp


    nstart = np.rint(tstart / tsamp).astype(np.int)
    nstop  = np.rint(tstop  / tsamp).astype(np.int)
    ncand  = np.rint(tcand  / tsamp).astype(np.int)

    print("Preparing the RFI Mask...Using a Spectral Kurtosis Algorithm...")

    data = filfile.get_data(nstart = nstart, nsamp = ngulp)

    badchans = your.utils.rfi.sk_filter(data, foff, nchan, tsamp, sigma = sigma)

    print("Done.")

    print("Making the radioburst file...")

    data  = filfile.get_data(nstart = nstart, nsamp = nstop - nstart)


    data = data.T

    data = np.asarray(data , dtype = np.float32)

    dedispdata = dedisperse_array(data, DM, freqs, tsamp, ref_freq = "top")

    mjdstart = tstartobs + tstart / 24 / 3600

    times = np.linspace(0 , dedispdata.shape[1] * tsamp, dedispdata.shape[1])

    max = ncand - nstart

    tburst = times[max]


    twin = timewin * 1e-3 / 2
    win  = np.rint(twin / tsamp).astype(np.int)


    dedispdata = dedispdata[:, max - win : max + win]

    print("Grabbed dedispersed data = ", dedispdata.shape)

    dedispdata = np.array(dedispdata, dtype = np.float32)

    burst = Radioburst(id,telescope,fc * u.MHz,bw * u.MHz,type, mjdstart, times[-1] * u.s, tsamp * u.s, foff * u.MHz, tburst * u.s, DM *u.pc * u.cm**(-3), boxcar * tsamp * u.s, badchans, dedispdata)



    print("File Done! ")

    burst.save(filename = name, outdir = outdir)
