
import math
import collections

class AppError(Exception): pass

p_svg = {}
p_svg["active"] = False; p_svg["out"] = ""; p_svg["height"] = 0; p_svg["width"] = 0; 

p_space = [ {}, {} ]; 
p_space[0]["scalefactor"] = None; p_space[1]["scalefactor"] = None

p_line = {}
p_line["props"] = ""

p_text = {}
p_text["props"] = ""; p_text["anc"] = "start"; p_text["rot"] = None; p_text["adj"] = None; p_text["height"] = None; 

p_ar = {}
p_ar["active"] = False

p_curve = {}
p_leg = []
p_tt = {}

p_clust = {}
p_clust["mode"] = None; 
p_clust["xofslist"] = (0,0,4, 0,-4,4,-4,-4, 4, 0,-6,0,6, 4,-8,4,8,-4,-8,-4, 8, 0,  0,10,-10, 4,  4,10,-10,-4, -4,10,-10, 8,-8,-8, 8)
p_clust["yofslist"] = (0,4,0,-4, 0,4,-4, 4,-4,-6, 0,6,0,-8, 4,8,4,-8,-4, 8,-4,10,-10, 0,  0,10,-10, 4,  4,10,-10,-4, -4, 8,-8, 8,-8)

p_fieldnames = None;

p_dtformat = "%Y-%m-%d"


def _init():
    # initialize the environment / state
    global p_svg, p_space, p_clust, p_curve, p_leg, p_tt, p_ar, p_dtformat
    p_svg["active"] = True
    p_space[0]["scalefactor"] = None; p_space[1]["scalefactor"] = None
    p_clust["mode"] = None
    p_curve["x"] = p_curve["y"] = None
    p_leg = []
    p_tt = {} 
    p_ar = {}; p_ar["active"] = False
    p_fieldnames = None
    p_dtformat = "%Y-%m-%d"
    return True


### setting text, line, color, symbol properties

def textprops( css=None, ptsize=10, color="#000000", opacity=1.0, anchor="start", rotate=None, adjust=None, nodefaults=False ):
    # set text properties for subsequent text rendering... 
    global p_text
    p_text = {}
    p_text["props"] = ""; 

    if css != None:         
        if ":" in css: p_text["props"] += "style=" + quo(css) + " "
        else:          p_text["props"] += "class=" + quo(css) + " "

    if nodefaults == True: pass
        # means we ignore function kwparm defaults, allowing a parent <g> style to style the text (except 'rotate' and 'adjust').
        # But this app code needs to know ptsize / text height for various layouts (we won't have this if font-size was 
        # styled in css= or a parent <g>.  So for best results ptsize= should always be given or else we go with ptsize=10.
    else:
        p_text["props"] += "font-size=\"" + str(ptsize) + "pt\" "
        color = str(color)
        if color != "#000000":  p_text["props"] += "fill=" + quo(color) + " "   # black is the svg color hard default
        try:
            if opacity != 1.0:      p_text["props"] += "fill-opacity=" + quo(opacity) + " "  # 1.0 the svg opacity hard default
        except: raise AppError( "textprops() is expecting numeric opacity value but got: " + str(opacity) )

    anchor = str(anchor)
    if anchor not in ["start", "middle", "end"]: raise AppError( "textprops() anchor must be either 'start', 'middle', or 'end'" + str(anchor) )
    p_text["anc"] = anchor
    if rotate != None:
        try: rotate = float(rotate)
        except: raise AppError( "textprops() is expecting numeric rotate value but got: " + str(rotate) )
    p_text["rot"] = rotate
    if adjust != None:
       try: testnum = adjust[0] + adjust[1]
       except: raise AppError( "textprops() is expecting adjust as 2-member numeric list, but got: " + str(adjust) )
    p_text["adj"] = adjust
    p_text["height"] = (ptsize/72.0)*100.0
    p_text["ptsize"] = ptsize   # in case needed by app
    return True

def lineprops( css=None, width=1.0, color="#000000", opacity=1.0, dash=None, nodefaults=False ):
    # set line properties for subsequent line rendering...
    global p_line
    p_line = {}
    p_line["props"] = ""; 

    if css != None:        
        if ":" in css: p_line["props"] += "style=" + quo(css) + " "
        else:          p_line["props"] += "class=" + quo(css) + " "
    
    if nodefaults == True: pass
        # means we ignore kwparm defaults, allowing a parent <g> style to control everything about the line.
    else:
        if css == None or "stroke:" not in css: p_line["props"] += "stroke=" + quo(str(color)) + " "
        try: width = float(width)
        except: raise AppError( "lineprops() is expecting numeric width value but got: " + str(width) )
        if width != 1.0: p_line["props"] += "stroke-width=" + quo(width) + " "       # 1.0 is the svg linewidth hard default
        try:
            if opacity != 1.0:     p_line["props"] += "stroke-opacity=" + quo(opacity) + " "  # 1.0 is the svg opacity hard default
        except: raise AppError( "lineprops() is expecting numeric opacity value but got " + str(opacity) )
        if dash != None:       p_line["props"] += "stroke-dasharray=" + quo( dash ) + " " 
    return True


### low-level drawing routines 

def lin( x1, y1, x2, y2, props=None ):
    # draw line from x1,y1 to x2,y2 (native) using current line properties. (props arg is used internally to override)
    global p_svg
    try: testnum = float(x1) + y1 + x2 + y2
    except: raise AppError( "lin() is expecting four numeric values: " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) )
    if props == None:  props = p_line["props"]
    p_svg["out"] += "<polyline points=\"" + str2f(x1) + "," + str2f(flip(y1)) + " " + \
         str2f(x2) + "," + str2f(flip(y2)) + "\" " + props + " />\n"
    return True

def txt( x, y, txt, anchor=None ):
    # render text at x,y (native) using current text properties
    global p_svg
    txt = str(txt)
    try: testnum = float(x) + y 
    except: raise AppError( "txt() is expecting two numeric values: " + str(x) + " " + str(y) )
    if p_text["adj"] != None and len(p_text["adj"]) == 2: x += p_text["adj"][0]; y += p_text["adj"][1]   
    p_svg["out"] += "<text x=" + quo( str2f(x) ) + " y=" + quo( str2f(flip(y)) ) + " " + p_text["props"]
    if anchor != None:  # allows app to override
        if anchor not in ["start", "middle", "end"]: raise AppError( "txt() is expecting anchor of either 'start', 'middle', or 'end', but got: " + str(anchor) )
        p_svg["out"] += " text-anchor=" + quo( anchor ) + " "
    else:
        p_svg["out"] += " text-anchor=" + quo( p_text["anc"] ) + " "
    if p_text["rot"] != None and p_text["rot"] != 0:
        p_svg["out"] += "transform=\"rotate(" + str(p_text["rot"]) + " " + str2f(x) + "," + str2f(flip(y)) + ")\" "
    len0 = len(txt)
    tspanstr = "</tspan><tspan x=" + quo(str2f(x)) + " dy=\"1.05em\">"
    txt = txt.replace( "\n", tspanstr )  # support newlines
    if len(txt) != len0: txt = "<tspan>" + txt + "</tspan>"  
    len0 = len(txt)
    hw = p_text["height"]*0.6;  ps0 = p_text["ptsize"]; pssup = p_text["ptsize"] * 0.8; 
    tspanstr = "<tspan dy=\"-" + str2f(hw) + "\" font-size=\"" + str2f(pssup) + "pt\">"
    tspanstr2 = "</tspan><tspan dy=\"" + str2f(hw) + "\">"
    txt = txt.replace( "<sup>", tspanstr ).replace( "</sup>", tspanstr2 ) # support <sup> </sup> constructs
    hw = p_text["height"]*0.3
    tspanstr = "<tspan dy=\"" + str(hw) + "\" font-size=\"" + str2f(pssup) + "pt\">"
    tspanstr2 = "</tspan><tspan dy=\"-" + str(hw) + "\">"
    txt = txt.replace( "<sub>", tspanstr ).replace( "</sub>", tspanstr2 ) # support <sub> </sub> constructs
    if len(txt) != len0: txt = txt + "</tspan>"  
    p_svg["out"] += ">" + txt + "</text>\n"
    return True

def rect( x1, y1, x2, y2, fill="#e0e0e0", opacity=1.0, outline=False ):
    # render shaded rectangle with lower-left at x1,y1 and upper right at x2,y2  (native)
    global p_svg
    try: testnum = float(x1) + y1 + x2 + y2
    except: raise AppError( "rect() is expecting four numeric values, but got: " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) )
    p_svg["out"] += "<rect x=" + quo(x1) + " y=" + quo(str2f(flip(y2))) + " width=" + quo(str2f(x2-x1)) + \
                     " height=" + quo(str2f(y2-y1)) + " "
    if fill == None: fill = "none"
    _polyparms( fill, opacity, outline )
    p_svg["out"] += "/>\n"
    return True

def circle( x, y, diameter, fill="#e0e0e0", opacity=1.0, outline=False ):
    # render a circle
    global p_svg
    try: testnum = float(x) + y + diameter
    except: raise AppError( "circle() is expecting x, y, diameter as numeric values, but got " + str(x) + " " + str(y) + " " + str(diameter) )
    p_svg["out"] += "<circle cx=" + quo(str2f(x)) + " cy=" + quo(str2f(flip(y))) + " r=" + quo(str2f(diameter/2.0)) + " "
    _polyparms( fill, opacity, outline )
    p_svg["out"] += "/>\n"
    return True

def polygon( ptlist, fill="#e0e0e0", opacity=1.0, outline=False ):
    # render a polygon
    global p_svg
    p_svg["out"] += "<polygon points=\""
    for pt in ptlist:
        p_svg["out"] += str2f(pt[0]) + "," + str2f(flip(pt[1])) + " "
    if fill == None: raise AppError( "the fill= arg is mandatory for polygon()" )
    p_svg["out"] += "\" "
    _polyparms( fill, opacity, outline )
    p_svg["out"] += "/>\n"
    return True

def _polyparms( fill, opacity, outline ):
    # this code shared by several routines above 
    if outline == True: p_svg["out"] += p_line["props"] + " "
    if fill != None: p_svg["out"] += "fill=" + quo(fill) + " "
    try:
        if opacity != 1.0: p_svg["out"] += "opacity=" + quo(opacity)
    except: raise AppError( "expecting numeric 'opacity' value, but got: " + str(opacity) )
    return True

def _gtooltip( mode ):
    # manage tooltip attributes in an svg <g> tag, which will contain a plot element....
    # mode is either "begin" or "end"
    global p_svg, p_tt
    if len(p_tt) < 1: return False   # nothing to do
    elif mode == "begin":    # create a new <g> tag and maybe an <a> tag...
        if p_tt["popover"] == False: p_svg["out"] += "<g><title>" + p_tt["title"] + "</title>\n"
        else: p_svg["out"] += "<g data-toggle=\"popover\" title=\"" + p_tt["title"] + "\" data-content=\"" + p_tt["content"] + "\">\n"
        if p_tt["url"] != None: 
            p_svg["out"] += "<a xlink:href=\"" + p_tt["url"] + "\" " 
            if p_tt["target"] != None: p_svg["out"] += "target=" + quo( p_tt["target"] )
            p_svg["out"] += " >\n"
    elif mode == "end":    # close out the tags created earlier...
        if p_tt["url"] != None: p_svg["out"] += "</a>\n"
        p_svg["out"] += "</g>\n" 
        p_tt = {}    # clear 
    return True

def comment( text ):      # embed a comment in the result SVG...
    global p_svg
    p_svg["out"] += "<!-- " + text + " -->\n"; return True



### low-level dataspace-to-nativespace conversion routines 

def nx( dataval ):
    # for an x location in data space, return equivalent native coordinate
    return nu( "X", dataval )

def ny( dataval ):
    # for a Y location in data space, return equivalent native coordinate
    return nu( "Y", dataval )

def nu( axis, dataval ):
    # for an x or Y location in data space, return equivalent native coordinate
    iax = _getiax( axis )
    scaletype = p_space[iax]["scaletype"] 
    
    if scaletype == "categorical" and type( dataval ) is not int:  
        # an int dataval can access a category... it's simply treated as a number below...
        try:  ival = p_space[iax]["catlist"].index( str( dataval ))
        except:  raise ValueError( "encountered an unrecognized category term in " + axis + " space: " + str(dataval) )
        dataval = ival + 0.5

    minval = p_space[iax]["min"]; poslo = nmin(axis); poshi = nmax(axis) 
    scalefactor = p_space[iax]["scalefactor"]; rev = p_space[iax]["reverse"]

    try:
        if scaletype[:3] != "log" and rev == False:            # linear low-to-hi 
            return poslo + ((dataval - minval) * scalefactor )
        elif scaletype[:3] != "log" and rev == True:           # linear hi-to-low
            return poshi - ((dataval - minval) * scalefactor )
        else:
            pass
    except: 
        raise ValueError( "encountered a non-numeric data value in " + axis + " space: " + str(dataval) )

    try:
        if dataval <= 0.0:   # allow, tag it to minima
            return poslo
        plus1 = 0.0
        if scaletype == "log+1":
            plus1 = 1.0
        if scaletype[:3] == "log" and rev == False:             # log low-to-hi
            return poslo + ((_log(dataval+plus1) - _log(minval+plus1)) * scalefactor)
        elif scaletype[:3] == "log" and rev == True:           # log hi-to-low
            return poshi - ((_log(dataval+plus1) - _log(minval+plus1)) * scalefactor)
    except:
        raise ValueError( "encountered an incompatible data value in " + axis + " space: " + str(dataval) )

def ndist( axis, datadist ):
    # for a distance in X or Y numeric scaled space (but not categorical), return equialent distance in native units.
    return  nu( axis, datadist ) - nu( axis, 0.0 )

def inspace( axis, dataval ):
    # if dataval is within the plot area return True; if it's outside return False
    iax = _getiax( axis )
    natval = nu( axis, dataval ) 
    if natval >= nmin(axis) and natval <= nmax(axis): return True
    else: return False
 
def nmin( axis ): iax = _getiax( axis ); return p_space[iax]["poslo"]

def nmax( axis ): iax = _getiax( axis ); return p_space[iax]["poshi"]

def dmin( axis ): iax = _getiax( axis ); return p_space[iax]["min"]

def dmax( axis ): iax = _getiax( axis ); return p_space[iax]["max"]



### primary user-visible funtions........


def svgbegin( width=None, height=None, fluidsize=False, browser=None, testgrid=None, bgcolor=None, notag=False ):
    # begin a new svg graphic
    global p_svg
    p_svg["out"] = "<svg "
    boilerplate = "xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\""
    try: width = int(width); height = int(height)
    except: raise ValueError( "svg_begin() is expecting numeric width and height args." )
    vb = "viewBox=" + quo( "0 0 " + str(width) + " " + str(height) ) 
    if fluidsize == True:
        if browser == None: raise AppError( "svgbegin() is expecting the browser arg with fluidsize==True" )
        elif browser == "firefox":
            p_svg["out"] += vb    # Firefox needs just the vb
        elif browser == "chrome" or browser == "safari":
            p_svg["out"] += vb + " height=\"100%\" width=\"100%\" " # Chrome/safari needs vb +  height="100%" width="100%" 
        elif browser == "msie":
            p_svg["out"] += vb + " height=" + quo(height)   # MSIE needs vb + eg. height="400" 
    else:
        p_svg["out"] += "width=" + quo(width) + " height=" + quo(height)     # fixed size (viewBox not used)
    p_svg["out"] += " " + boilerplate + ">\n" 
    if notag == True:  p_svg["out"] = ""
    p_svg["out"] += "<!-- Inline SVG data display produced by minplot -->\n"  # this line must remain intact per Terms of Use
    p_svg["height"] = height; p_svg["width"] = width   # set globals
    if bgcolor != None:  rect( 0, 0, width, height, bgcolor )
    if testgrid != None:   _render_testgrid( width, height, 100 )
    _init()   # initialize the state
    lineprops(); textprops(); # set default line and text props
    return True


def svgresult( noclose=False ):
    # return the svg code that has been built thus far...
    global p_svg
    if p_svg["active"] == False:
        raise AppError( "svgresult(): no active graphic exists yet, see svgbegin()" )
    if noclose == True:  
        result = p_svg["out"]; p_svg["out"] = ""; 
        return result;  # building svg incrementally
    else: 
        p_svg["out"] += "</svg>"; p_svg["active"] = False; 
        return p_svg["out"];  # end of svg


def numspace( axis=None, axmin=None, axmax=None, poslo=None, poshi=None, log=None, reverse=False, allint=False ):    
    # set up a numeric X or Y space (linear or log)
    global p_space
    if p_svg["active"] == False:
        raise AppError( "numspace(): no active graphic exists yet, see svgbegin()" )
    iax = _getiax( axis )
    _spacepos( iax, poslo, poshi )     # set the native coords for this space
    if log == True:
        log = "log"
    if log in ["log", "log+1"]:
        if axmin < 0.0:
             raise AppError( "numspace(): negative axis min not allowed in log space" )
        p_space[iax]["scaletype"] = log
    else:
        p_space[iax]["scaletype"] = "numeric"

    try:
        axmin = float(axmin); axmax = float(axmax)
        if axmin > axmax:
             raise AppError( "numspace(): axis min must always be less than the axis max (see also reverse= )" )
    except:
        raise ValueError( "numspace() is expecting numeric axis min and axis max" )
             

    # compute inc... 
    inc = _getinc( axmin, axmax )
    if inc < 1.0 and allint == True: inc = 1.0

    # with mixed sign data it looks odd if scale inc doesn't land on 0.0 ... so adjust axmin and axmax if necessary
    # ..it works better to do this here rather than in autoscale() .. 
    #   because here, axmin and axmax are post-autoscale (already adjusted)
    if axmin < 0.0 and axmax > 0.0:  
        remainder = math.fmod( axmin, inc )
        if remainder != 0.0: axmin -= (inc+remainder)
        remainder = math.fmod( axmax, inc )
        if remainder != 0.0: axmax += (inc-remainder)

    # save these items for later...
    p_space[iax]["min"] = float(axmin)
    p_space[iax]["max"] = float(axmax)
    p_space[iax]["reverse"] = reverse
    p_space[iax]["inc"] = inc
    try: p_space[iax]["natinc"] = nu( axis, p_space[iax]["inc"] ) - nu( axis, 0.0 )  # size of inc in native units
    except: p_space[iax]["natinc"] = 5      # log space, just assign a small value

    # compute and save scalefactor...
    natrange = nmax(axis) - nmin(axis) 
    if log == "log":   datrange = _log(axmax) - _log(axmin)
    elif log == "log+1":   datrange = _log(axmax+1.0) - _log(axmin+1.0)
    else:   datrange = axmax - axmin  # linear
    p_space[iax]["scalefactor"] =  natrange/datrange

    return True


def catspace( axis=None, catlist=None, poslo=None, poshi=None, reverse=False ):
    # set up a categorical X or Y space 
    global p_space
    if p_svg["active"] == False:
        raise AppError( "catspace(): no active graphic exists yet, see svgbegin()" )
    if catlist == None or len(catlist) < 2:
        raise AppError( "catspace() is expecting catlist to be a valid iterable" )
    iax = _getiax( axis )
    _spacepos( iax, poslo, poshi )   # set the native coords for this space
    p_space[iax]["min"] = 0
    p_space[iax]["max"] = len( catlist )
    p_space[iax]["inc"] = 1
    p_space[iax]["scaletype"] = "categorical"
    p_space[iax]["catlist"] = catlist

    p_space[iax]["reverse"] = False
    if axis == "Y" and reverse == False:   p_space[iax]["reverse"] = True  # Y cats are normally top to bottom
    elif axis == "X" and reverse == True:   p_space[iax]["reverse"] = True
   
    natrange = nmax(axis) - nmin(axis) 
    datrange = dmax(axis) - dmin(axis)
    p_space[iax]["scalefactor"] =  natrange/datrange
    natinc = nu( axis, 1 )  - nu( axis, 0 )  # size of inc in native units (must use int)
    p_space[iax]["natinc"] = natinc

    # build return panel list
    Catpanel = collections.namedtuple( "Catpanel", ["name", "poslo", "poshi"] )
    catlo = poslo
    panellist = []
    for cat in catlist:
        panellist.append( Catpanel( cat, catlo, catlo+natinc ) )
        catlo += natinc

    return panellist



def findrange( testval=None, testfor='both', finish=False, nearest=None, addlpad=None ):
    # find suitable numeric axis min and max.  This function is called repeatedly for each row of data, 
    # allowing programmer flexibility with regard to stacked bars, clustered bars, etc.
    # When finally called with finish=True it returns a dict with members axmin, axmax, and others.
    # On degenerate case (no useful values encountered) it returns None.
    if p_ar["active"] == False:    # initialize
        p_ar["nvals"] = 0; p_ar["nbadvals"] = p_ar["allint"] = True; p_ar["allpos"] = True; p_ar["allneg"] = True;
        p_ar["minval"] = 99999999999999.0; p_ar["maxval"] = -99999999999999.0; 

    if finish == True:
        # compute min and max and return results
        if testval != None: raise AppError( "findrange() cannot have both testval= and finish=True in same call" )

        if p_ar["nvals"] == 0 or p_ar["active"] == False: return None

        if nearest != None:
            try: nearest = float(nearest)
            except: raise ValueError( "if nearest= is specified it must be numeric" )
            if nearest <= 0.0: raise ValueError( "if nearest= is specified it must be a number > 0" )
        if addlpad != None and ( addlpad.isdigit() == False or addlpad <= 0 ): raise ValueError( "if addlpad= is specified it must be an integer > 0" )

        # determine inc for 'nearest' and 'addlpad' purposes...
        inc = nearest
        if inc == None: inc = _getinc( p_ar["minval"], p_ar["maxval"] )
        if inc < 1.0 and p_ar["allint"] == True: inc = 1.0

        # back off the min (and advance the max) to nearest "whole" increment...
        h = math.fmod( p_ar["minval"], inc )
        if h == 0.0:  h = inc # min is on the boundary; add an extra inc
        if p_ar["minval"] < 0.0: axmin = p_ar["minval"] - (inc+h)  # must go the other way when negative  (any action required for max below?)
        else: axmin = p_ar["minval"] - h
    
        h = inc - math.fmod( p_ar["maxval"], inc )
        if h == 0.0:  h = inc # max is on the boundary; add an extra inc
        else: axmax = p_ar["maxval"] + h

        if addlpad != None: axmin -= (inc*addlpad); axmax += (inc*addlpad)
        
        # guard against flukes...
        if p_ar["allpos"] == True and axmin < 0.0:  axmin = 0.0
        if p_ar["allneg"] == True and axmax > 0.0:  axmax = 0.0

        p_ar["active"] = False

        # prepare namedtuple result...
        Autorange = collections.namedtuple( "Autorange", ["axmin", "axmax", "inc", "nvals", "datamin", "datamax", "allint", "allpos", "allneg", "nbadvals"] )
        return Autorange( axmin, axmax, inc, p_ar["nvals"], p_ar["minval"], p_ar["maxval"], p_ar["allint"], p_ar["allpos"], p_ar["allneg"], p_ar["nbadvals"] )

        
    # otherwise we're testing values...
    p_ar["active"] = True
    
    try: fval = float( testval )
    except: p_ar["nbadvals"] += 1; return False

    p_ar["nvals"] += 1
    if testfor != 'max' and fval < p_ar["minval"]:  p_ar["minval"] = fval
    if testfor != 'min' and fval > p_ar["maxval"]:  p_ar["maxval"] = fval
    if fval != math.floor( fval ):  p_ar["allint"] = False
    if fval < 0.0:  p_ar["allpos"] = False
    elif fval > 0.0:  p_ar["allneg"] = False
    return True


def datafieldnames( namelist=None ):
    global p_fieldnames
    p_fieldnames = namelist
    return True


def numinfo( numfield=None, datarows=None, distrib=False, distbinsize=None, accumfield=None, percentiles=False ):
    # Return some characteristics of a numeric data field.
    # Has options for frequency distributions and percentiles for boxplots

    dfindex = getdfindex( numfield, datarows )

    # go thru the data and find min, max, and some other characteristics...
    nvals = nbadvals = 0
    sum = sumsq = 0.0
    allint = allpos = allneg = numsorted = True; 
    minval = 99999999999999.0; maxval = -99999999999999.0; prevval = maxval; 

    for row in datarows:
        if dfindex == -1: strval = row[numfield]   # dict rows
        else: strval = row[dfindex]

        try: fval = float( strval )
        except: nbadvals += 1; continue

        nvals += 1
        if fval < minval:  minval = fval
        if fval > maxval:  maxval = fval
        if fval != math.floor( fval ):  allint = False
        if fval < 0.0:  allpos = False
        elif fval > 0.0:  allneg = False
        if fval < prevval: numsorted = False
        sum += fval
        sumsq += (fval*fval)

    if nvals == 0: return None

    mean = sum / float(nvals)
    sd = math.sqrt( ( sumsq - ((sum*sum)/float(nvals)) ) / float(nvals-1) )
    sem = sd / math.sqrt( float(nvals) )

    dist = None
    binsize = None
    if distrib == True:   # run a freq distribution
        # compute inc and axmax, axmin ... needed for calculating distribution
        inc = _getinc( minval, maxval )
        if inc < 1.0 and allint == True: inc = 1.0
        # back off the min (and advance the max) to nearest "whole" increment...
        h = math.fmod( minval, inc )
        if h == 0.0:  h = inc # min is on the boundary; add an extra inc
        axmin = minval - h
    
        h = inc - math.fmod( maxval, inc )
        if h == 0.0:  h = inc # max is on the boundary; add an extra inc
        axmax = maxval + h
    
        # guard against flukes...
        if allpos == True and axmin < 0.0:  axmin = 0.0
        if allneg == True and axmax > 0.0:  axmax = 0.0

        if accumfield != None: tfindex = getdfindex( accumfield, datarows )

        dist = []
        try:
            if distbinsize == None: binsize = inc/2.0
            elif str(distbinsize)[:4] == "inc/": binsize = inc / math.fabs(float(distbinsize[4:]))
            else: binsize = math.fabs(float(distbinsize))
        except: raise AppError( "numinfo(): error getting distribution binsize" )
        # print "***binsize:", str(binsize)
        halfbin = binsize / 2.0
        curval = axmin
        while curval < axmax:
            dist.append( { "binmid":curval+halfbin, "binlo":curval, "accum":0 } )
            curval += binsize
        for row in datarows:
            if dfindex == -1:  strval = row[numfield]   # dict rows
            else: strval = row[dfindex]
            try: fval = float( strval )
            except: continue

            if accumfield != None:
                if tfindex == -1: tallyval = row[accumfield]  # dict rows
                else: tallyval = row[tfindex]
            else: tallyval = 1

            for drow in dist:
                if fval < (drow["binmid"]+halfbin): drow["accum"] += tallyval; break

    pcl = None
    if percentiles == True:
        if numsorted == False: raise AppError( "numinfo(): pcttiles=True requires data to be sorted in numeric order (low to high)" )
        pcl = _percentiles( datarows, numfield, dfindex )

    # prepare namedtuple result....
    Numinfo = collections.namedtuple( "Numinfo", ["min", "max", "nvals", "nbad", "allint", "numsorted", 
                                          "mean", "sd", "sem", "sum", "distribution", "distbinsize", "percentiles" ] )
    return Numinfo( min, max, nvals, nbadvals, allint, numsorted, mean, sd, sem, sum, dist, binsize, pcl )


def catinfo( catfield=None, datarows=None, nullspacers=False, distrib=False, accumfield=None ):
    # return some characteristics of a categorical data field.
    # Option for frequency distributions 

    dfindex = getdfindex( catfield, datarows )

    catlist = [] 
    prevcat = ""
    for row in datarows:
        if dfindex == -1: strval = row[catfield]  # dict rows
        else:  strval = row[dfindex] 

        if nullspacers == True and ( strval == None or strval == "" ): catlist.append( "" )
 
        if strval == prevcat:  continue   # skip adjacent duplicates quickly
        prevcat = strval

        dup = False
        for cat in catlist:    # see if we have cat already... if so skip it...
            if cat == strval: dup = True; break
        if dup == True: continue
        catlist.append( strval )

    dist = None
    if distrib == True:   # run a freq distribution
        if accumfield != None: tfindex = getdfindex( accumfield, datarows )
        dist = []
        for cat in catlist: dist.append( { "term":cat, "accum":0 } ) 
        try:
            for row in datarows:
                if dfindex == -1:  strval = row[catfield]
                else:  strval = row[dfindex]
                if accumfield != None:
                    if tfindex == -1:   tallyval = row[accumfield]  # dict rows
                    else: tallyval = row[tfindex]                  
                else: tallyval = 1
                bin = catlist.index( strval ) 
                dist[bin]["accum"] += tallyval  
        except: raise AppError( "catinfo(): frequency distribution error" )

    # prepare namedtuple result
    Catfield_info = collections.namedtuple( "Catfield_info", ["catlist", "distribution"] )  
    return Catfield_info( catlist, dist )



def plotdeco( title=None, titlepos="left", xlabel=None, xlabeldist=None, ylabel=None, y2label=None, ylabeldist=None, outline=False, shade=None ):
    global p_text
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "plotdeco(): plot area has not yet been set up yet." )

    if outline != None or shade != None:  rect( nmin('X'), nmin('Y'), nmax('X'), nmax('Y'), fill=shade, outline=outline )

    rothold = p_text["rot"] 
    if title != None: 
        _gtooltip( "begin" )
        if titlepos == "center": txt( (nmin("X")+nmax("X"))/2.0, nmax("Y")+5, title, anchor="middle" )
        elif titlepos == "right": txt( nmax("X"), nmax("Y")+5, title, anchor="end" )
        else: txt( nmin("X"), nmax("Y")+5, title, anchor="start" )
        _gtooltip( "end" )
    if xlabel != None:
        if xlabeldist == None: xlabeldist = 40
        try: xlabeldist = float(xlabeldist)
        except: raise AppError( "plotdeco() is expecting numeric xlabeldist value but got: " + str(xlabeldist) )
        _gtooltip( "begin" ); txt( (nmin("X")+nmax("X"))/2.0, nmin("Y")-xlabeldist, xlabel, anchor="middle" ); _gtooltip( "end" )
    if ylabel != None:
        if ylabeldist == None: ylabeldist = 40
        p_text["rot"] = -90
        try: ylabeldist = float(ylabeldist)
        except: raise AppError( "plotdeco() is expecting numeric ylabeldist value but got: " + str(ylabeldist) )
        _gtooltip( "begin" ); txt( nmin("X")-ylabeldist, (nmin("Y")+nmax("Y"))/2.0, ylabel, anchor="middle" ); _gtooltip( "end" )
    if y2label != None:
        if ylabeldist == None: ylabeldist = 40
        p_text["rot"] = 90
        try: ylabeldist = float(ylabeldist)
        except: raise AppError( "plotdeco() is expecting numeric ylabeldist value but got: " + str(ylabeldist) )
        _gtooltip( "begin" ); txt( nmax("X")+ylabeldist, (nmin("Y")+nmax("Y"))/2.0, y2label, anchor="middle" ); _gtooltip( "end" )
    p_text["rot"] = rothold
    return True
    

def axisrender( axis=None, axisline=True, inc=None, tics=True, stubs=True, grid=False, 
               loc=None, stubformat=None, divideby=None, sep=None, stublist=None ):
    # render an axis scale
    global p_space, p_text
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "axisrender(): plot area has not yet been set up yet." )
    axis = axis.upper()
    iax = _getiax( axis )
    if axis == "X": othax = "Y"
    else: othax = "X"

    a = nmin(axis); b = nmax(axis)
    if loc in ["right", "top"]:   loc = "max"; c = nmax(othax); d = nmin(othax)
    else:    loc = "min"; c = nmin(othax); d = nmax(othax)

    if axisline == True:
        if axis == "X":  lin( a, c, b, c ); lin( b, c, a, c )
        else:  lin( c, a, c, b ); lin( c, b, c, a )

    iscat = False
    if p_space[iax]["scaletype"] == "categorical":  iscat = True

    if inc != None:   # explicit inc... remember it
         p_space[iax]["inc"] = inc
         try: p_space[iax]["natinc"] = nu( axis, p_space[iax]["inc"] ) - nu( axis, 0.0 )  # size of inc in native units
         except: p_space[iax]["natinc"] = 5    # log space, just assign a small value
         
    valstart = dmin(axis); valend = dmax(axis); valinc = p_space[iax]["inc"]

    if tics == None: tics = 0.0

    if tics != 0.0:   # ticend is used in several places below...
        if loc == "max":   ticend = c + tics
        else:   ticend = c - tics

    if tics != 0.0 and stublist == None:
        val = valstart
        while val <= valend:
            if inspace( axis, val ) == False: val += valinc; continue
            if axis == "X":   lin( nx( val ), c, nx( val ), ticend )
            else:   lin( c, ny( val ), ticend, ny( val ) )
            val += valinc


    if grid == True and stublist == None:   # grid for stublist done below...
        gridend = d
        val = valstart
        while val <= valend:
            if inspace( axis, val ) == False:   val += valinc; continue
            if axis == "X":   lin( nx( val ), c, nx( val ), gridend )
            else:   lin( c, ny( val ), gridend, ny( val ) )
            val += valinc

    if stubs == True:
        txtadj = 0.0
        xstubanchor = "middle"

        # we spend a fair amt of effort here fine-tuning rotated stubs... rotate = -90 to 90
        rotnone = False
        if p_text["rot"] == None:      # default to rotate=45 when appropriate....
            rotnone = True            # remember rotate was = None so we can restore afterward
            if axis == "X":      # see if any X axis stubs will be long (> 3 chars)...
                if iscat == True:
                    for cat in p_space[iax]["catlist"]:   
                        if len( cat ) > 3:  p_text["rot"] = 45; break
                elif stublist != None: 
                    for pair in stublist:
                        if len( pair[1] ) > 3:  p_text["rot"] = 45; break
                elif valend >= 1000:   p_text["rot"] = 45

        if p_text["rot"] == None:   rotate = 0
        else:   rotate = p_text["rot"]   
        
        if loc == "max":
            if axis == "X" and rotate > 0 and rotate <= 90:  xstubanchor = "end"; stubstart = c
            elif axis == "X" and rotate < 0 and rotate >= -90:   xstubanchor = "start"; stubstart = c
            else:   stubstart = c + tics + 2
        else:
            if axis == "X":
                if iscat == True or stublist != None:
                    if iscat == True: basis = p_space[iax]["natinc"]
                    elif stublist != None: basis = p_text["height"]   # changed scg 3/11/2016; can't use inc for this
                    if rotate > 0 and rotate <= 90:
                        xstubanchor = "start"; stubstart = c - (tics*2)
                        if rotate <= 60:   txtadj = basis * 0.3
                        else:   txtadj = basis * 0.15
                    elif rotate < 0 and rotate >= -90:
                        xstubanchor = "end"; stubstart = c - (tics*2)
                        if rotate >= -60:   txtadj = basis * -0.3
                        else:   txtadj = basis * -0.15
                else:
                    stubstart = (c - tics) - p_text["height"]
            else:
                stubstart = (c - tics) -2

        if axis == "Y":
            txtadj = p_text["height"] * 0.3   # vertical centering of Y stub texts 


        # render the stubs... 3 scenarios: stublist, categories, or numerics
        _gtooltip( "begin" )

        if stublist != None:   # list of (numval, label) pairs...
            gridend = d
            if stubformat == None: stubformat = "%s"
            try:
                for pair in stublist:
                    val = float( pair[0] )
                    if inspace( axis, val ) == False:  continue
                    outstr = stubformat % pair[1] 
                    if axis == "X":
                        txt( nx(val)-txtadj, stubstart, outstr, anchor=xstubanchor )
                        if tics != 0.0: lin( nx( val ), c, nx( val ), ticend )
                        if grid == True:   lin( nx(val), c, nx(val), gridend )

                    else:
                        txt( stubstart, ny(val)-txtadj, outstr, anchor="end" )
                        if tics != 0.0:    lin( c, ny(val), ticend, ny(val) )
                        if grid == True:   lin( c, ny(val), gridend, ny(val) )
            except: raise AppError( "axisrender(): error rendering " + axis + " axis from stublist" )

        elif p_space[iax]["scaletype"] == "categorical":
            if stubformat == None: stubformat = "%s"
            for cat in p_space[iax]["catlist"]:
                if cat == None or cat == "":  continue   # skip spacers
                outstr = stubformat % cat
                if axis == "X": txt( nx( cat )-txtadj, stubstart, outstr, anchor=xstubanchor )
                else: txt( stubstart, ny( cat )-txtadj, outstr, anchor="end" )

        else:   # numeric
            if stubformat == None: stubformat = "%g"
            if divideby == None: divideby = 1
            try:
                # prevdrawn = nu( axis, valstart ) + p_text["height"]
                prevdrawn = -500.0
                val = valstart - valinc
                while val <= valend:
                    val += valinc
                    if inspace( axis, val ) == False:  continue
                    if sep != None and math.fabs(nu( axis, val ) - prevdrawn) < sep:  continue
                    outstr = stubformat % (val/divideby)
                    if axis == "X":  txt( nx( val )-txtadj, stubstart, outstr, anchor=xstubanchor )
                    else:  txt( stubstart, ny( val )-txtadj, outstr, anchor="end" )
                    prevdrawn = nu( axis, val ) 
            except:
                raise AppError( "axisrender(): error while generating numeric stubs for " + str(axis) + " axis" )

        _gtooltip( "end" )
        if rotnone: p_text["rot"] = None    # restore...
    return True


def bar( x=None, y=None, ybase=None, width=8, fill="#e0ffe0", opacity=1.0, outline=False, xofs=0.0, horiz=False ):
    # render a column bar
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "bar(): no plot area has been set up yet." )
    if x == None or y == None:  return False    # if None encountered just return 
    try: y = float(y)
    except:  raise AppError( "bar() is expecting numeric 'y': " + str(y) )
    if ybase == None: 
        if horiz == False: ybase = dmin( "Y" )
        else: ybase = dmin("X")
    try: ybase = float(ybase)
    except:  raise AppError( "bar() is expecting numeric 'ybase': " + str(ybase) )
    if ybase > y: ytmp = y; y = ybase; ybase = ytmp;  # downward bars
    f = width/2.0
    _gtooltip( "begin" )
    if horiz == True: rect( nx(ybase), (ny(x)-f)+xofs, nx(y), (ny(x)+f)+xofs, fill=fill, opacity=opacity, outline=outline )
    else:             rect( (nx(x)-f)+xofs, ny(ybase), (nx(x)+f)+xofs, ny(y), fill=fill, opacity=opacity, outline=outline )
    _gtooltip( "end" )
    return True


def errorbar( x=None, y=None, erramt=None, ymin=None, ymax=None, tailsize=5, xofs=0.0, horiz=False ):
    # render an error bar.  x is always specified.  Either y and erramt, or ymin and ymax, must be specified.
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "errorbar(): no plot area has been set up yet." )
    if x == None: return False    # coords may include None.. render nothing
    elif (y == None or erramt == None) and (ymin == None or ymax == None):  return False    # coords may include None... render nothing
    if y != None:
        try: ymin = y-erramt; ymax = y + erramt;
        except: raise AppError( "errorbar() is expecting numeric 'y' and 'erramt', got: " + str(y) + " " + str(erramt) )
    try: ymin = float(ymin); ymax = float(ymax)
    except: raise AppError( "errorbar() is expecting either 'y' and 'erramt', or 'ymin' and 'ymax' (all are numeric)" )
    f = tailsize/2.0
    if horiz == True: 
        lin( nx(ymin), ny(x)+ofs, nx(ymax), ny(x)+ofs )
        lin( nx(ymin), (ny(x)+ofs)-f, nx(ymin), (ny(x)+ofs)+f ); lin( nx(ymax), (ny(x)+ofs)-f, nx(ymax), (ny(x)+ofs)+f )
    else:             
        lin( nx(x)+xofs, ny(ymin), nx(x)+xofs, ny(ymax) )
        lin( (nx(x)+xofs)-f, ny(ymin), (nx(x)+xofs)+f, ny(ymin) ); lin( (nx(x)+xofs)-f, ny(ymax), (nx(x)+xofs)+f, ny(ymax) )
    return True


def datapoint( x=None, y=None, diameter=5.0, fill=None, opacity=0.7, outline=None, xofs=0.0, yofs=0.0 ):
    # render a circle data point                                   
    global p_clust
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "datapoint(): plot area has not been set up yet." )
    if x == None or y == None:  return False   # coords may include None... render nothing
    if fill == None and outline == None:  raise AppError( "datapoint() 'fill' or 'outline' must be specified" )
    natx = nx(x)+xofs; naty = ny(y)+yofs
    cofsx = 0.0; cofsy = 0.0;
    if p_clust["mode"] != None:
        if math.fabs( natx - p_clust["prevx"] ) <= p_clust["tol"] and math.fabs( naty - p_clust["prevy"] ) <= p_clust["tol"]:
            p_clust["ndup"] += 1
            ndup = (p_clust["ndup"])/p_clust["dampen"]; ofs = p_clust["offset"]
            if p_clust["mode"] == "surround":
                cofsx = p_clust["xofslist"][ ndup%37 ] * ofs; cofsy = p_clust["yofslist"][ ndup%37 ] * ofs  # 37 list mems
            elif p_clust["mode"] == "rightward":
                cofsx = ndup * ofs * 4.0
            elif p_clust["mode"] == "left+right":
                if ndup % 2 == 0: cofsx = (ndup/2.0) * ofs * 4.0
                else: cofsx = (ndup/2.0) * ofs * -4.0
            elif p_clust["mode"] == "upward":
                cofsy = ndup * ofs * 4.0

    _gtooltip( "begin" )
    circle( natx+cofsx, naty+cofsy, diameter=diameter, fill=fill, opacity=opacity, outline=outline )
    _gtooltip( "end" )
    if p_clust["mode"] != None: p_clust["prevx"] = natx; p_clust["prevy"] = naty;
    return True
        

def clustermode( mode=None, offset=0.8, tolerance=0.0, dampen=1 ):
    # set clustering parameters for datapoint()
    global p_clust
    try: testnum = float(offset) + tolerance + dampen
    except: AppError( "clustermode() is expecting 'offset',  'tolerance', 'dampen' to be numeric" )
    p_clust["mode"] = mode; p_clust["offset"] = float(offset); p_clust["tol"] = float(tolerance); p_clust["dampen"] = int(dampen)
    p_clust["ndup"] = 0; p_clust["prevx"] = 0.0; p_clust["prevy"] = 0.0;
    return True


def label( x=None, y=None, anchor="start", xofs=5.0, yofs=5.0, text="[label]" ):
    # render a piece of text somewhere in data space
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "label(): plot area has not been set up yet." )
    if x == None or y == None:   return False   # coords may include None... render nothing
    natx = nx(x)+xofs; naty = (ny(y)+yofs)-(p_text["height"]*0.3)
    _gtooltip( "begin" )
    txt( natx, naty, text, anchor=anchor )
    _gtooltip( "end" )
    return True


def rectangle( x=None, y=None, width=None, height=None, fill="#e0ffe0", opacity=1.0, outline=False ):
    # render a filled rectangle somewhere in data space   ... 
    # because of elaborate parameter scheme don't try to handle None as done elsewhere
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "rectangle(): plot area has not been set up yet." )
    try:
        if p_space[0]["scaletype"] == "categorical": natwidth = p_space[0]["natinc"]
        elif width == "all": pass
        else:  natwidth = ndist("X", width )
        if p_space[1]["scaletype"] == "categorical": natheight = p_space[1]["natinc"]
        elif height == "all": pass
        else:  natheight = ndist("Y", height )
    except: raise AppError( "rectangle(): invalid parameters" )
    if width  == "all": nx1 = nmin("X"); nx2 = nmax("X")
    else: nx1 = nx(x)-(natwidth/2.0); nx2 = nx(x)+(natwidth/2.0)
    if height == "all": ny1 = nmin("Y"); ny2 = nmax("Y")
    else: ny1 = ny(y)-(natheight/2.0); ny2 = ny(y)+(natheight/2.0)
    _gtooltip( "begin" )
    rect( nx1, ny1, nx2, ny2, fill=fill, opacity=opacity, outline=outline )
    _gtooltip( "end" )
    return True


def curvebegin( stairs=False, fill=None, opacity=1.0, onbadval="bridge", band=False, xofs=None ):
    global p_curve
    p_curve["stairs"] = stairs; p_curve["fill"] = fill; p_curve["opacity"] = opacity;
    p_curve["onbad" ] = onbadval; p_curve["band"] = band; p_curve["x"] = p_curve["y"] = None;
    p_curve["xofs"] = xofs;
    return True

def curvenext( x=None, y=None, y2=None ):
    global p_curve
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "curvenext(): plot area has not been set up yet." )

    if p_curve["fill"] != None and p_curve["band"] == False: y2 = dmin("X")  # fill under curve to ymin (not a band)

    if p_curve["band"] == True and y2 == None: y = None  # no y2 for band, we'll bail below...
    if x == None or y == None:
        if p_curve["onbad"] == "bridge": return False
        elif p_curve["onbad"] == "gap": p_curve["x"] = None; p_curve["y"] = None; return False

    if p_curve["x"] == None or p_curve["y"] == None: firsttime = True
    else:  prevx = p_curve["x"]; prevy = p_curve["y"]; prevy2 = p_curve["y2"]; firsttime = False

    p_curve["x"] = x; p_curve["y"] = y; p_curve["y2"] = y2

    if firsttime == True:  return True    # nothing more to do..

    xofs = p_curve["xofs"]
    if xofs == None: xofs = 0.0
    if p_curve["band"] == True or p_curve["fill"] != None: 
        startingpt = (nx(prevx)+xofs,ny(prevy))
        polygon( ( startingpt, (nx(x)+xofs,ny(y)), (nx(x)+xofs,ny(y2)), (nx(prevx)+xofs,ny(prevy2)), startingpt ), \
                                 fill=p_curve["fill"], opacity=p_curve["opacity"] )
    elif p_curve["stairs"] == True: lin( nx(prevx)+xofs, ny(prevy), nx(x)+xofs, ny(prevy) ); lin( nx(x)+xofs, ny(prevy), nx(x)+xofs, ny(y) ); 
    else: lin( nx(prevx)+xofs, ny(prevy), nx(x)+xofs, ny(y) )

    return True


def line( x1=None, y1=None, x2=None, y2=None ):
    # draw a line in data space, with 'min' and 'max' supported
    if x1 == None or y1 == None or x2 == None or y2 == None: raise AppError( "line() is expecting 4 args x1, y1, x2, y2" )
    if x1 == 'min': x1 = nmin('X')
    elif x1 == 'max': x1 = nmax('X')
    else: x1 = nx( x1 )
    if y1 == 'min': y1 = nmin('Y')
    elif y1 == 'max': y1 = nmax('Y')
    else: y1 = ny( y1 )
    if x2 == 'min': x2 = nmin('X')
    elif x2 == 'max': x2 = nmax('X')
    else: x2 = nx( x2 )
    if y2 == 'min': y2 = nmin('Y')
    elif y2 == 'max': y2 = nmax('Y')
    else: y2 = ny( y2 )
    lin( x1, y1, x2, y2 )
    return True


def arrow( x1=None, y1=None, x2=None, y2=None, headlen=18, headwid=0.3, fill="#888", opacity=1.0 ):
    # draw an arrow in data space with tip at x2, y2.  r is length of arrowhead; w is theta for arrowhead stoutness
    if x1 == None or y1 == None or x2 == None or y2 == None: raise AppError( "arrow() is expecting 4 args x1, y1, x2, y2" )
    line( x1=x1, y1=y1, x2=x2, y2=y2 )
    x1 = nx(x1); y1 = ny(y1); x2 = nx(x2); y2 = ny(y2); # now go to native units
    halfpi = 1.5707963
    vx = x2 - x1; vy = y2 - y1;
    if vx == 0.0 and y2 > y1: th0 = halfpi; # avoid divide by zero 
    elif vx == 0.0 and y1 > y2: th0 = -(halfpi); # avoid divide by zero 
    else: th0 = math.atan( vy / vx );

    th1 = th0 + headwid; th2 = th0 - headwid;
    r = headlen
    if x2 < x1: ax1 = x2+(r*math.cos(th1)); ay1 = y2+(r*math.sin(th1)); ax2 = x2+(r*math.cos(th2)); ay2 = y2+(r*math.sin(th2));
    else:       ax1 = x2-(r*math.cos(th1)); ay1 = y2-(r*math.sin(th1)); ax2 = x2-(r*math.cos(th2)); ay2 = y2-(r*math.sin(th2));
    polygon(  ((x2,y2), (ax1,ay1), (ax2,ay2) ), fill=fill, opacity=opacity, outline=False )
    return True


def pieslice( pctval=None, startval=0.0, fill="#ccc", outline=False, opacity=0.8, placement="right" ):
    # render a piegraph slice.   pctval controls size of slice and is 0.0 to 1.0.
    # startval controls where (radially) the slice "starts" and is also 0.0 to 1.0.

    if pctval == None or pctval <= 0.0: return False
    elif pctval > 1.0: raise AppError( "pieslice() pctval= must be a number between 0.00 and 1.00" )

    if startval == None or startval < 0.0 or startval > 8:  raise AppError( "pieslice() startval= must be a number between 0.00 and 1.00 or so" )

    twopi = 6.28319; 
    halfpi = 1.5707963
    boxw = (nmax('X')-nmin('x')); boxh = (nmax('Y')-nmin('Y'));   
    if boxw < boxh: radius = boxw / 2.0
    else: radius = boxh / 2.0
    if placement == "left": cx = nmin('X') + radius; 
    else: cx = nmax('X') - radius; 
    cy = nmin('Y') + (boxh/2.0)   

    theta = (startval * -1.0 * twopi) + halfpi    # starting theta
    endtheta =  theta - (pctval * twopi)          # ending theta

    pts = []
    # do the two straight edges...
    pts.append( ( cx + (radius * math.cos( endtheta )), cy + (radius * math.sin( endtheta )) ) ); 
    pts.append( (cx, cy) )
    pts.append( ( cx + (radius * math.cos( theta )), cy + (radius * math.sin( theta )) ) )  

    while theta > endtheta:     # now do curved outer edge
        theta -= 0.03 
        pts.append( ( cx + (radius * math.cos( theta )), cy + (radius * math.sin( theta )) ) )

    _gtooltip( "begin" )
    polygon( pts, fill=fill, outline=outline, opacity=opacity )
    _gtooltip( "end" )
    return True


def legenditem( sample=None, label=None, color=None, outline=None, width=None ):
    # post a legend entry, to be rendered later using legendrender()
    global p_leg, p_tt
    if sample == None or label == None: raise AppError( "legenditem() is expecting mandatory parameters 'sample' and 'label'" )
    if width == None:   # make a rough guess of line length
        width = ((label.find("\n")+1) * (p_text["height"] *0.5))+15;  # contains a newline
        if width <= 0: width = (len(label) * (p_text["height"] *0.7)+15);  # usual case...
    if sample in [ "circle", "square" ]:
        if color == None: raise AppError( "legenditem() is expecting 'color' parameter with sample " + str(sample) )
        p_leg.append( { "shape":sample, "color":color, "label":label, "outline":outline, "width":width } )
    elif sample == "line":
        p_leg.append( { "shape":"line", "lineprops":p_line["props"], "label":label, "width":width } )
    else: raise AppError( "legenditem() unrecognized 'sample' parameter: " + str(sample) )
    p_leg[-1]["tooltip"] = p_tt.copy(); p_tt = {}   # take a copy of any current tooltip settings, then clear p_tt
    return True

def legendrender( location=None, xpos=0.0, ypos=0.0, format="down", sampsize=6, linelen=20, title=None ):
    # render the legend using entries posted earlier
    global p_leg, p_tt
    if location == None and (xpos == None or ypos == None): location = "topleft"
    if location == "topleft": xpos += nmin("X")+5; ypos += nmax("Y")-p_text["height"]
    elif location == "bottomleft": xpos += nmin("X")+5; ypos += nmin("Y")+3
    elif location == "topright": xpos += nmax("X")-200; ypos += nmax("Y")-p_text["height"]
    elif location == "bottomright": xpos += nmax("X")-200; ypos += nmin("Y")+3
    try: xloc = float(xpos); ypos = float(ypos);
    except: raise AppError( "legendrender() location= arg error" )
    if len( p_leg ) == 0: raise AppError( "legendrender(): no legenditem() yet" )

    if format == "down":
        sampw = 10
        for row in p_leg:   # see if any line samps (line samps need wider sampw)...
            if row["shape"] == "line": sampw = linelen; break   

    halfln = p_text["height"]*0.3
    x = xpos; y = ypos
    if title != None: nlines = title.count( "\n" ) + 1; txt( x, y, title ); y -= (p_text["height"]*1.1*nlines);
    for row in p_leg:
        if format == "across": # line samps need wider sampw....
            if row["shape"] == "line": sampw = linelen
            else: sampw = sampsize+2
        if len(row["tooltip"]) > 0: p_tt = row["tooltip"].copy(); _gtooltip( "begin" )   # render tooltip assoc. w/ legend row (if any)
        if row["shape"] == "line": lin( x, y+halfln, x+sampw, y+halfln, props=row["lineprops"] )
        elif row["shape"] == "circle": circle( x+(sampw-(sampsize/2.0)), y+halfln, sampsize+1, fill=row["color"], outline=row["outline"] )
        elif row["shape"] == "square": rx = x+(sampw-(sampsize)); rect( rx, y, rx+sampsize, y+(sampsize), fill=row["color"], outline=row["outline"] )
        txt( x+sampw+5, y, row["label"] )
        _gtooltip( "end" ) # end tooltip assoc. w/ legend row (if any)
        nlines = row["label"].count( "\n" ) + 1
        if format == "down": y -= (p_text["height"]*1.1*nlines)
        elif format == "across": x += (row["width"] + sampw)

    p_leg = []
    return True


def tooltip( title=None, url=None, target=None, content=None, bs_popover=False ):
    # capture the necessary info in order to associate a tooltip/xlink with subsequent plot element
    global p_tt
    if title == None and url == None: raise AppError( "tooltip() is expecting 'title' and/or 'url' parameters" )
    if bs_popover == True and ( title == None or content == None ): raise AppError( "tooltip() is expecting 'title' and 'content' parameters for bootstrap popover" )
    p_tt = {}
    p_tt["title"] = title; p_tt["url"] = url; p_tt["target"] = target; p_tt["content"] = content; p_tt["popover"] = bs_popover;
    return True


def groupbegin( id=None, css=None, transform=None ):
    # start an svg <g> group
    p_svg["out"] += "<g"
    if id != None: p_svg["out"] += " id=" + quo(id) 
    if css != None: 
        if ":" in css: p_svg["out"] += " style=" + quo(css) 
        else: p_svg["out"] += " class=" + quo(css)
    if transform != None: p_svg["out"] += " transform=" + quo(css)
    p_svg["out"] += ">\n"
    return True


def groupend():
    # end an svg <g> group  
    p_svg["out"] += "</g>\n"
    return True


### internal utility routines

def flip( yval ): 
    # translate our native Y units (lower-left origin) to svg's (upper-left origin)
    return p_svg["height"] - yval


def quo( val ):
    # return val enclosed in double quotes
    if type( val ) is int or type( val ) is float: return "\"" + str( val ) + "\""
    else: return "\"" + val + "\""


def str2f( val ):
    # return str() of val, with val rounded to 2 decimal places (for use with svg native coordinates)
    return str( "{:.2f}".format( val ).replace(".00", "" ) ) 


def getdfindex( fieldname=None, datarows=None ):
    # determine index (first=0) of the data field of interest, or -1 if data rows are dict
    if datarows == None:  raise AppError( "expecting datarows= " )
    elif len(datarows) < 1:  raise AppError( "datarows= has zero rows" )
    elif len(datarows[0]) < 1: raise AppError( "first row in datarows= is empty" )
    elif len(datarows[0]) == 1: return 0         # one field per row, index has to be 0
    elif type( datarows[0] ) is dict: 
        try: str = datarows[0][fieldname]       # test to see if fieldname is a valid dict member
        except: raise KeyError( "dict member '" + fieldname + "' not found in datarows=" )
        return -1  # data rows are dict and fieldname seems valid
    try:  dfindex = int( fieldname )     # test for an int fieldname eg. "2"
    except:
        if p_fieldnames == None: raise AppError( "datarows= are not dict and data fieldnames have not been defined, see datafields()" )
        try:  dfindex = p_fieldnames.index( fieldname )
        except: raise AppError( "fieldname '" + str(fieldname) + "' not recognized" )
    return dfindex
    

def _getiax( axis ):
    # return 0 for "X" or 1 for "Y"...
    if axis == None: raise AppError( "axis= is required, 'X' or 'Y' expected" )
    elif axis.upper() == "X": return 0
    elif axis.upper() == "Y": return 1
    else: raise AppError( "invalid axis, 'X' or 'Y' expected, but got: " + str(axis) )


def _spacepos( iax, poslo, poshi ):
    # handle the native coordinates for numspace() and catspace() routines, supplying default location if necessary
    global p_svg, p_space
    if iax != 0 and iax != 1: raise AppError( "_spacepos got invalid iax argument" )
    if poslo == None: poslo = 80
    if poshi == None:
        if iax == 0: poshi = p_svg["width"] - 50
        else: poshi = p_svg["height"] - 50
    try: p_space[iax]["poslo"] = float(poslo); p_space[iax]["poshi"] = float(poshi)
    except: raise ValueError( "native unit values must be numeric, got: " + str(poshi) + " " + str(poslo)  )


def _render_testgrid( width, height, inc ):
    # render a test grid showing our pixel units
    lineprops( width=0.5, color="#a0a0a0", dash="5,3" )
    textprops( ptsize=11, color="#d08080", anchor="middle", opacity=0.5 )
    curx = inc
    while curx <= width:
        lin( curx, 0.0, curx, height ); txt( curx, 0.0, str(curx) ); curx += inc

    textprops( ptsize=11, color="#d08080", anchor="start", opacity=0.5 )
    cury = inc
    while cury <= height:
        lin( 0.0, cury, width, cury ); txt( 0.0, cury, str(cury) ); cury += inc

    lineprops( width=0.5, color="#a0a0a0" ); lin( 0, 0, width, 0 ); lin( 0, 0, 0, height ); 
    txt( 0.0, 0.0, "0" )
    textprops( ptsize=11, color="#d08080", anchor="end", opacity=0.5 )
    txt( width-10, height-20, "minplot units" )
    return True


def _getinc( minval, maxval ):
    # find a reasonable inc for the given numeric range... algorthm: Dan Pelleg peldan@yahoo.com
    diff = math.fabs( maxval - minval )
    h = diff / 10.0
    mult = math.pow( 10.0, math.floor( math.log10( h ) ) )
    mantissa = h / mult
    if mantissa < 2.0:   inc = 2.0 * mult
    elif mantissa < 5.0: inc = 5.0 * mult
    else:  inc = 10.0 * mult
    return inc
    

def _log( dataval ):
    # wrapper for math.log that is lenient with dataval=0.0
    if dataval == 0.0:  return 0.0 # allow, tag it to minima
    else:   return math.log( dataval )


def _percentiles( datarows, fieldname, dfindex ):
    # compute 5th, 25th, 50th, 75th, and 95th percentiles on a data field
    pcl = {}
    nums= []
    # first we must make a vector of values, leaving out any non-numerics...
    for row in datarows:
        if dfindex == -1:  strval = row[fieldname]   # access by dict member name
        else: strval = row[dfindex]
        try: fval = float( strval )
        except: continue
        nums.append( fval )
    nvals = len( nums )
    if nvals < 3: raise AppError( "not enough numeric values to compute percentiles" )
    cell = nvals/20; 
    if nvals % 20 != 0: pcl["5th"] = nums[cell]; 
    else: pcl["5th"] = (nums[cell-1] + nums[cell])/2.0
    cell = nvals/4; 
    if nvals % 4 != 0: pcl["25th"] = nums[cell]; 
    else: pcl["25th"] = (nums[cell-1] + nums[cell])/2.0
    cell = nvals/2; 
    if nvals % 2 != 0: pcl["median"] = nums[cell]; 
    else: pcl["median"] = (nums[cell-1] + nums[cell])/2.0
    cell = (nvals-(nvals/4))-1; 
    if nvals % 4 != 0: pcl["75th"] = nums[cell]; 
    else: pcl["75th"] = (nums[cell] + nums[cell+1])/2.0
    cell = (nvals-(nvals/20))-1; 
    if nvals % 20 != 0: pcl["95th"] = nums[cell]; 
    else: pcl["95th"] = (nums[cell] + nums[cell+1])/2.0

    return pcl

#    pctile = (n % 20 ) ? PLV[(n/20) + 1] :  (PLV[n/20] + PLV[(n/20) + 1] ) /2.0 ;  /* 5th */
#    pctile = ( n % 4 ) ?  PLV[(n/4) + 1]  :  (PLV[n/4] + PLV[(n/4) + 1])/2.0 ;      /* 25 */
#    pctile = ( n % 2 ) ?  PLV[(n+1) / 2]  :  (PLV[n/2] + PLV[(n/2)+1])/2.0 ;   /* median/ 50th */
#    pctile = ( n % 4 )  ? PLV[n - (n/4)]  :  (PLV[(n+1) - (n/4)] + PLV[n-(n/4)])/2.0 ;   /* 75 */
#    pctile = ( n % 20 ) ? PLV[n - (n/20)] : (PLV[(n+1) - (n/20)] + PLV[n - (n/20)]) / 2.0 ;  /* 95 */
