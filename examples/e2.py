import minplot as p

def example2():                                          # scatterplot example

    dataset1 = [ ( 2, -8), (-3,  5), (-8, -4), ( 4,  7), (0, -3) ]

    p.svgbegin( width=300, height=300 )

    # find X range and set up X space...
    for dp in dataset1:  
        p.findrange( testval=dp[0] )  
    xrange = p.findrange( finish=True )
    p.numspace( axis='X', axmin=xrange.axmin, axmax=xrange.axmax, poslo=60, poshi=280 )

    # find Y range and set up Y space...
    for dp in dataset1:  
        p.findrange( testval=dp[1] )  
    yrange = p.findrange( finish=True )
    p.numspace( axis='Y', axmin=yrange.axmin, axmax=yrange.axmax, poslo=60, poshi=280 )

    p.lineprops( color='#777' )
    p.textprops( color='#777' )
    p.plotdeco( title='Some mixed-sign data', ylabel='var 1', xlabel='var 2', 
                     shade='#eee', outline=True )

    # do crosshairs at 0, 0
    p.lineprops( color='#ccc' )
    p.line( x1='min', y1=0.0, x2='max', y2=0.0 )
    p.line( x1=0.0, y1='min', x2=0.0, y2='max' )
    
    # render axes...
    p.lineprops( color='#777' ); p.textprops( color='#777' )
    p.axisrender( axis='X', tics=8 )
    p.axisrender( axis='y', tics=8 )

    # render red data points
    for dp in dataset1:
        p.datapoint( x=dp[0], y=dp[1], fill='#b07070', diameter=10 )

    # render an arrow...
    p.arrow( x1=-5, y1=-10, x2=1.5, y2=-8.3 )

    svg = p.svgresult()
    return svg
