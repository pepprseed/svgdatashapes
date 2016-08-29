# elementary heatmap 

import minplot as p

def example10():

    # define a 10 x 10 matrix of magnitude values
    plotdata = [ [ 0, 0, 1, 3, 0, 0, 4, 3, 8, 10  ],
                 [ 0, 1, 0, 0, 0, 4, 3, 8, 7, 3   ],
                 [ 1, 0, 0, 0, 4, 3, 12, 7, 3, 0  ],
                 [ 0, 0, 0, 2, 3, 9, 11, 3, 1, 0  ],
                 [ 0, 3, 0, 4, 7, 5, 2, 0, 1, 0   ],
                 [ 0, 0, 4, 3, 12, 16, 3, 0, 1, 0 ],
                 [ 0, 3, 7, 11, 14, 3, 2, 0, 0, 0 ],
                 [ 2, 4, 10, 7, 3, 0, 0, 0, 2, 0  ],
                 [ 7, 9, 6, 2, 0, 2, 0, 1, 0, 0   ],
                 [ 10, 8, 3, 4, 0, 0, 2, 4, 0, 0 ] ]


    p.svgbegin( width=400, height=400 )

    p.textprops( color='#777', cssstyle="font-family: sans-serif; font-weight: bold;" )
    p.lineprops( color='#777' )

    # set up X and Y space...
    p.numspace( axis='X', axmin=0, axmax=10, poslo=100, poshi=350 )
    p.numspace( axis='Y', axmin=0, axmax=10, poslo=100, poshi=350 )

    # render axes and plotting area
    p.axisrender( axis='X', tics=8, loc="min-8" )
    p.axisrender( axis='y', tics=8, loc="min-8" )
    p.plotdeco( shade='#eee', outline=True, rectadj=8 )
    p.plotdeco( ylabel='&Delta; density [g/cm<sup>2</sup>]', xlabel='&Delta; weight [g]')

    iy = 10
    for row in plotdata:
        iy -= 1
        ix = -1
        for val in row:
            ix += 1
            if val == None: continue
            color = findcolor( val )
            p.tooltip( title='N = ' + str(val) )
            p.rectangle( x=ix+0.5, y=iy+0.5, width=1.0, height=1.0, fill=color )

    # p.legenditem( label="Group B", sample='circle', color='#00a', width=80 )
    # p.legendrender( location='top', yadjust=30, format='across' )

    # return the svg 
    return p.svgresult()

def findcolor( val ):
            if val == 0:   return '#000'
            elif val == 1: return '#303'
            elif val == 2: return '#606'
            elif val <= 4: return '#909'
            elif val <= 8: return '#b0b'
            elif val < 12: return '#d0d'
            else:          return '#f0f'
