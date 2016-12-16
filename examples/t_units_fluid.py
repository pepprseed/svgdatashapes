# Create a fluidsize SVG and display the test grid.
# Try resizing your browser window down to something small.
# note, in flask you can get the 'browser' string via:  request.user_agent.browser

import svgdatashapes as s

def test_units_fluid( browser ):    #  browser:  'firefox', 'chrome', 'safari', or 'msie'

    s.svgbegin( width=500, height=400, fluidsize=True, browser=browser, testgrid=True )
    return s.svgresult()

