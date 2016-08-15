# Create a fluidsize SVG and display the test grid.
# Try resizing your browser window down to something small.

import minplot as p

def test_fluid( browser ):    #  browser:  'firefox', 'chrome', 'safari', or 'msie'

    p.svgbegin( width=500, height=400, fluidsize=True, browser=browser, testgrid=True )
    svg = p.svgresult()
    return svg

    # note, in flask you can get the 'browser' string via:  request.user_agent.browser
