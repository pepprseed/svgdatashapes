# curves plot with error bars; irregular X axis stubs; data point tooltips 
# option: dobands .... if True show shaded SEM bands also

import svgdatashapes as s

def example6( dobands=False ):     
   
    # assign some data column names...
    cols=['time','group1','group1sem','group2','group2sem','group3','group3sem']

    dataset = [ [  0, 33, 2.4, 49, 4.3, 75, 5.8 ],
                [  3, 35, 3.1, 44, 3.9, 70, 6.1 ],
                [  6, 30, 2.8, 51, 3.2, 67, 4.0 ],
                [ 12, 34, 3.7, 58, 3.8, 66, 3.9 ],
                [ 24, 27, 5.0, 75, 6.2, 63, 8.2 ] ]
    
    # define our xstubs this way because they are irregularly spaced
    xstubs = [ [ 0, '0' ], [ 3, '3'], [ 6, '6' ], [ 12, '12' ], [ 24, '24' ] ]

    textstyle = 'font-family: sans-serif; font-weight: bold;'
    s.settext( ptsize=12, color='#777', style=textstyle )
    s.setline( color='#aaa' )

    # begin building our svg...
    s.svgbegin( width=550, height=450 )

    # set up the X and Y space
    s.xspace( svgrange=(100,500), datarange=(0,26) )
    s.yspace( svgrange=(100,400), datarange=(0.0,100.0) )

    # render X and Y axes...  
    s.xaxis( axisline=False, stublist=xstubs, loc='bottom-10' )
    s.yaxis( axisline=False, grid=True, loc='left-20' )
    s.plotdeco( xlabel='Months of follow up', xlabeladj=(-20,-10), 
                ylabel='O<sub>2</sub> exchange ratio [%]', ylabeladj=(-20,0) )

    # render the curves 
    for group in ['group1', 'group2', 'group3']:
        # get array index positions for the columns we're working with....
        xcol = cols.index( 'time' ) 
        ycol = cols.index( group )
        semcol = cols.index( group + 'sem' )

        # color...
        if group == 'group1': linecolor = '#8d8'; bandcolor='#cfc'
        elif group == 'group2': linecolor = '#88d'; bandcolor='#ccf'
        elif group == 'group3': linecolor = '#d88'; bandcolor='#fcc'

        # shaded bands option
        if dobands == True:
            s.curvebegin( band=True, fill=bandcolor, opacity=0.5 )
            for row in dataset:
                s.curvenext( x=row[xcol], y=row[ycol]+row[semcol], y2=row[ycol]-row[semcol] )

        # initialize line style and register a legend item...
        s.setline( color=linecolor, width=4 )
        s.legenditem( label=group, sample='line', width=100 )

        # render the curves, error bars, and data points 
        s.curvebegin()
        for row in dataset:
            s.setline( width=4 )
            s.curvenext( x=row[xcol], y=row[ycol] )  
            s.setline( width=2 )   
            s.errorbar( x=row[xcol], y=row[ycol], erramt=row[semcol] )  
        for row in dataset:
            s.tooltip( str(row[ycol])+' %'  )
            s.datapoint( x=row[xcol], y=row[ycol], color=linecolor, diameter=12, opacity=0.5 )  # do datapoints last

    # display the legend...
    s.legendrender( location='top', format='across' )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
