import numpy as np
import basicChecks
from datetime import datetime

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('input', type=str, nargs='+', help='filenames')
# args = parser.parse_args()

output = "/data/user/rturcotte/analysis/taxiNoise/testsV7/"

def createOutputFilename():
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    return "ROIs_created_" + today_str + ".npz"

outputname = createOutputFilename()
print(outputname)
# basicChecks.runChecksFromOneFrame(frame)
# roi = basicChecks.getROI(frame)
# time = basicChecks.getRadioTime(frame)

# other file... plot histogram ROIs and dts