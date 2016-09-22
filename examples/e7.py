# beeswarm and boxplot display; tooltips on outlier data points
# option: ylog .... if True use a log Y axis; otherwise use linear

import minplot as p
import sampledata2 

def example7( ylog=False ):


    # get several 1-D example arrays of numbers sorted on magnitude, and put them into a dict
    plotdata = {}
    plotdata['1f'] = sampledata2.vectors( 'set1' )   # eg. [ 33, 36, 39, 41, 41, 49,.. ]
    plotdata['2f'] = sampledata2.vectors( 'set2' )
    plotdata['1m'] = sampledata2.vectors( 'set3' )
    plotdata['2m'] = sampledata2.vectors( 'set4' )

    p.svgbegin( width=550, height=350 )

    # find overall data range in Y (examine all 4 datasets)
    for key in plotdata:
        for val in plotdata[key]:
            p.findrange( testval=val )
    yrange = p.findrange( finish=True )

    # set up X space...
    p.catspace( axis='X', catlist=[ '1f', '2f', '1m', '2m' ], poslo=100, poshi=500 )

    if ylog == False: p.numspace( axis='Y', axmin=5, axmax=yrange.axmax, poslo=60, poshi=340 )  
    else: p.numspace( axis='Y', axmin=5, axmax=yrange.axmax, poslo=60, poshi=340, log=True )  

    # render axes and plotting area
    p.lineprops( color='#aaa' )
    p.textprops( color='#777', cssstyle='font-family: sans-serif; font-weight: bold;' )
    p.axisrender( axis='X', axisline=False, loc='min-8' )
    if ylog == False: p.axisrender( axis='y', tics=8, loc='min-8', grid=True )
    else: p.axisrender( axis='y', tics=8, loc='min-8', grid=True, inc=5, stubcull=20 )   
    p.plotdeco( ylabel='glucose [mg/dL]' )

    # compute percentiles and other summary info for each 1-D array
    info = {}
    for key in plotdata:
        info[key] = p.numinfo( datarows=p.vec2d( plotdata[key] ), numcol=0, percentiles=True )

    # render the beeswarms assisted by clustermode 
    p.clustermode( mode='left+right', tolerance=1.0 )
    diameter = 6; color = '#88c'; leftward = -8
    for key in plotdata:
        for val in plotdata[key]:
            if key in ['1f', '2f']: color = '#88c'
            else: color = '#db8'
            pctiles = info[key].percentiles
            if val < pctiles.p5 or val > pctiles.p95:   
                p.tooltip( 'Outlier: ' + str(val) + '    ID: nnnnnn' )    # tooltip for outliers 
            p.datapoint( x=key, y=val, diameter=diameter, color=color, xadjust=leftward )

    # render box plots and the 'N = nnn' annotation
    p.lineprops( color='#777' )
    p.textprops( ptsize=8, color='#777', anchor='middle' )
    rightward = 8
    for key in plotdata:
        if key in ['1f', '2f']: color = '#ddf'
        else: color = '#fed'
        pctiles = info[key].percentiles
        p.errorbar( x=key, ymin=pctiles.p5, ymax=pctiles.p95, adjust=rightward )
        p.bar( x=key, ybase=pctiles.p25, y=pctiles.p75, width=16, outline=True, adjust=rightward, color=color )
        p.datapoint( x=key, y=pctiles.median, diameter=6, color='#777', xadjust=rightward )
        p.label( text='N = '+str(info[key].nvals), x=key, y=None, yadjust=20, anchor='middle' )   # display N = nnn

    return  p.svgresult()
