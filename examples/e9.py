# producce a histogram by computing a frequency distribution then plotting the bins

import svgdatashapes as s
import sampledata2

def example9():

    # get a 1-D example array of numbers 
    plotdata = sampledata2.vectors( 'set1' )   # eg. [ 33, 36, 39, 41, 41, 49,.. ]

    s.svgbegin( width=500, height=350 )

    s.settext( style='font-family: sans-serif; font-weight: bold;' )
    s.setline( color='#aaa' )

    # compute a frequency distribution....
    info = s.columninfo( datarows=s.vec2d( plotdata ), column=0, distrib=True, distbinsize='inc/4' )
    freqdata = info.distribution

    # find the data min and max for X axis....
    for val in plotdata:
        s.findrange( testval=val )
    xrange = s.findrange( finish=True )
    s.xspace( svgrange=(80,450), datarange=xrange )
    
    # find the histogram min and max for Y axis...
    for row in freqdata:
        s.findrange( testval=row.accum )
    yrange = s.findrange( finish=True )
    s.yspace( svgrange=(80,320), datarange=yrange )

    # render X and Y axes
    s.xaxis()
    s.yaxis( loc='left-20', grid=True )
    s.plotdeco( xlabel='glucose  [mg/dL]', ylabel='Number of instances' )

    # render histogram
    for row in freqdata:
        s.bar( x=row.binmid, y=row.accum, width=5, color='pink' )

    # add a label mentioning the bin size...
    s.label( text='bin size = '+str( info.distbinsize ), xadjust=320, yadjust=300 )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()

