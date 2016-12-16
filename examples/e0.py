# A simple hello-world example to create a bar graph

import svgdatashapes as s

def example0():

    mydata = [ { 'name':'Group A', 'value':38.4 }, 
               { 'name':'Group B', 'value':67.4 }, 
               { 'name':'Group C', 'value':49.2 } ]

    # get a unique list of the categories for the X axis
    cats = s.uniqcats( datarows=mydata, column="name" )

    # set our text and line properties....
    textstyle = 'font-family: sans-serif; font-weight: bold;'
    s.settext( ptsize=12, color='#444', style=textstyle )
    s.setline( color='#ccc' )

    # begin building our svg
    s.svgbegin( width=550, height=350 )

    # set up our X axis space (categorical) located from x=100 to x=400 in the svg 
    s.xspace( svgrange=(100,400), catlist=cats )

    # set up our Y axis space (numeric) located from y=100 to y=300 in the svg 
    s.yspace( svgrange=(100,300), datarange=(0,100) )

    # render the X and Y axis...
    s.xaxis( tics=8 )
    s.yaxis( axisline=False, grid=True )
    s.plotdeco( ylabel='Score' )

    # render the column bars and error bars.... 
    for row in mydata:
        s.bar( x=row['name'], y=row['value'], color='#8a8', width=50, opacity=0.8 )

    # add a "Goal" line
    s.setline( color='#33a', dash='5,2' )
    s.line( x1='min', y1=60.0, x2='max', y2=60.0 )
    s.label( x='max', y=60.0, text="Goal", xadjust=10 )

    # return the SVG.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
