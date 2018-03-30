
# wind barbs over time (x axis) for several elevations (y axis)

import svgdatashapes as s
import svgdatashapes_dt as sdt          # for date/time support
import examples.sampledata4 as sampledata4 

def example11():                                          

    winddata = sampledata4.winddata()   # get some data

    s.svgbegin( width=800, height=550 )
    sdt.dateformat( '%Y-%m-%d %H:%M:%S' )

    # assign names to the data columns
    cols=[ 'timestamp', 'elevation', 'speed', 'direction' ]

    # find timestamp range and set up X space..
    xrange = sdt.daterange( column=cols.index('timestamp'), datarows=winddata, nearest='hour', inc='3hour', stubformat='%l%P' )
    s.xspace( svgrange=(100,750), datarange=xrange )

    # find Y range and set up Y space...
    for row in winddata:
        s.findrange( testval=row[ cols.index( 'elevation' ) ] )  
    yrange = s.findrange( finish=True )
    s.yspace( svgrange=(60,480), datarange=yrange )

    s.setline( color='#777' ); 
    s.settext( color='#555', style='font-family: sans-serif; font-weight: bold;' )
    s.plotdeco( title='Wind speed is indicated by the size of the little barb at tip of each vector.', 
                ylabel='Elevation (m)', xlabel='2003-05-07  time', outline=True )

    # render axes...
    s.xaxis( stublist=xrange.stublist, tics=8, stubrotate=0 )
    s.yaxis( tics=8 )

    s.setline( color='#33f' );  # blue
    # render windbarbs
    for row in winddata:
        xloc = sdt.toint( row[cols.index('timestamp')] )   # get 'timestamp' and convert to int for plotting
        yloc = row[ cols.index( 'elevation' ) ]    
        winddir = row[ cols.index( 'direction' ) ] 
        windspeed = row[ cols.index( 'speed' ) ]     # the size of the barb indicates wind speed

        s.arrow( x1=xloc, y1=yloc, direction=winddir, magnitude=40, tiptype='barb', headlen=windspeed )
        s.datapoint( x=xloc, y=yloc, diameter=5, color='#888' )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()
