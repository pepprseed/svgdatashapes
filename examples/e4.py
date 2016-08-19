import minplot as p
import minplot_dt as pdt

def example4():                                        # plot some date-based data
    pdt.setformat( "%Y/%m/%d" )

    dataset1 = [ ("2015/04/10", 45), ("2015/12/2", 33),  ("2015/12/7", 22), 
                 ("2015/12/28", 30), ("2016/01/14", 38), ("2016/02/8", 32) ]

    p.svgbegin( width=500, height=300 )

    xrange = pdt.dtrange( dtcol="0", datarows=dataset1, nearest="3month", inc="3month", 
                stubformat="%b", inc2="year", stub2format=" %Y" )
    # alt1:  xrange = pdt.dtrange( dtcol="0", datarows=dataset1, 
    #          nearest="year", inc="month", stubformat="1 %b '%y" )  
    # alt2:  xrange = pdt.dtrange( dtcol="0", datarows=dataset1, 
    #          nearest="week_day2", stubformat="%b %d" )             

    # set up X space...
    p.numspace( axis='X', axmin=xrange.axmin, axmax=xrange.axmax, poslo=60, poshi=400 )

    # find Y range and set up Y space...
    for dp in dataset1:  
        p.findrange( testval=dp[1] )  
    yrange = p.findrange( finish=True )
    p.numspace( axis='Y', axmin=yrange.axmin, axmax=yrange.axmax, poslo=60, poshi=280 )

    p.lineprops( color='#777' )
    p.textprops( color='#777' )
    p.plotdeco( title='Date time data', outline=True )

    # render axes...
    p.lineprops( color='#777' ); p.textprops( color='#777' )
    p.axisrender( axis='X', stublist=xrange.stublist, tics=8, grid=True )
    p.textprops( color='#777' )
    p.axisrender( axis='y', tics=8 )

    # render red data points
    for dp in dataset1:
        p.bar( x=pdt.num(dp[0]), y=dp[1], fill='#d44', width=5, opacity=0.6 )

    svg = p.svgresult()
    return svg
