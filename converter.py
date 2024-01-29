from argparse import ArgumentParser

from astropy.table import Table
import numpy as np

from HDMSpectra import HDMSpectra

CIRELLI_MASSES = np.array([5, 6, 8, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220, 240, 260, 280, 300, 330, 360, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000, 1100, 1200, 1300, 1500, 1700, 2000, 2500, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12000, 15000, 20000, 30000, 50000, 100000])  # fmt: skip

CIRELLI_LOG10X = np.arange(-8.9, 0.05, 0.05)

# keys = HDMSpectra channel names
# values = PPPC4DM channel names
CHANNELS = {
    "eL": "eL",
    "eR": "eR",
    "e": "e",
    "muL": "\\[Mu]L",
    "muR": "\\[Mu]R",
    "mu": "\\[Mu]",
    "tauL": "\\[Tau]L",
    "tauR": "\\[Tau]R",
    "tau": "\\[Tau]",
    "d": "d",
    "dL": "dL",
    "dR": "dR",
    "u": "u",
    "uL": "uL",
    "uR": "uR",
    "s": "s",
    "sL": "sL",
    "sR": "sR",
    "c": "c",
    "cL": "cL",
    "cR": "cR",
    "b": "b",
    "bL": "bL",
    "bR": "bR",
    "t": "t",
    "tL": "tL",
    "tR": "tR",
    "W": "W",
    "WL": "WLeft",
    "WR": "WRight",
    "W0": "WL",
    "Z": "Z",
    "ZL": "ZLeft",
    "ZR": "ZRight",
    "Z0": "ZL",
    "g": "g",
    "gL": "gL",
    "gR": "gR",
    "gamma": "\\[Gamma]",
    "gammaL": "\\[Gamma]L",
    "gammaR": "\\[Gamma]R",
    "h": "h",
    "nue": "\\[Nu]e",
    "nueL": "\\[Nu]eL",
    "numu": "\\[Nu]\\[Mu]",
    "numuL": "\\[Nu]\\[Mu]L",
    "nutau": "\\[Nu]\\[Tau]",
    "nutauL": "\\[Nu]\\[Tau]L",
}

UNAVAILABLE_CHANNELS = [
    "q",
    "WT",
    "ZT",
    "V->e",
    "V->\\[Mu]",
    "V->\\[Tau]",
]

parser = ArgumentParser()
parser.add_argument("-o", "--output-file", required=True, help="Path to output file")
parser.add_argument("-c", "--channels", help=f"OPTIONAL: Select specific channels\n{list(CHANNELS.keys())}", nargs="+")
args = parser.parse_args()


def main(output_file, channels):
    if channels is None:
        channels = CHANNELS.keys()

    hdm_data_file = "../HDMSpectra/data/HDMSpectra.hdf5"
    mDMs = CIRELLI_MASSES
    mDMs = mDMs[mDMs > 500]  # lower limit of HDMSpectra
    log10x = CIRELLI_LOG10X[CIRELLI_LOG10X > -6] # lower limit of HDMSpectra
    log10x = np.round(log10x, decimals=2)
    x = 10**log10x
    spectra = np.zeros((len(channels), len(mDMs) * len(x)))
    for idx, ch in enumerate(channels):
        mDM_spectra = []
        for mDM in mDMs:
            dNdx = HDMSpectra.spec(
                finalstate="gamma",
                X=ch,
                xvals=x,
                mDM=mDM,
                data=hdm_data_file,
                annihilation=True,
            )
            mDM_spectra.append(dNdx)
        spectra[idx] = np.array(mDM_spectra).flatten()

    hdm_table = Table(
        [np.repeat(mDMs, len(log10x)), np.tile(log10x, len(mDMs))] + [spectrum for spectrum in spectra],
        names=["mDM", "Log[10,x]"] + [CHANNELS[ch] for ch in channels],
    )

    hdm_table.write(output_file, format="ascii.fast_basic", delimiter=" ", overwrite=True)



if __name__ == "__main__":
    main(**vars(args))
