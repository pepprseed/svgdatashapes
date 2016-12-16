# basic example of plotting data + time data

import svgdatashapes as s
import svgdatashapes_dt as sdt   # for date/time support

def example5():                                          # plot some dates with times

    dataset1 = [ ('2016-02-29T23:59:20', 45), ('2016-03-1T00:01:17', 33), ('2016-03-1T16:25:33', 22), 
                 ('2016-03-01T14:55:22', 30), ('2016-03-02T00:12:57', 38), ('2016-03-2T11:48:00', 32) ]

    s.svgbegin( width=800, height=300 )

    s.setline( color='#777' )   # set gray line color
    s.settext( color='#555' )   # set gray text color

    # indicate our datetime notation...
    sdt.dateformat( '%Y-%m-%dT%H:%M:%S' )

    # find min max range of the datetimes and set up X space
    xrange = sdt.daterange( column=0, datarows=dataset1, nearest='day', inc='6hour', stubformat='%l%P', 
                          inc2='day', stub2format='%b %d', stub2place='replace' )
    s.xspace( svgrange=(50,750), datarange=xrange )

    # find Y min max numeric range and set up Y space...
    for dp in dataset1:  
        s.findrange( testval=dp[1] )  
    yrange = s.findrange( finish=True )
    s.yspace( svgrange=(60,280), datarange=yrange )

    # render axes...
    s.settext( color='#555', ptsize=11 )
    s.xaxis( stublist=xrange.stublist, tics=8, grid=True )
    s.yaxis( tics=8 )
    s.plotdeco( title='Date time data', outline=True )

    # render red bars
    for dp in dataset1:
        s.bar( x=sdt.toint(dp[0]), y=dp[1], color='#4f4', width=5, opacity=0.6 )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
