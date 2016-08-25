
import minplot as p

def example6( bandsopt=False ):     
    # produce a plot with 3 curves, error bars, and irregular X axis stubs, and data point tooltips 
    # bandsopt .... if True show shaded SEM bands also
   
    colnames = [ "time", "group1", "group1sem", "group2", "group2sem", "group3", "group3sem" ]

    dataset = [ [  0, 33, 2.4, 49, 4.3, 75, 5.8 ],
                [  3, 35, 3.1, 44, 3.9, 70, 6.1 ],
                [  6, 30, 2.8, 51, 3.2, 67, 4.0 ],
                [ 12, 34, 3.7, 58, 3.8, 66, 3.9 ],
                [ 24, 27, 5.0, 75, 6.2, 63, 8.2 ] ]
    
    # define our xstubs this way because they are irregularly spaced
    xstubs = [ [ 0, "0" ], [ 3, "3"], [ 6, "6" ], [ 12, "12" ], [ 24, "24" ] ]

    # initialize minplot and begin building our svg...
    p.svgbegin( width=550, height=450 )

    # register our data columns...
    p.datacolumns( namelist=colnames )

    # set a css text style
    textstyle = "font-family: sans-serif; font-weight: bold;"    

    # set up the X axis for time
    p.numspace( axis='X', axmin=0, axmax=26, poslo=100, poshi=500 )

    # set up the Y numerically scaled space... 
    p.numspace( axis='Y', axmin=0.0, axmax=100.0, poslo=100, poshi=400 )
    # with alt1 use: p.numspace( axis='Y', axmin=yrange.axmin, axmax=yrange.axmax, poslo=100, poshi=400 )

    # render X and Y axes...  
    p.lineprops( color='#aaa' )
    p.textprops( ptsize=12, color='#777', cssstyle=textstyle )  
    p.axisrender( axis='X', axisline=False, stublist=xstubs, loc='bottom-10' )
    p.axisrender( axis='Y', axisline=False, grid=True, loc='left-20' )
    p.plotdeco( xlabel="Months of follow up", xlabeladj=(-20,-10), ylabel="O<sub>2</sub> exchange ratio [%]", ylabeladj=(-20,0) )

    # render the curves 
    for group in ["group1", "group2", "group3"]:
        # use icol() to get array index position from column name
        xcol = p.icol( "time" ) 
        ycol = p.icol( group )
        semcol = p.icol( group + "sem" )

        # color...
        if group == "group1": linecolor = "#8d8"; bandcolor="#cfc"
        elif group == "group2": linecolor = "#88d"; bandcolor="#ccf"
        elif group == "group3": linecolor = "#d88"; bandcolor="#fcc"

        # shaded bands option
        if bandsopt == True:
            p.curvebegin( band=True, fill=bandcolor, opacity=0.5 )
            for row in dataset:
                p.curvenext( x=row[xcol], y=row[ycol]+row[semcol], y2=row[ycol]-row[semcol] )

        # initialize line style and register a legend item...
        p.lineprops( color=linecolor, width=4 )
        p.legenditem( label=group, sample='line', width=100 )

        # render the curves, error bars, and data points 
        p.curvebegin()
        for row in dataset:
            p.lineprops( width=4 )
            p.curvenext( x=row[xcol], y=row[ycol] )  
            p.lineprops( width=2 )   
            p.errorbar( x=row[xcol], y=row[ycol], erramt=row[semcol] )  
        for row in dataset:
            p.tooltip( str(row[ycol])+" %"  )
            p.datapoint( x=row[xcol], y=row[ycol], fill=linecolor, diameter=12, opacity=0.5 )  # do datapoints last

    # display the legend...
    p.legendrender( location='topleft', format='across' )

    # capture the entire SVG...
    return p.svgresult()
