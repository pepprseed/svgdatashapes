
# wind barbs over time (x axis) for several elevations (y axis)

import minplot as p
import minplot_dt as pdt
import sampledata4

def example11():                                          

    winddata = sampledata4.winddata()   # get some data

    p.svgbegin( width=800, height=500 )
    pdt.dateformat( '%Y-%m-%d %H:%M:%S' )

    p.datacolumns( namelist=[ 'timestamp', 'elevation', 'speed', 'direction' ] )

    # find timestamp range...
    xrange = pdt.daterange( dtcol='timestamp', datarows=winddata, nearest='hour', inc='3hour', stubformat='%l%P' )

    # set up X space...
    p.numspace( axis='X', axmin=xrange.axmin, axmax=xrange.axmax, poslo=100, poshi=750 )

    # find Y range and set up Y space...
    for row in winddata:
        p.findrange( testval=row[ p.index( 'elevation' ) ] )  
    yrange = p.findrange( finish=True )
    p.numspace( axis='Y', axmin=yrange.axmin, axmax=yrange.axmax, poslo=60, poshi=480 )

    p.lineprops( color='#777' ); 
    p.textprops( color='#555', cssstyle='font-family: sans-serif; font-weight: bold;' )
    p.plotdeco( title='Wind speed is indicated by size of the little barb at the tip of each vector.', 
                ylabel='Elevation (m)', xlabel='2003-05-07  time', outline=True )

    # render axes...
    p.axisrender( axis='X', stublist=xrange.stublist, tics=8, stubrotate=0 )
    p.axisrender( axis='y', tics=8 )

    p.lineprops( color='#33f' );  # blue
    # render windbarbs
    for row in winddata:
        xloc = pdt.dateitem( 'timestamp', row )   # get 'timestamp' and convert to int for plotting
        yloc = row[ p.index( 'elevation' ) ]    
        winddir = row[ p.index( 'direction' ) ] 
        windspeed = row[ p.index( 'speed' ) ]     # the size of the barb indicates wind speed

        p.arrow( x1=xloc, y1=yloc, direction=winddir, magnitude=40, tiptype='barb', headlen=windspeed )
        p.datapoint( x=xloc, y=yloc, diameter=5, color='#888' )

    return p.svgresult()
