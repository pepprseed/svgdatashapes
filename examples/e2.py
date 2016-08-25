import minplot as p

def example2():                                          # scatterplot example

    dataset1 = [ (-6.3, -5.2), (0.4, 1.8), (8.1, 8.7), (-3.7, -5.1), (8.6, 8.2), (-7.5, -8.3), (-8.0, -9.2),
       (-9.8, -9.1), (-6.7, -5.5), (7.6, 6.9), (-3.0, -2.3), (-4.8, -5.4), (-1.1, -0.8), (6.4, 5.7), (-5.2, -5.7),
       (9.7, 9.9), (5.9, 4.9), (-1.1, -2.5), (-8.3, -8.5), (5.8, 5.5), (9.1, 7.6), (-3.8, -3.8), (-7.0, -6.1),
       (-1.9, -2.7), (-5.9, -6.1), (0.3, -0.1), (-3.4, -4.7), (8.9, 8.9), (1.0, 2.1), (-3.5, -4.7), (4.0, 1.6),
       (2.9, 8.3), (-0.2, 5.6), (2.4, -4.1), (1.4, -7.0), (1.6, 7.6), (-1.0, -9.0), (8.8, 0.7), (-5.1, 5.4), (5.7, -4.5) ]

    dataset2 = [ (4.9, 4.2), (-4.9, -3.8), (8.6, 8.7), (0.9, 1.1), (-7.8, -7.9), (-0.1, 0.0), (8.6, 8.0), (-3.4, -3.1),
       (-3.8, -4.5), (6.7, 8.1), (-3.4, -3.0), (8.4, 8.4), (-4.3, -5.1), (2.8, 3.4), (5.4, 5.3), (4.0, 4.9), (8.3, 9.6),
       (7.7, 6.9), (1.7, 2.2), (-6.8, -6.0), (6.4, 5.8), (4.4, 3.8), (2.8, 4.3), (-2.0, -0.8), (-5.4, -5.7), (-0.2, 1.2),
       (-3.3, -2.2), (5.7, 5.5), (2.2, 1.9), (-0.2, 0.9), (7.7, -8.1), (-7.6, -8.0), (8.3, 3.7), (-9.9, -0.3), (7.2, 6.0),
       (-8.6, -3.6), (1.4, 1.8), (-5.5, 8.6), (1.1, -2.0), (7.8, -2.3) ]


    p.svgbegin( width=400, height=400 )

    p.textprops( color='#777', cssstyle="font-family: sans-serif; font-weight: bold;" )
    p.lineprops( color='#777' )

    # pretend we're getting data dynamically and find the data range in X and Y
    for dp in dataset1 + dataset2:       # find range in X
        p.findrange( testval=dp[0] )    
    xrange = p.findrange( finish=True )
    for dp in dataset1 + dataset2:       # find range in Y
        p.findrange( testval=dp[1] )    
    yrange = p.findrange( finish=True )

    # set up X and Y space...
    p.numspace( axis='X', axmin=xrange.axmin, axmax=xrange.axmax, poslo=100, poshi=350 )
    p.numspace( axis='Y', axmin=yrange.axmin, axmax=yrange.axmax, poslo=100, poshi=350 )

    # render axes and plotting area
    p.axisrender( axis='X', tics=8, loc="min-8" )
    p.axisrender( axis='y', tics=8, loc="min-8" )
    p.plotdeco( shade='#eee', outline=True, rectadj=8 )
    p.plotdeco( ylabel='&Delta; density [g/cm<sup>2</sup>]', xlabel='&Delta; density [g/cm<sup>2</sup>]', 
          ylabeladj=(-15,0), xlabeladj=(0,-10) )

    # do crosshairs at 0, 0
    p.lineprops( color='#888', dash="3,3" )
    p.line( x1='min', y1=0.0, x2='max', y2=0.0 )
    p.line( x1=0.0, y1='min', x2=0.0, y2='max' )

    # render dataset1 in red data points
    p.legenditem( label="Group A", sample='circle', color='#a00', width=80 )
    for dp in dataset1:
        p.tooltip( "("+str(dp[0])+","+str(dp[1])+")" )
        p.datapoint( x=dp[0], y=dp[1], fill='#a00', diameter=8, opacity=0.6 )

    # render dataset2 in blue data points
    p.legenditem( label="Group B", sample='circle', color='#00a', width=80 )
    for dp in dataset2:
        p.tooltip( "("+str(dp[0])+","+str(dp[1])+")" )
        p.datapoint( x=dp[0], y=dp[1], fill='#00a', diameter=8, opacity=0.6 )

    p.legendrender( location='topleft', locadj=(0,30), format='across' )

    # return the svg 
    return p.svgresult()
