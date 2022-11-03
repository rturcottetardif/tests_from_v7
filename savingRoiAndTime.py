import numpy as np
import basicChecks
from datetime import datetime
from icecube import dataio
import h5py

def createOutputFilename(directory=""):
    # More meaningful name ?
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    return directory + "ROIs_created_" + today_str + ".hdf5"

outputname = createOutputFilename()
print(outputname)

# Let's try to save HDF5 files 
def openH5File(outputname):
    hf = h5py.File(outputname, 'w')
    return hf

def closeH5File(hf):
    hf.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, nargs='+', help='i3 filenames')
    parser.add_argument('--outputdir', type=str, default='/data/user/rturcotte/analysis/taxiNoise/testsV7/', help="hdf5 output directory")
    args = parser.parse_args()

    outputname = createOutputFilename(directory = args.outputdir)
    hf = openH5File(outputname)
    serial_id = 0
    for file in args.input:
        in_file = dataio.I3File(file, "r")
        for frame in in_file:
            serial_id += 1
            bc = basicChecks.BasicChecks(frame)
            hf['{0}'.format(serial_id)] = serial_id
            hf['{0}'.format(serial_id)].attrs['time'] = bc.timeFromI3
            hf['{0}'.format(serial_id)].attrs['roi'] = bc.roi
            hf['{0}'.format(serial_id)].attrs['trigger'] = bc.triggerType
            # Do we want the waveforms ??? do we want some info from the waveforms... 
            # do we want runid eventid ??

    print("I saved a Hdf5 file here: ", outputname)
    closeH5File(hf)
