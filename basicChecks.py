import numpy as np
from icecube import dataio
from datetime import datetime


def getRadioTime(frame):
    radioTime = frame["RadioTaxiTime"]
    return radioTime

def getTimeFromFilename(filename):
    dateFromFilename = filename.split("_")[-2]
    return dateFromFilename

def getROI(frame):
    roi = frame["RadioAntennaROI"]
    return roi

def getCascadingLength(frame):
    cascading = frame["RadioTraceLength"]
    return cascading

def getIds(frame):
    runid = frame["I3EventHeader"].run_id
    eventid = frame["I3EventHeader"].event_id
    return runid, eventid

def triggerType(frame):
    print("......")

def getSerDes(frame):
    serDes = frame["RadioSerdesDelay"]
    return serDes

# These should in Q-frames
class BasicChecks(self, frame):
    def __init__(self):
        self.runid = "NOTSET"
        self.evenid = "NOTSET"
        self.serDes = "NOTSET"
        self.cascadingLength = "NOTSET"
        self.dateFromI3 = "NOTSET"
        self.dateFromFilename = "NOTSET"
        self.roi = "NOTSET"

        self.getInfoFromFrame(frame)
        self.runChecksFromOneFrame(frame)

    def openLogFile(self):
    
    
    def getInfoFromFrame(self, frame):
        self.runid, self.eventid = getIds(frame)
        self.serDes = getSerDes(frame)
        self.cascadingLength = getCascadingLength(frame)
        self.roi = getROI(frame)
        self.dateFromI3 = getRadioTime(frame)

    def verifyHeader(self):
        if (self.runid <= 0) or (self.eventid <= 0):
            print("::WARNING:: Runid or eventid is broken...value: ", self.runid, self.eventid)

    def verifySerdesDelay(self):
        if (self.serDes < 0) or (self.serDes > 1000):
            print("::WARNING:: Something is fishy with the SerDes, value: ", self.serDes)

    def verifyCascadingMode(self):
        if not self.cascadingLength in [1024, 2048, 4096]:
            print("::WARNING:: Something is fishy with cascading, value: ", self.cascading)

    def verifyROI(self):
        if len(self.roi) != 3:
            print("::WARNING:: The shape for ROI is weird")
        if np.max(self.roi) > 4096:
            print("::WARNING:: ROI has a too big value, something is fishy...")

    def verifyRadioTime(frame, filename):
        ## I COULD DO SOMETHING LIKE VERIFYING WITH PREVIOUS ?? I'm not sure...
        dateFromI3 = getRadioTime(frame)
        dateFromFilename = getTimeFromFilename(filename).split("-")
        dt = datetime(int(dateFromFilename[0]), int(dateFromFilename[1]), int(dateFromFilename[2]))
        if str(dateFromI3.utc_year) != dt.strftime("%Y"):
            print("::WARNING:: The year do not fit i3file time...", str(dateFromI3.utc_year), dt.strftime("%Y"))
        # BROKEN ! TO FIX
        # if str(dateFromI3.utc_month) is not str(dt.strftime("%b")):
        #     print(len(str(dateFromI3.utc_month)), len(str(dt.strftime("%b"))))
        #     print("::WARNING:: The month do not fit i3file time...", str(dateFromI3.utc_month), str(dt.strftime("%b")))
        if int(dateFromI3.utc_day_of_month) != int(dt.strftime("%d")):
            print("::WARNING:: The day do not fit i3file time...", str(dateFromI3.utc_day_of_month), dt.strftime("%d"))

    def runChecksFromOneFrame(self):
        self.verifyHeader()
        self.verifyCascadingMode()
        # self.verifyRadioTime(frame, file)
        self.verifySerdesDelay()
        self.verifyROI()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, nargs='+', help='filenames')
    args = parser.parse_args()

    for file in args.input:
        in_file = dataio.I3File(file, "r")
        for frame in in_file:
            runChecksFromOneFrame(frame)
