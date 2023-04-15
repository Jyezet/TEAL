from datetime import datetime
import time as tm

def gettime(): # Get current UNIX time, to display to the user when the next batch will be sent 
  year = datetime.now().year
  month = datetime.now().month
  day = datetime.now().day
  hour = datetime.now().hour
  minute = datetime.now().minute
  second = datetime.now().second
  tempvar = datetime(year, month, day, hour, minute, second)
  unix = tm.mktime(tempvar.timetuple())
  return unix
