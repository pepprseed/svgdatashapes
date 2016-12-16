# pie chart; slices have tooltips

import svgdatashapes as s

def example3():                                       # pie graph example

    dataset1 = [ 0.33, 0.25, 0.2, 0.15, 0.07 ]

    s.svgbegin( width=500, height=300 )

    textstyle = 'font-family: sans-serif; font-weight: bold;' 
    s.settext( color='#333', style=textstyle )

    # set up X space and Y space for centering of pie... 
    s.xspace( svgrange=(50,400) )
    s.yspace( svgrange=(50,280) )

    s.setline( color='#aaa', width=0.5 ); 
    s.plotdeco( outline=True )

    colors = [ '#f00', '#0f0', '#aaf', '#0ff', '#ff0', '#f0f' ]
    labels = [ 'Delaware', 'Vermont', 'Alabama', 'Utah', 'Arkansas' ]

    # render the pie graph one slice at a time... and add a legend entry for each
    s.setline( color='#fff', width=4 )   # outline the slices w/ a fat white line
    accum = 0.4;     # start at 0.4 to rotate entire pie for pleasing appearance
    islice = 0
    for val in dataset1:
        s.tooltip( title=labels[islice] )
        s.pieslice( pctval=val, startval=accum, color=colors[islice], 
             outline=True, showpct=True, opacity=0.5 )
        s.legenditem( sample='square', label=labels[islice], color=colors[islice] )
        accum += val
        islice += 1

    # render the legend
    s.settext( color='#888' )
    s.legendrender( location='top', title='Pie graph example' )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
