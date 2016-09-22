
import minplot as p
import minplot_dt as pdt

def example12():    # Secchi depth readings plot with reversed Y axis

    depthdata = [ 
      ('09/21/2016', 6.60), ('09/19/2016', 6.20), ('09/08/2016', 4.85), ('09/01/2016', 6.00),
      ('08/18/2016', 7.00), ('08/09/2016', 7.60), ('08/03/2016', 7.10), ('07/28/2016', 7.25),
      ('07/22/2016', 8.10), ('07/14/2016', 8.65), ('07/08/2016', 9.95), ('06/29/2016', 9.60),
      ('06/22/2016', 9.40), ('06/16/2016', 8.60), ('06/9/2016', 8.40), ('06/02/2016', 8.30),
      ('05/26/2016', 8.40), ('05/19/2016', 7.85), ('05/11/2016', 7.95), ('05/05/2016', 7.70),
      ('04/28/2016', 7.85), ('04/19/2016', 7.15), ('03/30/2016', 7.20)   ]

    p.svgbegin( width=800, height=200 )
    pdt.dateformat( '%m/%d/%Y' )

    # find our date range for X and build some stubs...
    xrange = pdt.daterange( dtcol='0', datarows=depthdata, nearest='month', inc='month', 
                stubformat='%b', inc2='year', stub2format=' %Y' )

    # set up X space...
    p.numspace( axis='X', axmin=xrange.axmin, axmax=xrange.axmax, poslo=60, poshi=750 )

    # find Y max and set up reversed Y space (0 at top)
    for dp in depthdata:  
        p.findrange( testval=dp[1] )  
    yrange = p.findrange( finish=True, addlpad=1 )
    p.numspace( axis='Y', reverse=True, axmin=0, axmax=yrange.axmax, poslo=60, poshi=180 )

    p.lineprops( color='#777' )
    p.textprops( color='#777', cssstyle='font-family: sans-serif; font-weight: bold;' )

    # render axes...
    p.axisrender( axis='X', stublist=xrange.stublist, tics=8 )
    p.lineprops( color='#cfc' )
    p.axisrender( axis='y', tics=8, grid=True )
    p.lineprops( color='#777' )
    p.plotdeco( title='Secchi depth readings', ylabel='Depth (m)',  outline=True )

    # render the blue depth lines... 
    p.lineprops( color='#99f' )
    for dp in depthdata:
         xloc = pdt.toint(dp[0])
         p.line( x1=xloc, y1=0.0, x2=xloc, y2=dp[1] )
         p.datapoint( x=xloc, y=dp[1], diameter=5, color='#99f' )

    return p.svgresult()
