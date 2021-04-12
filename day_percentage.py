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

start_time = time.time()

def prepHours(start, end):
    """ Takes a starting and an ending hour in 12-hour format and returns them in 24-hour format."""
    try:
        hours = list(map(float, "{} {}".format(start, end).replace("am", " 0")
                    .replace("pm", " 12").replace(":", ".").split()))                   # replace am/pm with 0 and 12 respectively,
                                                                                        # return a list of integers. First two
                                                                                        # containing the starting hour, the last two
                                                                                        # the ending hour.
    except:
        print("Can't understand your input.\nExiting...")
        sys.exit(-1)

    startList = list(map(int, str(sum(hours[:2:])).split(".")))             # convert starting hour to 24-hour format
                                                                            # by summing the first two integers in the
                                                                            # list.
    endList = list(map(int, str(sum(hours[2::])).split(".")))               # convert the ending hour by doing the same.
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
    if passedBy > totalHours:                                               # if more hours have passed than the distance
                                                                            # between the start and the end 
        passedBy = passedBy - totalHours                                        
        percentage = round(passedBy / (24*60 - totalHours) * 100)               
        if percentage != 0:
            return "-%"+str(round(passedBy / (24*60 - totalHours) * 100))
    return "%"+str(round(passedBy / totalHours * 100))

def writeFile(outFile, percentage, exec_time, start, end):
    """ Write the calculated percentage into a file."""
    outputFile = open(outFile, "w+")
    time_file = open("/home/ares/Projects/daypercentage/dayleft.log", "a")

    outputFile.write(percentage)
    outputFile.close()

    time_file.write("Execution time: {:.6f}, Time of the day: {}, Starting hour: {}, Ending hour: {}{}".format(exec_time,
        datetime.now(), start, end, "\n"))
    time_file.close()
    

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
    exec_time = time.time() - start_time
    
    writeFile(file, percentage, exec_time, start, end)

if __name__ == "__main__":
    main()


