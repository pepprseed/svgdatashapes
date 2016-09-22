
import minplot as p

def example14():          # horizontal stacked bars
   
    colnames = [ 'trial', 'group1', 'group1sem', 'group2', 'group2sem', 'group3', 'group3sem' ]

    dataset = [ (  'Trial1', 33, 2.4, 49, 4.3, 75, 5.8 ),
                (  'Trial2', 35, 3.1, 44, 3.9, 70, 6.1 ),
                (  'Trial3', 30, 2.8, 51, 3.2, 67, 4.0 ),
                (  'Trial4', 34, 3.7, 58, 3.8, 66, 3.9 ),
                (  'Trial5', 27, 5.0, 75, 6.2, 63, 8.2 ) ]

    p.svgbegin( width=700, height=300 )

    p.datacolumns( namelist=colnames )

    trials = p.catinfo( datarows=dataset, catcol='trial' )   # get the list of Trial category labels
    p.catspace( axis='y', catlist=trials.catlist, poslo=80, poshi=280 )  # categorical space in Y
    
    # set up the X numerically scaled space... 
    p.numspace( axis='x', axmin=0, axmax=200, poslo=100, poshi=400 )

    # render X and Y axes...  
    p.lineprops( color='#aaa' )
    p.textprops( ptsize=12, color='#777', cssstyle='font-family: sans-serif; font-weight: bold;' )  
    p.axisrender( axis='y', tics=5, stubs=True )
    p.axisrender( axis='x', axisline=False, grid=True )

    # render the horizontal stacked bars
    for row in dataset:
        trialname = row[ p.index( 'trial' ) ]
        base = 0
        for group in ['group1', 'group2', 'group3']:
            # select color 
            if group == 'group1': barcolor='#8d8'
            elif group == 'group2': barcolor = '#88d'
            elif group == 'group3': barcolor = '#d88'

            col = p.index( group )

            # with horizontal bars, the sense of x, y arg names are swapped
            p.bar( horiz=True, x=trialname, y=base+row[col], ybase=base, color=barcolor, width=18, opacity=0.5 )

            base += row[col]   # starting location of next stacked bar 

    # define and display the legend...
    p.legenditem( label='Group1', sample='square', color='#8d8', width=100 )
    p.legenditem( label='Group2', sample='square', color='#88d', width=100 )
    p.legenditem( label='Group3', sample='square', color='#d88', width=100 )
    p.legendrender( location='top', xadjust=260 )

    return p.svgresult()
