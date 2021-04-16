import os

def runGalenTest():
    os.system('command galen test ./Layout/layoutCheck.test --htmlreport "./Layout/report"')

#runGalenTest()