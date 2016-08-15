import minplot as p
import minplot_dt as pdt

def example5():                                          # plot some dates with times
    pdt.setformat( "%Y-%m-%dT%H:%M:%S" )

    dataset1 = [ ("2016-02-29T23:59:20", 45), ("2016-03-1T00:01:17", 33), ("2016-03-1T16:25:33", 22), 
                 ("2016-03-01T14:55:22", 30), ("2016-03-02T00:12:57", 38), ("2016-03-2T11:48:00", 32) ]
    
    p.svgbegin( width=800, height=300 )

    xrange = pdt.dtrange( dtfield="0", datarows=dataset1, nearest="day", inc="6hour", stubformat="%l%P", 
                          inc2="day", stub2format="%b %d", stub2place="replace" )

    # set up X space...
    p.numspace( axis='X', axmin=xrange.axmin, axmax=xrange.axmax, poslo=60, poshi=750 )

    # find Y range and set up Y space...
    for dp in dataset1:  
        p.findrange( testval=dp[1] )  
    yrange = p.findrange( finish=True )
    p.numspace( axis='Y', axmin=yrange.axmin, axmax=yrange.axmax, poslo=60, poshi=280 )

    p.lineprops( color='#777' )
    p.textprops( color='#555' )
    p.plotdeco( title='Date time data', outline=True )

    # render axes...
    p.lineprops( color='#777' ); p.textprops( color='#555', ptsize=11 )
    p.axisrender( axis='X', stublist=xrange.stublist, tics=8, grid=True )
    p.textprops( color='#555' )
    p.axisrender( axis='y', tics=8 )

    # render red data points
    for dp in dataset1:
        p.bar( x=pdt.num(dp[0]), y=dp[1], fill='#4f4', width=5, opacity=0.6 )

    svg = p.svgresult()
    return svg
