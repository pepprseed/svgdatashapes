# elementary heatmap 

import svgdatashapes as s

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


    s.svgbegin( width=400, height=400 )

    s.settext( color='#777', style='font-family: sans-serif; font-weight: bold;' )
    s.setline( color='#777' )

    # set up X and Y space...
    s.xspace( svgrange=(100,350), datarange=(0,10) )
    s.yspace( svgrange=(100,350), datarange=(0,10) )

    # render axes and plotting area
    s.xaxis( tics=8, loc='min-8' )
    s.yaxis( tics=8, loc='min-8' )
    s.plotdeco( shade='#eee', outline=True, rectadj=8 )
    s.plotdeco( ylabel='&Delta; density [g/cm<sup>2</sup>]', xlabel='&Delta; weight [g]')

    iy = 10
    for row in plotdata:
        iy -= 1
        ix = -1
        for val in row:
            ix += 1
            if val == None: continue
            color = findcolor( val )
            s.tooltip( title='N = ' + str(val) )
            s.rectangle( x=ix+0.5, y=iy+0.5, width=1.0, height=1.0, color=color )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()

def findcolor( val ):
            if val == 0:   return '#000'
            elif val == 1: return '#303'
            elif val == 2: return '#606'
            elif val <= 4: return '#909'
            elif val <= 8: return '#b0b'
            elif val < 12: return '#d0d'
            else:          return '#f0f'
