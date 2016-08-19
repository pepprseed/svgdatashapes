import minplot as p

def example1():

    dataset = []        # create a data set for this self-contained example...
    dataset.append( { 'state':'Ohio',          'avg':12,   'sem':3.4  } )
    dataset.append( { 'state':'Kansas',        'avg':42.1, 'sem':12.4 } )
    dataset.append( { 'state':'Michigan',      'avg':32.2, 'sem':7.3  } )
    dataset.append( { 'state':'Oklahoma',      'avg':72.3, 'sem':22.4 } )
    dataset.append( { 'state':'Mississippi',   'avg':62,   'sem':14.8 } )
    dataset.append( { 'state':'New Mexico',    'avg':44,   'sem':8.8  } )
    dataset.append( { 'state':'Wisconsin',     'avg':55,   'sem':6.2 } )
    dataset.append( { 'state':'South Dakota',  'avg':66.8, 'sem':16.3 } )
    dataset.append( { 'state':'New Hampshire', 'avg':97.5, 'sem':27.8 } )
    dataset.append( { 'state':'Georgia',       'avg':89,   'sem':19.2 } )

    # initialize minplot and begin building our svg...
    p.svgbegin( width=550, height=450 )

    # get an list of unique state names from the data...
    catinfo = p.catinfo( catcol='state', datarows=dataset )
    states = catinfo.catlist

    # set up the X categorical space... in the svg it will be 450 minplot units wide
    p.catspace( axis='X', catlist=states, poslo=50, poshi=500 )

    # find an appropriate Y axis min and max 
    for row in dataset:
        p.findrange( testval=row['avg']+row['sem'], testfor='max' )  # bar+errorbar
        p.findrange( testval=row['avg']-row['sem'], testfor='min' )  # bar-errorbar
    yrange = p.findrange( finish=True )
    ymin = yrange.axmin
    ymax = yrange.axmax

    textstyle = "font-family: sans-serif;"    # ensure sans-serif even via [img]

    # set up the Y numerically scaled space... in the svg it will be 300 minplot units high
    p.numspace( axis='Y', axmin=ymin, axmax=ymax, poslo=100, poshi=400 )

    # render X and Y axes...  light red, with light gray grid lines... 
    p.textprops( ptsize=12, color='#caa', cssstyle=textstyle )  
    p.lineprops( color='#e0e0e0' )
    p.axisrender( axis='X', tics=8 )
    p.axisrender( axis='Y', axisline=False, grid=True )

    # render the green curve lineplot.... set up its legend entry too
    p.lineprops( color='#8d8', width=2, dash="5,2"  )
    p.legenditem( label='line\nplot\ncurve', sample='line' )
    p.curvebegin()
    for row in dataset:
        p.curvenext( x=row['state'], y=row['avg'] )

    # render the column bars and error bars.... set up its legend entry too
    p.lineprops( color='#88f', width=0.5 )
    orange = '#fedcba'
    p.legenditem( label='bar\ngraph', sample='square', color=orange, outline=True )
    for row in dataset:
        p.bar( x=row['state'], y=row['avg'], ybase=0.0, fill=orange, opacity=0.8, 
             width=20, outline=True )
        p.errorbar( x=row['state'], y=row['avg'], erramt=row['sem'], tailsize=10 )

    # render the legend...
    p.textprops( ptsize=12, color='#888' )
    p.lineprops( color='#aaf', width=0.5 )
    p.legendrender( location='topleft', format='across' )

    # capture the entire SVG...
    svg = p.svgresult()

    return svg
