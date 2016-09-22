# bar graph plotted from dict rows; color-coded bars; multi-line legend entries

import minplot as p

def example1():

    dataset = []        # create a data set for this self-contained example...
    dataset.append( { 'state':'Ohio',          'avg':12,   'sem':3.4  , 'new':True} )
    dataset.append( { 'state':'Kansas',        'avg':42.1, 'sem':12.4 , 'new':True} )
    dataset.append( { 'state':'Michigan',      'avg':32.2, 'sem':7.3  , 'new':True} )
    dataset.append( { 'state':'Oklahoma',      'avg':72.3, 'sem':22.4 , 'new':False} )
    dataset.append( { 'state':'Mississippi',   'avg':62,   'sem':14.8 , 'new':False} )
    dataset.append( { 'state':'New Mexico',    'avg':44,   'sem':8.8  , 'new':True} )
    dataset.append( { 'state':'Wisconsin',     'avg':55,   'sem':6.2  , 'new':False} )
    dataset.append( { 'state':'South Dakota',  'avg':66.8, 'sem':16.3 , 'new':False} )
    dataset.append( { 'state':'New Hampshire', 'avg':97.5, 'sem':27.8 , 'new':False} )
    dataset.append( { 'state':'Georgia',       'avg':89,   'sem':19.2 , 'new':False} )


    # initialize minplot and begin building our svg...
    p.svgbegin( width=550, height=450 )

    # get an list of unique state names from the data...
    catinfo = p.catinfo( catcol='state', datarows=dataset )

    # set up the X categorical space... 
    p.catspace( axis='X', catlist=catinfo.catlist, poslo=100, poshi=530 )

    # set up the Y numerically scaled space... 
    p.numspace( axis='Y', axmin=0, axmax=140, poslo=100, poshi=400 )

    # render the X and Y axes...  
    p.lineprops( color='#ccc' )
    p.textprops( ptsize=12, color='#444', cssstyle='font-family: sans-serif; font-weight: bold;' )
    p.axisrender( axis='X', tics=8 )
    p.axisrender( axis='Y', axisline=False, grid=True )
    p.plotdeco( ylabel='Avg. Calls / day' )

    # render the column bars and error bars.... set up legend entries too
    p.legenditem( label='2010 expansion\nstates', sample='square', color='pink')
    p.legenditem( label='Pre-2010\nstates', sample='square', color='powderblue')
    p.lineprops( color='#777' )
    for row in dataset:
        if row['new'] == True: barcolor='pink'
        else: barcolor='powderblue'
        p.errorbar( x=row['state'], y=row['avg'], erramt=row['sem'], tailsize=10 )
        p.bar( x=row['state'], y=row['avg'], ybase=0.0, color=barcolor, width=20, opacity=0.8 )

    # render the legend...
    p.legendrender( location='top', format='across' )

    # return the SVG...
    return p.svgresult()
