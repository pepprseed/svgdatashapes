# producce a histogram by computing a frequency distribution then plotting the bins

import minplot as p
import sampledata2

def example9():
    # produce a histogram

    # get a 1-D example array of numbers 
    plotdata = sampledata2.vectors( 'set1' )   # eg. [ 33, 36, 39, 41, 41, 49,.. ]

    p.svgbegin( width=500, height=350 )

    textstyle = "font-family: sans-serif; font-weight: bold;"
    p.textprops( cssstyle=textstyle )

    # compute a frequency distribution....
    info = p.numinfo( datarows=p.vec2d( plotdata ), numcol=0, distrib=True, distbinsize='inc/4' )
    freqdata = info.distribution

    # find the data min and max for X axis....
    for val in plotdata:
        p.findrange( testval=val )
    range = p.findrange( finish=True )
    p.numspace( axis='X', axmin=range.axmin, axmax=range.axmax, poslo=80, poshi=450 )
    
    # find the histogram min and max for Y axis...
    for row in freqdata:
        p.findrange( testval=row.accum )
    range = p.findrange( finish=True )
    p.numspace( axis='Y', axmin=range.axmin, axmax=range.axmax, poslo=80, poshi=320 )

    # render X and Y axes
    p.lineprops( color='#aaa' )
    p.axisrender( axis='X' )
    p.axisrender( axis='Y', loc='left-20', grid=True )
    p.plotdeco( xlabel='glucose  [mg/dL]', ylabel='Number of instances' )

    # render histogram
    for row in freqdata:
        p.bar( x=row.binmid, y=row.accum, width=5, fill='pink' )

    p.label( text='bin size = '+str( info.distbinsize ), xadjust=320, yadjust=300 )

    return p.svgresult()

