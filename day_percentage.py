"""

This program calculates the amount of the day that has passed in percentages.
User can determine the hours of the day. If the day has ended, the output is
a negative percentage that indicates the amount of the time that has passed 
since the end.

"""

from datetime import datetime
import sys

def prepHours(start, end):
    """ Takes a starting and an ending hour in 12-hour format and returns them in 24-hour format."""
    try:
        hours = list(map(float, "{} {}".format(start, end).replace("am", " 0")
                    .replace("pm", " 12").replace(":", ".").split()))                   # replace am/pm with 0 and 12 respectively,
                                                                                        # return a list of integers. First two
                                                                                        # containing starting hours, the last two
                                                                                        # the ending hours.
    except:
        print("Can't understand your input.\nExiting...")
        sys.exit(-1)

    startList = list(map(int, str(sum(hours[:2:])).split(".")))   # convert starting hour to 24-hour format
                                                                            # by summing the first two integers in the
                                                                            # list.
    endList = list(map(int, str(sum(hours[2::])).split(".")))     # convert the ending hour by doing the same.
    checkValues(startList, endList)
    start = startList[0] * 60 + int(str(startList[1]).ljust(2, "0"))        # convert starting hour into minutes
    end = endList[0] * 60 + int(str(endList[1]).ljust(2, "0"))              # converts ending hour into minutes
    return start, end

def checkValues(startList, endList):
    if not 0 <= startList[0] <= 24 or not 0 <= endList[0] <= 24:
        print("Hours must be between 0 and 12.\nExiting...")
        sys.exit(-1)
    if not 0 <= startList[1] <= 59 or not 0 <= endList[1] <= 59:
        print("Minutes must be between 0 and 59.\nExiting...")
        sys.exit(-1)
    return

def getHours(start="6am", end="10pm"):
    """ Returns starting, ending hours and the distance between the two in minutes"""
    start, end = prepHours(start, end)
    totalHours = findDistance(start, end)
    return start, end, totalHours

def findDistance(start, end):
    """ Finds the distance between two given hours by counting the minutes in-between."""
    if start == end:                                                         
        return 24*60
    count = 0
    while start != end:
        if start == 24*60:
            start = 0
        count += 1
        start += 1
    return count

def findPercentage(start, end, totalHours):
    """ Calculates the percentage of the day that has gone by. (or the amount after in ended)"""
    format = "%H:%M"
    now = list(map(int, datetime.now().strftime(format).split(":")))        # get the current time 
    now = now[0] * 60 + now[1]                                              # turn it into minutes
    passedBy = findDistance(start, now)                                     # find the distance between the start
                                                                            # and now
    percentage = "%"+str(round(passedBy / totalHours * 100))                    
    if passedBy > totalHours:                                               # if more hours passed have than the distance
                                                                            # between the start and the end 
        passedBy = passedBy - totalHours                                        
        percentage = round(passedBy / (24*60 - totalHours) * 100)               
        if percentage != 0:
            return "-%"+str(round(passedBy / (24*60 - totalHours) * 100))
    return "%"+str(round(passedBy / totalHours * 100))

def writeFile(outFile, percentage):
    """ Write the calculated percentage into a file."""
    outputFile = open(outFile, "w+")

    outputFile.write(percentage)

if __name__ == "__main__":
    if len(sys.argv) > 4:
        print("Too many values to unpack.")
        sys.exit(-1)
    elif len(sys.argv) == 4:
        outFile, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
        start, end, totalHours = getHours(start, end)
    elif len(sys.argv) == 3:
        print("Too few values to unpack.")
        sys.exit(-1)
    elif len(sys.argv) == 1:
        print("You didn't enter an output file name.")
        sys.exit(-1)
    else:
        outFile = sys.argv[1]
        start, end, totalHours = getHours()

    percentage = findPercentage(start, end, totalHours)

    writeFile(outFile, percentage)
