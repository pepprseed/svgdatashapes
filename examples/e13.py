
import svgdatashapes as s

def example13():       # clustered bars
   
    cols = [ 'trial', 'group1', 'group1sem', 'group2', 'group2sem', 'group3', 'group3sem' ]

    dataset = [ (  'Trial1', 33, 2.4, 49, 4.3, 75, 5.8 ),
                (  'Trial2', 35, 3.1, 44, 3.9, 70, 6.1 ),
                (  'Trial3', 30, 2.8, 51, 3.2, 67, 4.0 ),
                (  'Trial4', 34, 3.7, 58, 3.8, 66, 3.9 ),
                (  'Trial5', 27, 5.0, 75, 6.2, 63, 8.2 ) ]

    s.svgbegin( width=550, height=450 )

    textstyle='font-family: sans-serif; font-weight: bold;'
    s.settext( ptsize=12, color='#777', style=textstyle )
    s.setline( color='#aaa' )

    cats = s.uniqcats( datarows=dataset, column=cols.index('trial') )
    s.xspace( svgrange=(80,520), catlist=cats )
    
    # set up the Y numerically scaled space... 
    s.yspace( svgrange=(100,400), datarange=(0,110) )

    # render X and Y axes...  
    s.xaxis( tics=5, stubs=True, stubrotate=0 )
    s.yaxis( axisline=False, grid=True, loc='left-20' )

    # render the bar clusters
    for row in dataset:
        trialname = row[ cols.index( 'trial' ) ]

        for group in ['group1', 'group2', 'group3']:
            # get array index positions for the columns we're working with....
            ycol = cols.index( group )
            semcol = cols.index( group + 'sem' )

            # select color and adjust left or right to make the cluster
            if group == 'group1': adjust = -10; barcolor='#8d8'
            elif group == 'group2': adjust = 0; barcolor = '#88d'
            elif group == 'group3': adjust = 10; barcolor = '#d88'

            s.bar( x=trialname, y=row[ycol], adjust=adjust, color=barcolor )

            s.errorbar( x=trialname, y=row[ycol], erramt=row[semcol], adjust=adjust )

    # define and display the legend...
    s.legenditem( label='Group1', sample='square', color='#8d8', width=100 )
    s.legenditem( label='Group2', sample='square', color='#88d', width=100 )
    s.legenditem( label='Group3', sample='square', color='#d88', width=100 )
    s.legendrender( location='top', xadjust=300 )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
