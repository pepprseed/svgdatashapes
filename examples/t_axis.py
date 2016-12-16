import svgdatashapes as s

def test_axis():

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

    textstyle = 'font-family: sans-serif;'    # ensure sans-serif even via [img]

    # building our svg...
    s.svgbegin( width=800, height=600 )

    s.setline( color='#555' )
    s.settext( color='#444', style=textstyle )  


    # left column ... X categorical space... 
    cats = s.uniqcats( datarows=dataset, column='state' )
    s.xspace( svgrange=(50,350), catlist=cats )

    s.yspace( svgrange=(500,550), datarange=(0,10) )
    s.xaxis( tics=8 )   # use default stubrotate

    s.yspace( svgrange=(400,450), datarange=(0,10) )
    s.xaxis( tics=8, stubrotate=90 )

    s.yspace( svgrange=(300,350), datarange=(0,10) )
    s.xaxis( tics=8, stubrotate=-45 )

    s.yspace( svgrange=(200,250), datarange=(0,10) )
    s.xaxis( tics=8, stubrotate=60 )


    # right column ... X numeric space....
    s.xspace( svgrange=(450,750), datarange=(0,10000) )

    s.yspace( svgrange=(500,550), datarange=(0,10) )
    s.xaxis( tics=8 )   # use default stubrotate

    s.yspace( svgrange=(400,450), datarange=(0,10) )
    s.xaxis( tics=8, stubrotate=0 )   

    s.yspace( svgrange=(300,350), datarange=(0,10) )
    s.xaxis( tics=8, stubrotate=90 )   

    s.yspace( svgrange=(200,250), datarange=(0,10) )
    s.xaxis( tics=8, stubrotate=-45 )   

    s.yspace( svgrange=(100,150), datarange=(0,10) )

    xstubs = [ [ 0, '0' ], [ 1000, '1000'], [ 2000, '2000' ], [ 5000, '5000' ], [ 10000, '10000' ] ]
    s.xaxis( tics=8, stublist=xstubs, stubrotate=90 )
  
    return s.svgresult()
