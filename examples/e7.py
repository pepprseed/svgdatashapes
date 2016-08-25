
import minplot as p
import sampledata as sd

def example7( ylog=False ):
    # produce beeswarm and boxplot display
    # ylog .... if True use a log Y axis; otherwise use linear

    plotdata = {}

    # sampledata() provides several 1-D example arrays of numbers sorted on magnitude
    plotdata['1f'] = sd.sampledata( '1f' )   # eg. [ 33, 36, 39, 41, 41, 49,.. ]
    plotdata['2f'] = sd.sampledata( '2f' )
    plotdata['1m'] = sd.sampledata( '1m' )
    plotdata['2m'] = sd.sampledata( '2m' )

    p.svgbegin( width=550, height=350 )

    textstyle = "font-family: sans-serif; font-weight: bold;"

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
    p.textprops( color='#777', cssstyle=textstyle )
    p.axisrender( axis='X', axisline=False, loc='min-8' )
    if ylog == False: p.axisrender( axis='y', tics=8, loc='min-8', grid=True )
    else: p.axisrender( axis='y', tics=8, loc='min-8', grid=True, inc=5, stubcull=20 )   
    p.plotdeco( ylabel='glucose [mg/dL]', ylabeladj=(-20,0) )

    # compute percentiles and other summary info for each 1-D array
    info = {}
    for key in plotdata:
        info[key] = p.numinfo( datarows=p.vec2d( plotdata[key] ), numcol=0, percentiles=True )

    # render the beeswarms assisted by clustermode 
    p.clustermode( mode='left+right', tolerance=1.0 )
    diameter = 6; color = '#88c'; xofs = -8;
    for key in plotdata:
        for val in plotdata[key]:
            if key in ['1f', '2f']: color = '#88c'
            else: color = '#db8'
            pctiles = info[key].percentiles
            if val < pctiles["5th"] or val > pctiles["95th"]:   
                p.tooltip( "Outlier: " + str(val) + "    ID: nnnnnn" )    # tooltip for outliers 
            p.datapoint( x=key, y=val, diameter=diameter, fill=color, xofs=xofs )

    # render box plots and the "N = nnn" annotation
    p.lineprops( color='#777' )
    p.textprops( ptsize=8, color='#777', anchor='middle' )
    for key in plotdata:
        if key in ['1f', '2f']: color = '#ddf'
        else: color = '#fed'
        pctiles = info[key].percentiles
        p.errorbar( x=key, ymin=pctiles['5th'], ymax=pctiles['95th'], xofs=8 )
        p.bar( x=key, ybase=pctiles['25th'], y=pctiles['75th'], width=16, outline=True, xofs=8, fill=color )
        p.datapoint( x=key, y=pctiles['median'], diameter=6, fill='#777', xofs=8 )
        p.txt( p.nx(key), p.nmin('Y')-40, 'N = ' + str(info[key].nvals) )   # display N = nnn

    return  p.svgresult()
