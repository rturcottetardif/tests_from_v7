import matplotlib.pyplot as plt
import h5py
import numpy as np

def readHDF5(filename):
    hf = h5py.File(filename, 'r')
    return hf

filename = "/data/user/rturcotte/analysis/taxiNoise/testsV7/ROIs_created_2022-11-03.hdf5"
hf_in = readHDF5(filename)

rois = []
for key in hf_in.keys():
    rois.append(hf_in[key].attrs["roi"])

plt.hist(np.asarray(rois).flatten())
plt.savefig("/data/user/rturcotte/analysis/taxiNoise/testsV7/roiHistTest.png")


# if __name__ == '__main__':
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument('input', type=str, nargs='+', help='hdf5 filenames')
#     parser.add_argument('--outputdir', type=str, default='/data/user/rturcotte/analysis/taxiNoise/testsV7/', help="plot output directory")
#     args = parser.parse_args()

# here plotting of the npz files

# Read npz file
# plot hist rois
# plot rate events (soft and scint)
# ....