# multipanel display of curves or bars; plot data are dict rows.
# option: dispmode .... either 'curves',  'bars', or 'updown'

import minplot as p
import sampledata3 

def example8( dispmode='curves' ):

    # get some plotdata.  One data row per plotted panel (with some missing data as None)
    if dispmode in ['curves', 'bars' ]: plotdata = sampledata3.dictrows( 'set1' )
    elif dispmode == 'updown': plotdata = sampledata3.dictrows( 'mixedsign' )

    textstyle = 'font-family: sans-serif; font-weight: bold;'    

    # initialize minplot and begin building our svg...
    p.svgbegin( width=600, height=200 )

    # get an list of unique state names from the data...
    catinfo = p.catinfo( catcol='group', datarows=plotdata )

    # set up the X categorical space and capture panel boundary coordinates...
    panels = p.catspace( axis='X', catlist=catinfo.catlist, poslo=80, poshi=580 )

    # dynamically find Y scale max and min
    for row in plotdata:
        p.findrange( testval=row['t1'], erramt=row['t1sem'] );
        p.findrange( testval=row['t2'], erramt=row['t2sem'] );
        p.findrange( testval=row['t3'], erramt=row['t3sem'] );
        p.findrange( testval=row['t4'], erramt=row['t4sem'] );
    yrange = p.findrange( finish=True )

    # make a couple of settings that depend on dispmode....
    if dispmode in ['curves', 'bars']: ymin = 0.0; ybase = None; ylabel = 'weight [g]'
    elif dispmode == 'updown': ymin = yrange.axmin; ybase = 0.0; ylabel = 'Change'

    # set up the Y numerically scaled space... 
    p.numspace( axis='Y', axmin=ymin, axmax=yrange.axmax, poslo=80, poshi=180 )

    # highlight one of the panels...
    p.rectangle( x='D', height='all', fill='#ffc', adjust=(0,-35,0,0) )

    # render the whole-plot X and Y axes...  
    p.lineprops( color='#ada' )
    p.textprops( ptsize=12, color='#444', cssstyle=textstyle )  
    p.axisrender( axis='X', tics=8, axisline=False, grid=True )
    p.axisrender( axis='Y', axisline=False, inc=10, loc='left-10' )
    p.plotdeco( xlabel='Group', ylabel=ylabel )


    # iterate across data rows / panels...
    iloop = 0
    for row in plotdata:
        pan = panels[iloop]   # get panel boundary coords info...
        iloop += 1

        # set up panel's interior X categorical space; blank entries help w/ spacing.  
        # The previously set Y numeric space is still in effect.
        p.catspace( axis='x', catlist=['', 't1', 't2', 't3', 't4', ''], poslo=pan.poslo, poshi=pan.poshi )

        # render error bars for one panel
        p.lineprops( color='#bbb', width=1 )
        for key in [ 't1', 't2', 't3', 't4' ]:
            p.errorbar( x=key, y=row[key], erramt=row[key+'sem'] )

        # render curve (or bar set) for the current panel...

        if dispmode == 'curves':
            p.lineprops( color='#b44', width=2 )
            p.curvebegin()
            for key in [ 't1', 't2', 't3', 't4' ]:
                p.curvenext( x=key, y=row[key] )
                p.datapoint( x=key, y=row[key], diameter=5, fill='#b44' )

        elif dispmode in ['bars', 'updown']:
            barcolor = [ 'orange', 'blue', 'green', 'red' ]
            icolor = 0
            for key in [ 't1', 't2', 't3', 't4' ]:
                p.bar( x=key, y=row[key], width=5, fill=barcolor[icolor], ybase=ybase )
                icolor += 1

    if dispmode in ['bars', 'updown']:   # add a legend for the colors
        p.textprops( cssstyle=None, ptsize=9 )
        p.legenditem( label='t1', color='orange', width=40 )
        p.legenditem( label='t2', color='blue', width=40 )
        p.legenditem( label='t3', color='green', width=40 )
        p.legenditem( label='t4', color='red', width=40 )
        p.legendrender( xadjust=50, yadjust=28, format='across' )   # position the left side of legend at (50, 28)


    # return the SVG...
    return p.svgresult()
