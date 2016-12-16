
import svgdatashapes as s

def example14():          # horizontal stacked bars
   
    cols = [ 'trial', 'group1', 'group1sem', 'group2', 'group2sem', 'group3', 'group3sem' ]

    dataset = [ (  'Trial1', 33, 2.4, 49, 4.3, 75, 5.8 ),
                (  'Trial2', 35, 3.1, 44, 3.9, 70, 6.1 ),
                (  'Trial3', 30, 2.8, 51, 3.2, 67, 4.0 ),
                (  'Trial4', 34, 3.7, 58, 3.8, 66, 3.9 ),
                (  'Trial5', 27, 5.0, 75, 6.2, 63, 8.2 ) ]

    s.svgbegin( width=700, height=300 )
    textstyle = 'font-family: sans-serif; font-weight: bold;'
    s.settext( ptsize=12, color='#777', style=textstyle )
    s.setline( color='#aaa' )

    trials = s.uniqcats( datarows=dataset, column=cols.index('trial') )   # get the list of Trial category labels
    s.yspace( svgrange=(80,280), catlist=trials )  # categorical space in Y
    
    # set up the X numerically scaled space... 
    s.xspace( svgrange=(100,400), datarange=(0,200) ) 

    # render X and Y axes...  
    s.xaxis( tics=5, stubs=True )
    s.yaxis( axisline=False, grid=True )

    # render the horizontal stacked bars
    for row in dataset:
        trialname = row[ cols.index( 'trial' ) ]
        base = 0
        for group in ['group1', 'group2', 'group3']:
            # select color 
            if group == 'group1': barcolor='#8d8'
            elif group == 'group2': barcolor = '#88d'
            elif group == 'group3': barcolor = '#d88'

            col = cols.index( group )
            semcol = cols.index( group + 'sem' )

            # with horizontal bars, the sense of x, y arg names are swapped
            s.bar( horiz=True, x=trialname, y=base+row[col], ybase=base, color=barcolor, width=18, opacity=0.5 )

            # also show error bars on each segment
            s.errorbar( horiz=True, x=trialname, y=base+row[col], erramt=row[semcol] )

            base += row[col]   # starting location of next stacked bar 

    # define and display the legend...
    s.legenditem( label='Group1', sample='square', color='#8d8', width=100 )
    s.legenditem( label='Group2', sample='square', color='#88d', width=100 )
    s.legenditem( label='Group3', sample='square', color='#d88', width=100 )
    s.legendrender( location='top', xadjust=260 )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
