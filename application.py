#! /usr/bin/env python

from __future__ import print_function     # python3-style print

from flask import Flask, render_template, request

import examples.e0 as e0
import examples.e1 as e1
import examples.e2 as e2
import examples.e3 as e3
import examples.e4 as e4
import examples.e5 as e5
import examples.e6 as e6
import examples.e7 as e7
import examples.e8 as e8
import examples.e9 as e9
import examples.e10 as e10
import examples.e11 as e11
import examples.e12 as e12
import examples.e13 as e13
import examples.e14 as e14
import examples.e15 as e15
import examples.t_units as t_units
import examples.t_units_fluid as t_units_fluid
import examples.t_axis as t_axis
import examples.t_distribs as t_distribs


# create application...
app = Flask(__name__)

# turn on debugging for apache instance... to see errors tail /var/log/httpd/error_log
# (this should not be enabled for instances exposed to the outside world)
app.config[ "DEBUG" ] = True


@app.route("/")
def welcome():
    return render_template("home")

@app.route("/pages/examplist")
def examplist():
    return render_template("examplist")


@app.route("/LICENSE.txt")
def license():
    return "[Placeholder]", 200, { "Content-Type":"text/plain" }
    
@app.route("/svgdatashapes.py")
def sds_src():
    return "[Placeholder]", 200, { "Content-Type":"text/plain" }

@app.route("/svgdatashapes_dt.py")
def sds_dt_src():
    return "[Placeholder]", 200, { "Content-Type":"text/plain" }

@app.route("/pages/e0")
def example0():
    svg = e0.example0()
    writesvg( svg, "e0" )
    return render_template("view1", filename="e0", title="Hello world", svg=svg )

@app.route("/pages/e1")
def example1():
    svg = e1.example1()
    writesvg( svg, "e1" )
    return render_template("view1", filename="e1", title="Example 1", svg=svg )

@app.route("/pages/e2")
def example2():
    svg = e2.example2()
    writesvg( svg, "e2" )
    return render_template("view1", filename="e2", title="Example 2", svg=svg, sdlink=1,
       comment="Hover over datapoints to see tooltips" )

@app.route("/pages/e3")
def example3():
    svg = e3.example3()
    writesvg( svg, "e3" )
    return render_template("view1", filename="e3", title="Example 3", svg=svg, 
       comment="Hover over slices to see tooltips" )

@app.route("/pages/e4")
def example4():
    svg = e4.example4()
    writesvg( svg, "e4" )
    return render_template("view1", filename="e4", title="Example 4", svg=svg )

@app.route("/pages/e5")
def example5():
    svg = e5.example5()
    writesvg( svg, "e5" )
    return render_template("view1", filename="e5", title="Example 5", svg=svg )

@app.route("/pages/e6")
def example6():
    svg = e6.example6( )
    writesvg( svg, "e6" )
    return render_template("view1", filename="e6", title="Example 6", svg=svg, 
       comment="Hover over datapoints to see tooltips" )

@app.route("/pages/e6a")
def example6a():
    svg = e6.example6( dobands=True )
    writesvg( svg, "e6a" )
    return render_template("view1", filename="e6", title="Example 6a", svg=svg, 
        comment="In this example dobands=True" )

@app.route("/pages/e7")
def example7():
    svg = e7.example7()
    writesvg( svg, "e7" )
    return render_template("view1", filename="e7", title="Example 7", svg=svg, sdlink=2,
        comment="Hover over outlier datapoints for tooltips" )

@app.route("/pages/e7a")
def example7a():
    svg = e7.example7( ylog=True )
    writesvg( svg, "e7a" )
    return render_template("view1", filename="e7", title="Example 7a", svg=svg, sdlink=2,
        comment="In this example ylog=True ... hover over outlier datapoints for tooltips" )

@app.route("/pages/e8")
def example8():
    svg = e8.example8()
    writesvg( svg, "e8" )
    return render_template("view1", filename="e8", title="Example 8", svg=svg, sdlink=3,
         comment="In this example dispmode='curves'" )

@app.route("/pages/e8a")
def example8a():
    svg = e8.example8( dispmode="bars" )
    writesvg( svg, "e8a" )
    return render_template("view1", filename="e8", title="Example 8a", svg=svg, sdlink=3,
         comment="In this example dispmode='bars'" )

@app.route("/pages/e8b")
def example8b():
    svg = e8.example8( dispmode="updown" )
    writesvg( svg, "e8b" )
    return render_template("view1", filename="e8", title="Example 8b", svg=svg, sdlink=3,
         comment="In this example dispmode='updown'" )

@app.route("/pages/e9")
def example9():
    svg = e9.example9()
    writesvg( svg, "e9" )
    return render_template("view1", filename="e9", title="Example 9", svg=svg, sdlink=2 )

@app.route("/pages/e10")
def example10():
    svg = e10.example10()
    writesvg( svg, "e10" )
    return render_template("view1", filename="e10", title="Example 10", svg=svg, 
        comment="Hover over cells for tooltips" )

@app.route("/pages/e11")
def example11():
    svg = e11.example11()
    writesvg( svg, "e11" )
    return render_template("view1", filename="e11", title="Example 11", svg=svg, sdlink=4 )

@app.route("/pages/e12")
def example12():
    svg = e12.example12()
    writesvg( svg, "e12" )
    return render_template("view1", filename="e12", title="Example 12", svg=svg )

@app.route("/pages/e13")
def example13():
    svg = e13.example13()
    writesvg( svg, "e13" )
    return render_template("view1", filename="e13", title="Example 13", svg=svg )

@app.route("/pages/e14")
def example14():
    svg = e14.example14()
    writesvg( svg, "e14" )
    return render_template("view1", filename="e14", title="Example 14", svg=svg )

@app.route("/pages/e15")
def example15():
    svg = e15.example15()
    writesvg( svg, "e15" )
    return render_template("view1", filename="e15", title="Example 15", svg=svg )


@app.route("/pages/test_axis")
def test_axis():
    svg = t_axis.test_axis()
    return render_template("view1", filename="t_axis", title="Axis rendering test", svg=svg )


@app.route("/pages/test_units")
def test_units():
    svg = t_units.test_units()
    return render_template("view1", filename="t_units", title="SVG units", svg=svg )


@app.route("/pages/test_fluid_ff")
def test_fluid_ff():
    svg = t_units_fluid.test_units_fluid( browser='firefox' )
    return render_template("view1", filename="t_units_fluid", title="SVG units with fluid sizing (static firefox example)", svg=svg )

@app.route("/pages/test_fluid_wk")
def test_fluid_wk():
    svg = t_units_fluid.test_units_fluid( browser='chrome' )
    return render_template("view1", filename="t_units_fluid", title="SVG units with fluid sizing (static chrome / webkit example)", svg=svg )


@app.route("/pages/test_distribs")
def test_distribs():
    outstr = t_distribs.test_distribs()
    return render_template("view1", filename="t_distribs", title="Test of frequency distributions and percentiles computation", textresult=outstr )
 
 
@app.route("/pages/sampledata/<int:id>")
def sampledata( id ):
    return render_template( "sampledata", id=id )



def writesvg( svgcode, basename ):
    # refresh the static copy with latest...
    pathname = "./static/examples/" + basename + ".svg"
    try:
        fp = open( pathname, "w" )
    except:
        print( "ERROR: cannot open " + pathname + " for write" )
        return False

    print( '<?xml version="1.0" encoding="utf-8"?>', file=fp )   # these headers necessary for full functionality eg. &Delta;
    print( '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">', file=fp )

    # html special chars (beyond a basic few) cause xml problems via <img> ... remove them
    print( svgcode.replace( "&Delta;", ""), file=fp )
    fp.close()

# browser = request.user_agent.browser


# if this is a personal development version, do:   python application.py  ...then visit http://bhmpd01.jax.org:5005
# note, to access across network flask requires host="0.0.0.0"
if __name__ == '__main__':
    app.debug = True   # turn on debugging for gitclone instance
    app.run(host="0.0.0.0", port=5005)
