# bar graph plotted from dict rows; color-coded bars; multi-line legend entries

import svgdatashapes as s

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

    # get a unique list of state names 
    catlist = s.uniqcats( datarows=dataset, column='state' )

    # set our text and line properties
    textstyle = 'font-family: sans-serif; font-weight: bold;' 
    s.settext( ptsize=12, color='#444', style=textstyle )
    s.setline( color='#ccc' )

    # begin building our svg...
    s.svgbegin( width=550, height=450 )

    # set up categorical X space and numeric Y space...
    s.xspace( svgrange=(100,530), catlist=catlist )
    s.yspace( svgrange=(100,400), datarange=(0,140) )

    # render the X and Y axes...  
    s.xaxis( tics=8 )
    s.yaxis( axisline=False, grid=True )
    s.plotdeco( ylabel='Avg. Calls / day' )

    # render the bars and error bars.... set up legend entries too
    s.setline( color='#777' )
    for row in dataset:
        if row['new'] == True: barcolor='pink'
        else: barcolor='powderblue'
        s.errorbar( x=row['state'], y=row['avg'], erramt=row['sem'], tailsize=10 )
        s.bar( x=row['state'], y=row['avg'], ybase=0.0, color=barcolor, width=20, opacity=0.8 )

    # set up some legend entries and render the legend...
    s.legenditem( label='2010 expansion\nstates', sample='square', color='pink')
    s.legenditem( label='Pre-2010\nstates', sample='square', color='powderblue')
    s.legendrender( location='top', format='across' )

    # return the SVG.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
