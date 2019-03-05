#!/usr/bin/env python

import time
from datetime import datetime

try:
    import unicornhathd as unicorn
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicorn

unicorn.brightness(0.2)
unicorn.off()

y1 = [datetime.strptime("19:00:00","%H:%M:%S").time()] * 7
r1 = [datetime.strptime("20:00:00","%H:%M:%S").time()] * 7
g1 = [datetime.strptime("07:00:00","%H:%M:%S").time()] * 7
o1 = [datetime.strptime("08:30:00","%H:%M:%S").time()] * 7

g1[0] = g1[6] = datetime.strptime("08:00:00","%H:%M:%S").time()

#print g1

old_display = "off"

digit = [["***", "* *","* *", "* *","***"],
         ["  *","  *","  *","  *","  *"],
         ["***","  *","***","*  ","***"],
         ["***","  *","***","  *","***"],
         ["* *","* *","***","  *","  *"],
         ["***","*  ","***","  *","***"],
         ["***","*  ","***","* *","***"],
         ["***","  *","  *","  *","  *"],
         ["***","* *","***","* *","***"],
         ["***","* *","***","  *","***"]]

def displayNumber(x,y,d):
   for i in  digit[d]:
      for j in range(3):
         r,g,b = (255,255,255) if i[j] == "*" else (0,0,0)
         unicorn.set_pixel(x+j, y, r, g, b)
      y-=1
   unicorn.show()

def nightlight():
   global old_display
   now = datetime.now().time()
   week_day = getTimeParts('%w')[0]

   if now >= g1[week_day] and now < o1[week_day]: 
      r,g,b = 0,255,0
      display = "green"
   elif now >= y1[week_day] and now < r1[week_day]:
      r,g,b = 255,255,0
      display = "yellow"
   elif now >= r1[week_day]  or now < g1[week_day]:
      r,g,b = 255,0,0
      display = "red"
   else:
      r,g,b = 0,0,0
      display = "off"

   if display != old_display:
      old_display = display
      for y in range(5, 11):
         for x in range(0, 16):
            unicorn.set_pixel(x, y, r, g, b)

def displayTimeDots(x, y):
  r,g,b = (128,0,128) if int(getTimeParts('%S')[1])%2 == 0 else (0,0,0)
  unicorn.set_pixel(x, y-1, r, g, b)
  unicorn.set_pixel(x, y-3, r, g, b)
  unicorn.show()

def displayDateDots(x, y):
  r,g,b = 128,0,128
  unicorn.set_pixel(x+1, y, r, g, b)
  unicorn.set_pixel(x+1, y-1, r, g, b)
  unicorn.set_pixel(x+1, y-2, r, g, b)
  unicorn.set_pixel(x, y-2, r, g, b)
  unicorn.set_pixel(x, y-3, r, g, b)
  unicorn.set_pixel(x, y-4, r, g, b)
  unicorn.show()

# Gets a specific part of the current time, passed to strftime, then it is
# split into its individual numbers and converted into integers. Used to feed
# the display with numbers
def getTimeParts(timePart):
  parts = datetime.now().strftime(timePart)
  return [int(x) for x in parts]

displayedHourParts = getTimeParts('%H')
displayedMinuteParts = getTimeParts('%M')
displayedMonthParts = getTimeParts('%m')
displayedDayParts = getTimeParts('%d')

# Display Current Time
displayNumber(0,15, displayedHourParts[0])
displayNumber(4,15, displayedHourParts[1])
displayTimeDots(7,15)
displayNumber(9,15, displayedMinuteParts[0])
displayNumber(13,15, displayedMinuteParts[1])

# Display Day and Month
displayNumber(0,4, displayedDayParts[0])
displayNumber(4,4, displayedDayParts[1])
displayDateDots(7,4)
displayNumber(9,4, displayedMonthParts[0])
displayNumber(13,4, displayedMonthParts[1])

nightlight()

try:
  while True:
    hourParts = getTimeParts('%H')
    minuteParts = getTimeParts('%M')
    dayParts = getTimeParts('%d')
    monthParts = getTimeParts('%m')

    # TIME Details
    # Only update first hour number if it is different to what is currently displayed
    if hourParts[0] != displayedHourParts[0]:
      displayedHourParts[0] = hourParts[0]
      displayNumber(0,15, hourParts[0])

    # Only update second hour number if it is different to what is currently displayed
    if hourParts[1] != displayedHourParts[1]:
      displayedHourParts[1] = hourParts[1]
      displayNumber(4,15, hourParts[1])

    # Only update first minute number if it is different to what is currently displayed
    if minuteParts[0] != displayedMinuteParts[0]:
      displayedMinuteParts[0] = minuteParts[0]
      displayNumber(9,15, minuteParts[0])

    # Only update second minute number if it is different to what is currently displayed
    if minuteParts[1] != displayedMinuteParts[1]:
      displayedMinuteParts[1] = minuteParts[1]
      displayNumber(13,15, minuteParts[1])

    # MONTH Details
    # Only update first day number if it is different to what is currently displayed
    if dayParts[0] != displayedDayParts[0]:
      displayedDayParts[0] = dayParts[0]
      displayNumber(0,4, dayParts[0])

    # Only update second day number if it is different to what is currently displayed
    if dayParts[1] != displayedDayParts[1]:
      displayedDayParts[1] = dayParts[1]
      displayNumber(4,4, dayParts[1])

    # Only update first month number if it is different to what is currently displayed
    if monthParts[0] != displayedMonthParts[0]:
      displayedMonthParts[0] = monthParts[0]
      displayNumber(9,4, monthParts[0])

    # Only update second month number if it is different to what is currently displayed
    if monthParts[1] != displayedMonthParts[1]:
      displayedMonthParts[1] = monthParts[1]
      displayNumber(13,4, monthParts[1])

    displayTimeDots(7,15)

    nightlight()

    unicorn.show()
    # Sleep for 0.5 because the display doesn't need to update that often
    time.sleep(0.5)
except KeyboardInterrupt:
  unicorn.off()
