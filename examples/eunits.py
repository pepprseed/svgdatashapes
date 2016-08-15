
import minplot as p

def example_units():
    # create a fixed-size SVG 500 x 400 and display the test grid 
    p.svgbegin( width=500, height=400, testgrid=True )
    svg = p.svgresult()
    return svg
