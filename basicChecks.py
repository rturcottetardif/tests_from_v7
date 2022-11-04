import numpy as np
from icecube import dataio
from datetime import datetime

# Maybe looking if there is IceTop and scint ??

def getRadioTime(frame):
    radioTime = frame["RadioTaxiTime"]
    # That saves it in I3Time... do I want that ?
    #     time_np = np.datetime64(time.date_time)
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

def getTriggerType(frame):
    flags = frame["SurfaceFilters"]
    if flags['soft_flag'].condition_passed:
        return "soft"
    elif not flags['soft_flag'].condition_passed:
        return "scint"
        
# something like that 
def isRadio(frame):
    flags = frame["SurfaceFilters"]
    if flags['radio_data'].condition_passed:
        continue
    else:
        break


def getSerDes(frame):
    serDes = frame["RadioSerdesDelay"]
    return serDes

# These should in Q-frames
class BasicChecks():
    def __init__(self, frame):
        self.outputDir = "/data/user/rturcotte/analysis/taxiNoise/testsV7/"
        self.runid = "NOTSET"
        self.evenid = "NOTSET"
        self.serDes = "NOTSET"
        self.cascadingLength = "NOTSET"
        self.timeFromI3 = "NOTSET"
        self.timeFromFilename = "NOTSET"
        self.roi = "NOTSET"
        self.TriggerType = "NOTSET"

        self.getInfoFromFrame(frame)
        self.runChecksFromOneFrame()

    # to do .....
    def openLogFile(self):
        print("")
        f = open('log.txt', 'w')
        return f

    def closeLogFile(self):
        f.close()
    
    def getInfoFromFrame(self, frame):
        self.runid, self.eventid = getIds(frame)
        self.serDes = getSerDes(frame)
        self.cascadingLength = getCascadingLength(frame)
        self.roi = getROI(frame)
        self.dateFromI3 = getRadioTime(frame)
        self.triggerType = getTriggerType(frame)

    def verifyHeader(self):
        if (self.runid <= 0):
            print("::WARNING:: Runid is broken...value: ", self.runid)
        if (self.eventid <= 0) and (self.triggerType is not "soft"):
            print("::WARNING:: Eventid is broken, no IceTop coincidence ?...value: ", self.eventid)

    def verifySerdesDelay(self):
        if (self.serDes < 0) or (self.serDes > 1000):
            print("::WARNING:: Something is fishy with the SerDes, value: ", self.serDes)

    def verifyCascadingMode(self):
        if not self.cascadingLength in [1024, 2048, 4096]:
            print("::WARNING:: Something is fishy with cascading, value: ", self.cascading)

    def verifyROI(self):
        if len(self.roi) != 3:
            print("::WARNING:: The shape for ROI is weird")
        if self.cascadingLength == 1024:
            if np.max(self.roi) > 1024:
                print("::WARNING:: ROI has a too big value, something is fishy...")
        elif self.cascadingLength == 2048:
            if np.max(self.roi) > 2048:
                print("::WARNING:: ROI has a too big value, something is fishy...")
        elif self.cascadingLength == 4096:
            if np.max(self.roi) > 4096:
                print("::WARNING:: ROI has a too big value, something is fishy...")
        else:
            print('::WARNING:: Cascading length weird...')


    ## I COULD DO SOMETHING LIKE VERIFYING WITH PREVIOUS ?? I'm not sure what to do here....
    def verifyRadioTime(frame, filename):
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
            BasicChecks(frame)
