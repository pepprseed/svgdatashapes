# scatterplot of mixed sign data; crosshairs at (0,0); superscripts in labels; data points have tooltips

import svgdatashapes as s
import sampledata1 

def example2():                                          # scatterplot example

    # get some sample plot data...  eg.   [ (-6.3, -5.2), (0.4, 1.8),  .... ]
    dataset1 = sampledata1.datapoints( 'set1' )
    dataset2 = sampledata1.datapoints( 'set2' )

    s.svgbegin( width=400, height=400 )

    textstyle = 'font-family: sans-serif; font-weight: bold;'
    s.settext( color='#777', style=textstyle )
    s.setline( color='#777' )

    # find the data min and max in X
    for dp in dataset1 + dataset2:
        s.findrange( testval=dp[0] )    
    xrange = s.findrange( finish=True )

    # find the data min and max in Y
    for dp in dataset1 + dataset2:
        s.findrange( testval=dp[1] )    
    yrange = s.findrange( finish=True )

    # set up X and Y space...
    s.xspace( svgrange=(100,350), datarange=xrange )
    s.yspace( svgrange=(100,350), datarange=yrange )

    # render axes and a shaded plotting area
    s.xaxis( tics=8, loc='min-8' )
    s.yaxis( tics=8, loc='min-8' )
    s.plotdeco( shade='#eee', outline=True, rectadj=8 )

    # render axis labels with superscript, greek char...
    s.plotdeco( ylabel='&Delta; density [g/cm<sup>2</sup>]', xlabel='&Delta; weight [g]')

    # do crosshairs at 0, 0
    s.setline( color='#888', dash='3,3' )
    s.line( x1='min', y1=0.0, x2='max', y2=0.0 )
    s.line( x1=0.0, y1='min', x2=0.0, y2='max' )

    # render dataset1 in red data points
    for dp in dataset1:
        s.tooltip( '('+str(dp[0])+','+str(dp[1])+')' )
        s.datapoint( x=dp[0], y=dp[1], color='#a00', diameter=8, opacity=0.6 )

    # render dataset2 in blue data points
    for dp in dataset2:
        s.tooltip( '('+str(dp[0])+','+str(dp[1])+')' )
        s.datapoint( x=dp[0], y=dp[1], color='#00a', diameter=8, opacity=0.6 )

    # create a legend...
    s.legenditem( label='Group A', sample='circle', color='#a00', width=80 )
    s.legenditem( label='Group B', sample='circle', color='#00a', width=80 )
    s.legendrender( location='top', yadjust=30, format='across' )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
