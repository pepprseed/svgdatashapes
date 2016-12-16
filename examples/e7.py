# beeswarm and boxplot display; tooltips on outlier data points
# option: ylog .... if True use a log Y axis; otherwise use linear

import svgdatashapes as s
import sampledata2 

def example7( ylog=False ):


    # get several 1-D example arrays of numbers sorted on magnitude, and put them into a dict
    plotdata = {}
    plotdata['1f'] = sampledata2.vectors( 'set1' )   # eg. [ 33, 36, 39, 41, 41, 49,.. ]
    plotdata['2f'] = sampledata2.vectors( 'set2' )
    plotdata['1m'] = sampledata2.vectors( 'set3' )
    plotdata['2m'] = sampledata2.vectors( 'set4' )

    # set our text and line properties...
    textstyle = 'font-family: sans-serif; font-weight: bold;'
    s.settext( color='#777', style=textstyle )
    s.setline( color='#aaa' )

    # begin building our svg...
    s.svgbegin( width=550, height=350 )

    # set up X space (categorical)...
    s.xspace( svgrange=(100,500), catlist=[ '1f', '2f', '1m', '2m' ] )

    # find overall data range in Y (examine all 4 datasets) and set Y space
    for key in plotdata:
        for val in plotdata[key]:
            s.findrange( testval=val )
    yrange = s.findrange( finish=True )
    
    s.yspace( svgrange=(60,340), datarange=yrange, log=ylog )

    # render axes and plotting area
    s.xaxis( axisline=False, loc='min-8' )
    if ylog == False: s.yaxis( tics=8, loc='min-8', grid=True )
    else: s.yaxis( tics=8, loc='min-8', grid=True, inc=5, stubcull=20 )   
    s.plotdeco( ylabel='glucose [mg/dL]' )

    # compute percentiles and other summary info for each 1-D array
    info = {}
    for key in plotdata:
        info[key] = s.columninfo( datarows=s.vec2d( plotdata[key] ), column=0, percentiles=True )

    # render the beeswarms assisted by datapoints clustering
    s.setclustering( mode='left+right', tolerance=1.0 )
    diameter = 6; color = '#88c'; leftward = -8
    for key in plotdata:
        for val in plotdata[key]:
            if key in ['1f', '2f']: color = '#88c'
            else: color = '#db8'
            pctiles = info[key].percentiles
            if val < pctiles.p5 or val > pctiles.p95:   
                s.tooltip( 'Outlier: ' + str(val) + '    ID: nnnnnn' )    # tooltip for outliers 
            s.datapoint( x=key, y=val, diameter=diameter, color=color, xadjust=leftward )

    # render box plots and the 'N = nnn' annotation
    s.setline( color='#777' )
    s.settext( ptsize=8, color='#777', anchor='middle' )
    rightward = 8
    for key in plotdata:
        if key in ['1f', '2f']: color = '#ddf'
        else: color = '#fed'
        pctiles = info[key].percentiles
        s.errorbar( x=key, ymin=pctiles.p5, ymax=pctiles.p95, adjust=rightward )
        s.bar( x=key, ybase=pctiles.p25, y=pctiles.p75, width=16, outline=True, adjust=rightward, color=color )
        s.datapoint( x=key, y=pctiles.median, diameter=6, color='#777', xadjust=rightward )
        s.label( text='N = '+str(info[key].nvals), x=key, y=None, yadjust=20, anchor='middle' )   # display N = nnn

    # return the svg.  The caller could then add it in to the rendered HTML.
    return  s.svgresult()
