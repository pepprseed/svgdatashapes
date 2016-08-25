import minplot as p

def example3():                                       # pie graph example

    dataset1 = [ 0.33, 0.25, 0.2, 0.15, 0.07 ]

    p.svgbegin( width=500, height=300 )

    p.textprops( color='#333', cssstyle="font-family: sans-serif; font-weight: bold;" )

    # set up X space and Y space for the sake of centering pie... axmin and max don't matter
    p.numspace( axis='X', poslo=50, poshi=400, axmin=0.0, axmax=1.0, )
    p.numspace( axis='Y', poslo=50, poshi=280, axmin=0.0, axmax=1.0, )

    p.lineprops( color='#aaa', width=0.5 ); 
    p.plotdeco( outline=True )

    colors = [ '#f00', '#0f0', '#aaf', '#0ff', '#ff0', '#f0f' ]
    labels = [ 'Delaware', 'Vermont', 'Alabama', 'Utah', 'Arkansas' ]
    p.lineprops( color='#fff', width=4 )   # outline slices with a fat white line

    # render the pie graph one slice at a time...
    accum = 0.0; islice = 0
    for val in dataset1:
        p.tooltip( title=labels[islice] )
        p.pieslice( pctval=val, startval=accum+0.4, fill=colors[islice], outline=True, showpct=True, opacity=0.5 )
        p.legenditem( sample='square', label=labels[islice], color=colors[islice] )
        accum += val
        islice += 1

    p.textprops( color='#888' )
    p.legendrender( location='topleft', title='Pie graph example' )

    return p.svgresult()
