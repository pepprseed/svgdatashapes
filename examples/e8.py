
import minplot as p

def example8( dispmode='curves' ):

    # Define some plotdata.  One data row per plotted panel.  Note the missing cells in groups D and G
    plotdata = []
    plotdata.append( {'group':'A', 't1':14.4, 't1sem':2.3, 't2':17.3, 't2sem':4.3, 't3':23.5, 't3sem':6.4, 't4':20.7, 't4sem':5.8 } )
    plotdata.append( {'group':'B', 't1':16.2, 't1sem':3.8, 't2':18.9, 't2sem':3.3, 't3':25.2, 't3sem':11.2,'t4':25.7, 't4sem':6.1 } )
    plotdata.append( {'group':'C', 't1':11.3, 't1sem':3.0, 't2':13.6, 't2sem':5.8, 't3':17.3, 't3sem':3.9, 't4':22.3, 't4sem':6.8 } )
    plotdata.append( {'group':'D', 't1':18.8, 't1sem':5.2,                         't3':27.8, 't3sem':7.3, 't4':29.7, 't4sem':8.1 } )
    plotdata.append( {'group':'E', 't1':17.6, 't1sem':6.8, 't2':19.2, 't2sem':4.5, 't3':22.7, 't3sem':7.8, 't4':23.8, 't4sem':5.3 } )
    plotdata.append( {'group':'F', 't1':13.9, 't1sem':2.2, 't2':17.6, 't2sem':2.4, 't3':20.1, 't3sem':4.2, 't4':24.8, 't4sem':7.2 } )
    plotdata.append( {'group':'G', 't1':13.2, 't1sem':3.5, 't2':19.8, 't2sem':6.3,                         't4':26.7, 't4sem':5.8 } )
    plotdata.append( {'group':'H', 't1':14.3, 't1sem':3.0, 't2':13.6, 't2sem':4.8, 't3':16.3, 't3sem':4.9, 't4':20.3, 't4sem':3.8 } )

    textstyle = 'font-family: sans-serif; font-weight: bold;'    

    # initialize minplot and begin building our svg...
    p.svgbegin( width=600, height=200 )

    # get an list of unique state names from the data...
    catinfo = p.catinfo( catcol='group', datarows=plotdata )

    # set up the X categorical space and capture panel boundary coordinates...
    panels = p.catspace( axis='X', catlist=catinfo.catlist, poslo=80, poshi=580 )

    # set up the Y numerically scaled space... 
    p.numspace( axis='Y', axmin=0, axmax=35, poslo=80, poshi=180 )

    # render the whole-plot X and Y axes...  
    p.lineprops( color='#ada' )
    p.textprops( ptsize=12, color='#444', cssstyle=textstyle )  
    p.axisrender( axis='X', tics=8, axisline=False, grid=True )
    p.axisrender( axis='Y', axisline=False, inc=10, loc='left-10' )
    p.plotdeco( xlabel="Group", ylabel="weight [g]" )

    # iterate across data rows / panels...
    # we'll use try/except below to handle missing data gracefully
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
            try: p.errorbar( x=key, y=row[key], erramt=row[key+'sem'] )
            except: pass

        # render curve (or bar set) for the current panel...

        if dispmode == 'curves':
            p.lineprops( color='#b44', width=2 )
            p.curvebegin()
            for key in [ 't1', 't2', 't3', 't4' ]:
                try:
                    p.curvenext( x=key, y=row[key] )
                    p.datapoint( x=key, y=row[key], diameter=5, fill='#b44' )
                except: pass

        elif dispmode == 'bars':
            barcolor = [ 'orange', 'blue', 'green', 'red' ]
            icolor = 0
            for key in [ 't1', 't2', 't3', 't4' ]:
                try: p.bar( x=key, y=row[key], width=5, fill=barcolor[icolor] )
                except: pass
                icolor += 1

    if dispmode == 'bars':   # add a legend for the colors
        p.textprops( cssstyle=None, ptsize=9 )
        p.legenditem( label='t1', color='orange', width=40 )
        p.legenditem( label='t2', color='blue', width=40 )
        p.legenditem( label='t3', color='green', width=40 )
        p.legenditem( label='t4', color='red', width=40 )
        p.legendrender( locadj=(50,28), format='across' )   # position the left side of legend at (50, 28)


    # return the SVG...
    return p.svgresult()
