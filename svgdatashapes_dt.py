#
# SVGdatashapes_dt  0.3.6   SVGdatashapes.com    github.com/pepprseed/svgdatashapes
# Copyright 2016-8  Stephen C. Grubb   stevegrubb@gmail.com      MIT License
#
# This module provides date / time support for svgdatashapes
#


import svgdatashapes
from svgdatashapes import p_dtformat 
import collections
import datetime as d
import time
import calendar    

class AppDt_Error(Exception): pass



def dateformat( format=None ):
    # set the format string to be used for parsing datetimes found in the input data
    # format codes explained here: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    # Note that when they say zero-padded this refers to output only; parsing can handle eg. 3/4/2015
    global p_dtformat
    if format == None: raise AppDt_Error( "dateformat() expecting 'format' arg" )
    p_dtformat = format
    return True


def toint( dateval=None ):
    # for the given date/time string in whatever format, return the int utime value
    # toint( "1970-01-01.00:00" ) == 0
    if dateval == None: return None
    try:
        tt = d.datetime.strptime( dateval, p_dtformat ).timetuple()      # parse out the components
        utime = calendar.timegm( tt )
    except: raise AppDt_Error( "toint() got bad datetime value: " + str(dateval) + " (expecting format of " + p_dtformat + ")" )
    return utime 


def make( utime, fmt=None ):
    # format the given dt value as per fmt...
    if utime == None: return None
    if fmt == None: fmt = p_dtformat
    try:
        # tt = time.gmtime( utime )
        outstr = d.datetime.utcfromtimestamp(utime).strftime( fmt )
    except: raise AppDt_Error( "nicedt error on utime: " + str(utime) + " and format: " + p_dtformat )
    return outstr


def datediff( val1, val2, result="days" ):
    # return integer number of days difference (dt1 - dt2)
    try: dt1 = d.datetime.strptime( val1, p_dtformat )
    except: raise AppDt_Error( "datediff() invalid val1 arg: " + str(val1) )
    try: dt2 = d.datetime.strptime( val2, p_dtformat )
    except: raise AppDt_Error( "datediff() invalid val2 arg: " + str(val2) )
    if result != "seconds":
        dt1 = dt1.replace( second=0, microsecond=0 )
        dt2 = dt2.replace( second=0, microsecond=0 )

    if result == "days": 
        dt1 = dt1.replace( hour=0, minute=0 )
        dt2 = dt2.replace( hour=0, minute=0 )
        div = 86400
    elif result == "hours": 
        dt1 = dt1.replace( minute=0 )
        dt2 = dt2.replace( minute=0 )
        div = 3600
    elif result == "minutes": div = 60
    elif result == "seconds": div = 1
    return int(calendar.timegm( dt1.timetuple() ) - calendar.timegm( dt2.timetuple() ) ) / div


def daterange( column=None, datarows=None, nearest=None, inc=None, stubformat=None, 
             inc2=None, stub2format=None, stub2place="append", stub2first=True ):

    dfindex = svgdatashapes._getdfindex( column, datarows )

    if nearest == None: raise AppDt_Error( "findrange() requires a nearest= arg " )
    if inc == None: inc = nearest
    # if inc != nearest:
    #    if nearest == "year" and inc == "month": pass
    #    elif nearest == "month" and inc == "day": pass
    #    elif nearest == "day" and inc == "hour": pass
    #    else: raise AppDt_Error( "findrange() invalid nearest= and inc= combination" )

    if stubformat == None: stubformat = p_dtformat

    # find raw min and max
    dmin = 999999999999999999999999999; dmax = -999999999999999999999999999; 
    for row in datarows:
        if dfindex == -1:  strval = row[column]   # dict rows
        else:  strval = row[dfindex]

        utime = toint( strval )
        if utime < dmin: dmin = utime
        if utime > dmax: dmax = utime

    dtmin = d.datetime.utcfromtimestamp( dmin ).replace( second=0, microsecond=0 )      # always zero out seconds and ms
    dtmax = d.datetime.utcfromtimestamp( dmax ).replace( second=0, microsecond=0 )
    if nearest[-6:] != "minute": dtmin.replace( minute=0 ); dtmax.replace( minute=0 )   # usually zero out minutes


    if nearest == "year":
        dtmin = dtmin.replace( month=1, day=1, hour=0 )
        yr = dtmax.year;
        dtmax = dtmax.replace( year=yr+1, month=1, day=1, hour=0 )

    elif nearest == "3month":
        newmon = ((dtmin.month / 4) * 3) + 1
        dtmin = dtmin.replace( month=newmon, day=1, hour=0 )
        newmon = (((dtmax.month / 4)+1) * 3) + 1
        yr = dtmax.year
        if newmon >= 12: newmon = 1; yr += 1;
        dtmax = dtmax.replace( year=yr, month=newmon, day=1, hour=0 )

    elif nearest == "month":   
        dtmin = dtmin.replace( day=1, hour=0 )
        mon = dtmax.month; yr = dtmax.year;
        if mon == 12: dtmax = dtmax.replace( year=yr+1, month=1, day=1, hour=0 )
        else:         dtmax = dtmax.replace( month=mon+1, day=1, hour=0 )

    elif nearest == "week" or nearest[:8] == "week_day":   # week = Monday-based week; or week_dayN where N=1 for Tues; N=6 for Sun, etc
        wday = time.gmtime( dmin ).tm_wday   # struct_time tm_wday convention is that 0 = monday 
        dmin -= (wday*86400)                 # move timestamp back by necessary no. of days to reach opening week boundary (86400 sec per day)
        if nearest[:8] == "week_day": dmin -= ((7 - int(nearest[-1:])) * 86400)
        dtmin = d.datetime.utcfromtimestamp( dmin ).replace( hour=0 )

        wday = 7 - time.gmtime( dmax ).tm_wday
        dmax += (wday*86400)                 # move timestamp fwd by necessary no. of days to reach the next week boundary
        if nearest[:8] == "week_day": dmax += ((7 - int(nearest[-1:])) * 86400)
        dtmax = d.datetime.utcfromtimestamp( dmax ).replace( hour=0 )

    elif nearest == "day":
        dtmin = dtmin.replace( hour=0 )
        dmax += 86400  # jump forward one day
        dtmax = d.datetime.utcfromtimestamp( dmax ).replace( hour=0 )

    elif nearest in ["12hour", "6hour", "4hour", "3hour"]:
        nhr = int(nearest[:-4])
        newhr = (dtmin.hour / nhr) * nhr
        dtmin = dtmin.replace( hour=newhr )
        newhr = ((dtmax.hour / nhr)+1) * nhr
        day = dtmax.day
        if newhr >= 24: newhr = 0; day += 1
        dtmax = dtmax.replace( day=day, hour=newhr )

    elif nearest == "hour":
        dtmin = dtmin.replace( minute=0 )
        hr = dtmax.hour
        if hr == 23:      
            dmax += 3600  # jump forward one hour (there are 3600 sec per hour)
            dtmax = d.datetime.utcfromtimestamp( dmax )   # no replace necessary
        else: dtmax = dtmax.replace( hour=hr+1, minute=0 )

    elif nearest in [ "30minute", "10minute" ]:
        nmin = int(nearest[:-6])
        newmin = (dtmin.minute / nmin ) * nmin
        dtmin = dtmin.replace( minute=newmin )
        newmin = ((dtmax.minute / nmin)+1) * nmin
        hr = dtmax.hour
        if newmin >= 60: newmin = 0; hr += 1    # date rollover not imp.
        dtmax = dtmax.replace( hour=hr, minute=newmin )
     
    elif nearest == "minute":
        # dtmin is all set, just compute dtmax...
        newmin = dtmax.minute + 1
        hr = dtmax.hour
        if newmin >= 60: newmin = 0; hr += 1
        dtmax = dtmax.replace( hour=hr, minute=newmin )

    else: raise AppDt_Error( "findrange got unrecognized nearest= arg: " + str(nearest) )


    axmin = calendar.timegm( dtmin.timetuple() )
    axmax = calendar.timegm( dtmax.timetuple() )

    # at this point, dtmin and dtmax are the axis min and max as datetime type
    # and axmin and axmax are the axis min and max as int timestamps

    # now build a list of ready-to-render stubs with int positions...
    # will eventually add options for month rollover, year rollover, day rollover, etc.
    stublist = []

    iloop = 0
    dtcur = dtmin
    utime = axmin
    stub = dtcur.strftime( stubformat )  # do the first stub
    if inc2 != None and stub2first == True:
        stub2 = dtcur.strftime( stub2format )
        if stub2place == "prepend": stub = stub2 + stub 
        elif stub2place == "replace": stub = stub2 
        else: stub = stub + stub2
    stublist.append( [utime, stub] )

    while iloop < 500:   # sanity backstop
        yr = dtcur.year
        mon = dtcur.month
        day = dtcur.day
        if inc == "month":
            if mon == 12: dtcur = dtcur.replace( year=yr+1, month=1 )
            else: dtcur = dtcur.replace( month=mon+1 )
        elif inc == "3month":
            if mon >= 10: dtcur = dtcur.replace( year=yr+1, month=1 )
            else: dtcur = dtcur.replace( month=mon+3 )
        elif inc == "week" or inc[:8] == "week_day": utime += 604800       # number of seconds in a 7 day week
        elif inc == "day": utime += 86400
        elif inc == "12hour": utime += 43200
        elif inc == "6hour": utime += 21600
        elif inc == "4hour": utime += 14400
        elif inc == "3hour": utime += 10800
        elif inc == "hour": utime += 3600
        elif inc == "30minute": utime += 1800
        elif inc == "10minute": utime += 600
        elif inc == "minute": utime += 60
        else: raise AppDt_Error( "findrange() does not recognize inc=" + str(inc) )

        if inc not in ["month", "3month"]: dtcur = d.datetime.utcfromtimestamp( utime )

        if inc != "day": utime = calendar.timegm( dtcur.timetuple() ) 
        if utime > axmax: break

        # create the formatted stub
        stub = dtcur.strftime( stubformat )

        # stub2: check for rollover to new year (etc)
        if (inc2 == "year" and dtcur.year != yr) or  \
           (inc2 in ["month","3month"] and dtcur.month != mon) or  \
           (inc2 == "day" and dtcur.day != day):
            stub2 = dtcur.strftime( stub2format )
            if stub2place == "prepend": stub = stub2 + stub 
            elif stub2place == "replace": stub = stub2 
            else: stub = stub + stub2

        stublist.append( [ utime, stub ] )  
        iloop += 1

    Dtrange = collections.namedtuple( "Findrange", ["axmin", "axmax", "stublist"] )
    return Dtrange( axmin, axmax, stublist )

