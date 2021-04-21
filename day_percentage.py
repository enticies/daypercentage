"""

This program calculates the amount of the day that has passed in percentages.
User can determine the hours of the day. If the day has ended, the output is
a negative percentage that indicates the amount of the time that has passed 
since the end.

"""

from datetime import datetime
import sys
import argparse
import time
from multiplereplace import multipleReplace
import re

start_time = time.time()

def prepHours(start, end):
    """ Takes a starting and an ending hour in 12-hour format and returns them in 24-hour format."""
    start, end = parseInput(start, end)
    checkInput(start, end)
    table = {"am": "0", "pm":"12"}
    startAP = int(multipleReplace(table, start[-1]))
    endAP = int(multipleReplace(table, end[-1]))
    start = (int(start[0]) + startAP) * 60 + int(start[1])
    end = (int(end[0]) + endAP) * 60 + int(end[1])
    return start, end

def parseInput(start, end):
    table = {"am": " am", "pm": " pm", ":": " ", ".": " "}

    start = multipleReplace(table, start.lower()).split()
    end = multipleReplace(table, end.lower()).split()

    if len(start) == 2:
        start.insert(1, "00")
    if len(end) == 2:
        end.insert(1, "00")

    if len(start) > 1:
        if len(start[1]) == 1:
            start[1] = start[1].ljust(2, "0")
    if len(end) > 1:
        if len(end[1]) == 1:
            end[1] = end[1].ljust(2, "0")

    return start, end

def checkInput(start, end):
    endings = ["am", "pm"]
    # Check the format of the input
    if len(start) > 3 or len(end) > 3:
        print("Can't parse your input.\nExiting...")
        sys.exit(-1)
    # Check if non-integers have been entered
    if not (start[0]+start[1]).isdigit() or not (end[0]+end[1]).isdigit():
        print("Hour and minute portions must be integers.\nExiting...")
        sys.exit(-1)
    # Check if am/pm have been correctly entered
    if start[-1] not in endings or end[-1] not in endings:
        print("You need to specify AM/PM.\nExiting...")
        sys.exit(-1)
    # Check if minute portion is in correct range
    if not 0 <= int(start[1]) <= 59 or not 0 <= int(end[1]) <= 59:
        print("Minutes must be between 0 an 59.\nExiting...")
        sys.exit(-1)
    # Check if hour portion is in correct range
    if not 0 <= int(start[0]) <= 12 or not 0 <= int(end[0]) <= 12:
        print("Hours must be between 0 and 12.\nExiting...")
        sys.exit(-1)


def findDistance(start, end):
    """ Finds the distance between two given hours by counting the minutes in-between."""
    if start == end:                                                         
        return 24*60
    count = 0
    while start != end:
        if start == 24*60:
            start = 0
        else:
            count += 1
            start += 1
    return count

def findPercentage(start, end, totalHours):
    """ Calculates the percentage of the day that has gone by. (or the amount after in ended)"""
    format = "%H:%M"
    now = list(map(int, datetime.now().strftime(format).split(":")))        # get the current time 
    now = now[0] * 60 + now[1]                                              # turn it into minutes
    passedBy = findDistance(start, now)                                     # find the distance between the start and now
                                                                            
    percentage = "%"+str(round(passedBy / totalHours * 100))                    
    if passedBy > totalHours:                                               # if more hours passed have than the distance between the start and the end
        passedBy = passedBy - totalHours                                        
        percentage = round(passedBy / (24*60 - totalHours) * 100)               
        if percentage != 0:
            return "-%"+str(round(passedBy / (24*60 - totalHours) * 100))
    return "%"+str(round(passedBy / totalHours * 100))

def writeLog(start, end, execTime=None):
    logFile = open("/home/ares/Projects/daypercentage/dayleft.log", "a")

    if execTime: 
        logFile.write("Execution time: {:.6f}, Time of the day: {}, Starting hour: {}, Ending hour: {}\n".format(execTime,  
            datetime.now(), start, end))
    else:
        logFile.write("Incorrect minute. START: {}, END: {}, NOW: {}\n".format(start, end, execTime))
        logFile.close()
        sys.exit(-1)

    logFile.close()

def writeFile(outFile, percentage, execTime, start, end):
    """ Write the calculated percentage into a file."""
    outputFile = open(outFile, "w+")
    outputFile.write(percentage)
    outputFile.close()
    
    writeLog(start, end, execTime) 

def main():
    parser = argparse.ArgumentParser(exit_on_error=True)

    parser.add_argument("-f", "--file", metavar="", help="name of the output file.")
    parser.add_argument("-s", "--start", metavar="", help="starting hour.")
    parser.add_argument("-e", "--end", metavar="", help="ending hour.")
    
    args = parser.parse_args()

    start, end, file = args.start, args.end, args.file

    if not args.file:
        print("No name for the output file specified. Defaulting to 'dayleft.percentage'.")
        file = "dayleft.percentage"
    if not args.start:
        print("No start hour specified. Defaulting to 6am.")
        start = "6am"
    if not args.end:
        print("No end hour specified. Defaulting to 10pm.")
        end = "10pm"

    start, end = prepHours(start, end)
    totalHours = findDistance(start, end)

    percentage = findPercentage(start, end, totalHours)
    execTime = time.time() - start_time
    
    writeFile(file, percentage, execTime, start, end)

if __name__ == "__main__":
    main()


