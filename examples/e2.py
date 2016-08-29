# scatterplot of mixed sign data; crosshairs at (0,0); superscripts in labels; data points have tooltips

import minplot as p
import sampledata1 

def example2():                                          # scatterplot example

    # get some sample plot data...  eg.   [ (-6.3, -5.2), (0.4, 1.8),  .... ]
    dataset1 = sampledata1.datapoints( 'set1' )
    dataset2 = sampledata1.datapoints( 'set2' )

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
    p.plotdeco( ylabel='&Delta; density [g/cm<sup>2</sup>]', xlabel='&Delta; weight [g]')

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

    p.legendrender( location='top', yadjust=30, format='across' )

    # return the svg 
    return p.svgresult()
