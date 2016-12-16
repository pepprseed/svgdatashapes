# multipanel display of curves or bars; plot data are dict rows.
# option: dispmode .... either 'curves',  'bars', or 'updown'

import svgdatashapes as s
import sampledata3 

def example8( dispmode='curves' ):

    # get some plotdata.  One data row per plotted panel (with some missing data as None)
    if dispmode in ['curves', 'bars' ]: plotdata = sampledata3.dictrows( 'set1' )
    elif dispmode == 'updown': plotdata = sampledata3.dictrows( 'mixedsign' )

    # begin building our svg...
    s.svgbegin( width=600, height=200 )

    # set our text and line properties...
    textstyle = 'font-family: sans-serif; font-weight: bold;'
    s.settext( ptsize=12, color='#444', style=textstyle )
    s.setline( color='#ada' )

    # get an list of unique state names from the data...
    cats = s.uniqcats( datarows=plotdata, column='group' )

    # set up the X categorical space and capture panel boundary coordinates...
    panels = s.xspace( svgrange=(80,580), catlist=cats )

    # find Y scale max and min
    for row in plotdata:
        s.findrange( testval=row['t1'], erramt=row['t1sem'] );
        s.findrange( testval=row['t2'], erramt=row['t2sem'] );
        s.findrange( testval=row['t3'], erramt=row['t3sem'] );
        s.findrange( testval=row['t4'], erramt=row['t4sem'] );
    yrange = s.findrange( finish=True )

    # make a couple of settings that depend on dispmode....
    if dispmode in ['curves', 'bars']: ymin = 0.0; ybase = None; ylabel = 'weight [g]'
    elif dispmode == 'updown': ymin = yrange.axmin; ybase = 0.0; ylabel = 'Change'

    # set up the Y numerically scaled space... 
    s.yspace( svgrange=(80,180), datarange=(ymin,yrange.axmax) )

    # highlight one of the panels...
    s.rectangle( x='D', height='all', color='#ffc', adjust=(0,-35,0,0) )

    # render the whole-plot X and Y axes...  
    s.xaxis( tics=8, axisline=False, grid=True )
    s.yaxis( axisline=False, inc=10, loc='left-10' )
    s.plotdeco( xlabel='Group', ylabel=ylabel )

    # iterate across data rows / panels...
    iloop = 0
    for row in plotdata:
        panel = panels[iloop]   # get panel boundary coords info...
        iloop += 1

        # set up panel's interior X categorical space; blank entries help w/ spacing.  
        # The previously set Y numeric space is still in effect.
        s.xspace( svgrange=(panel), catlist=['', 't1', 't2', 't3', 't4', ''] )

        # render error bars for one panel
        s.setline( color='#bbb', width=1 )
        for key in [ 't1', 't2', 't3', 't4' ]:
            s.errorbar( x=key, y=row[key], erramt=row[key+'sem'] )

        # render curve (or bar set) for the current panel...
        if dispmode == 'curves':
            s.setline( color='#b44', width=2 )
            s.curvebegin()
            for key in [ 't1', 't2', 't3', 't4' ]:
                s.curvenext( x=key, y=row[key] )
                s.datapoint( x=key, y=row[key], diameter=5, color='#b44' )

        elif dispmode in ['bars', 'updown']:
            barcolor = [ 'orange', 'blue', 'green', 'red' ]
            icolor = 0
            for key in [ 't1', 't2', 't3', 't4' ]:
                s.bar( x=key, y=row[key], width=5, color=barcolor[icolor], ybase=ybase )
                icolor += 1

    if dispmode in ['bars', 'updown']:   # add a legend for the colors
        s.settext( style=None, ptsize=9 )
        s.legenditem( label='t1', color='orange', width=40 )
        s.legenditem( label='t2', color='blue', width=40 )
        s.legenditem( label='t3', color='green', width=40 )
        s.legenditem( label='t4', color='red', width=40 )
        s.legendrender( xadjust=50, yadjust=28, format='across' )   # position the left side of legend at (50, 28)

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
