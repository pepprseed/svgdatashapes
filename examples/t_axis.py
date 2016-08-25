import minplot as p

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

    # initialize minplot and begin building our svg...
    p.svgbegin( width=800, height=600 )

    p.lineprops( color='#555' )
    p.textprops( color='#444', cssstyle=textstyle )  


    # left column ... X categorical space... 
    catinfo = p.catinfo( catcol='state', datarows=dataset )
    p.catspace( axis='X', catlist=catinfo.catlist, poslo=50, poshi=350 )

    p.numspace( axis='Y', axmin=0, axmax=10, poslo=500, poshi=550 )
    p.axisrender( axis='X', tics=8 )   # use default stubrotate

    p.numspace( axis='Y', axmin=0, axmax=10, poslo=400, poshi=450 )
    p.axisrender( axis='X', tics=8, stubrotate=90 )

    p.numspace( axis='Y', axmin=0, axmax=10, poslo=300, poshi=350 )
    p.axisrender( axis='X', tics=8, stubrotate=-45 )

    p.numspace( axis='Y', axmin=0, axmax=10, poslo=200, poshi=250 )
    p.axisrender( axis='X', tics=8, stubrotate=60 )


    # right column ... X numeric space....
    p.numspace( axis='X', axmin=0, axmax=10000, poslo=450, poshi=750 )

    p.numspace( axis='Y', axmin=0, axmax=10, poslo=500, poshi=550 )
    p.axisrender( axis='X', tics=8 )  # use default stubrotate

    p.numspace( axis='Y', axmin=0, axmax=10, poslo=400, poshi=450 )
    p.axisrender( axis='X', tics=8, stubrotate=0 )

    p.numspace( axis='Y', axmin=0, axmax=10, poslo=300, poshi=350 )
    p.axisrender( axis='X', tics=8, stubrotate=90 )

    p.numspace( axis='Y', axmin=0, axmax=10, poslo=200, poshi=250 )
    p.axisrender( axis='X', tics=8, stubrotate=-45 )

    p.numspace( axis='Y', axmin=0, axmax=10, poslo=100, poshi=150 )
    xstubs = [ [ 0, "0" ], [ 1000, "1000"], [ 2000, "2000" ], [ 5000, "5000" ], [ 10000, "10000" ] ]
    p.axisrender( axis='X', tics=8, stublist=xstubs, stubrotate=90 )
  
    
    return p.svgresult()
