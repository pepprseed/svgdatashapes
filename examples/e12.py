
import svgdatashapes as s
import svgdatashapes_dt as sdt       # for date/time support

def example12():    # Secchi depth readings plot with reversed Y axis

    depthdata = [ 
      ('09/21/2016', 6.60), ('09/19/2016', 6.20), ('09/08/2016', 4.85), ('09/01/2016', 6.00),
      ('08/18/2016', 7.00), ('08/09/2016', 7.60), ('08/03/2016', 7.10), ('07/28/2016', 7.25),
      ('07/22/2016', 8.10), ('07/14/2016', 8.65), ('07/08/2016', 9.95), ('06/29/2016', 9.60),
      ('06/22/2016', 9.40), ('06/16/2016', 8.60), ('06/9/2016', 8.40), ('06/02/2016', 8.30),
      ('05/26/2016', 8.40), ('05/19/2016', 7.85), ('05/11/2016', 7.95), ('05/05/2016', 7.70),
      ('04/28/2016', 7.85), ('04/19/2016', 7.15), ('03/30/2016', 7.20)   ]

    s.svgbegin( width=800, height=220 )
    sdt.dateformat( '%m/%d/%Y' )
    s.settext( color='#777', style='font-family: sans-serif; font-weight: bold;' )
    s.setline( color='#777' )

    # find our date range for X and build some stubs
    xrange = sdt.daterange( column=0, datarows=depthdata, nearest='month', inc='month', 
                stubformat='%b', inc2='year', stub2format=' %Y' )

    # set up X space...
    s.xspace( svgrange=(100,750), datarange=xrange )

    # find Y max and set up reversed Y space (0 at top)
    for dp in depthdata:  
        s.findrange( testval=dp[1] )  
    yrange = s.findrange( finish=True, addlpad=1 )
    s.yspace( svgrange=(60,180), datarange=(0,yrange.axmax), reverse=True )

    # render axes...
    s.xaxis( stublist=xrange.stublist, tics=8 )
    s.setline( color='#cfc' )
    s.yaxis( tics=8, grid=True )
    s.setline( color='#777' )
    s.plotdeco( title='Secchi depth readings indicating water clarity: Stormy Lake', ylabel='Depth (m)', outline=True )

    # render the blue depth lines... 
    s.setline( color='#99f', width=2 )
    for dp in depthdata:
         xloc = sdt.toint(dp[0])
         s.line( x1=xloc, y1=0.0, x2=xloc, y2=dp[1] )
         s.datapoint( x=xloc, y=dp[1], diameter=5, color='#99f' )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
