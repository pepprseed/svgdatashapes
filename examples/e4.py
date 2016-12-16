# basic example of plotting date data

import svgdatashapes as s
import svgdatashapes_dt as sdt     # for date/time support

def example4():                                        # plot some date-based data

    dataset1 = [ ('2015/04/10', 45), ('2015/12/2', 33),  ('2015/12/7', 22), 
                 ('2015/12/28', 30), ('2016/01/14', 38), ('2016/02/8', 32) ]

    s.setline( color='#777' )   # set gray line color
    s.settext( color='#777' )   # set gray text color

    s.svgbegin( width=500, height=300 )

    # indicate our date notation..
    sdt.dateformat( '%Y/%m/%d' )

    # find min max date range and set up x space...
    xrange = sdt.daterange( column=0, datarows=dataset1, nearest='3month', inc='3month', 
                stubformat='%b', inc2='year', stub2format=' %Y' )
    s.xspace( svgrange=(60,400), datarange=xrange )


    # find min max Y numeric range and set up Y space...
    for dp in dataset1:  
        s.findrange( testval=dp[1] )  
    yrange = s.findrange( finish=True )
    s.yspace( svgrange=(60,280), datarange=yrange )

    # render axes...
    s.xaxis( stublist=xrange.stublist, tics=8, grid=True )
    s.yaxis( tics=8 )
    s.plotdeco( title='Date time data', outline=True )

    # render red bars 
    for dp in dataset1:
        s.bar( x=sdt.toint(dp[0]), y=dp[1], color='#d44', width=5, opacity=0.6 )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()


# Note, here are some alternatives to try, for the daterange call above:
# sdt.daterange( column=0, datarows=dataset1, nearest='year', inc='month', stubformat='1 %b '%y' )  
# sdt.daterange( column=0, datarows=dataset1, nearest='week_day2', stubformat='%b %d' )             
