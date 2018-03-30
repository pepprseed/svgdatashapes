#
# SVGdatashapes  0.3.6   SVGdatashapes.com    github.com/pepprseed/svgdatashapes
# Copyright 2016-8  Stephen C. Grubb   stevegrubb@gmail.com      MIT License
#

import math
import collections

class AppError(Exception): pass


# globals
p_text = {}
p_line = {}
p_curve = {}
p_leg = []
p_tt = {}
p_dtformat = "%Y-%m-%d"
p_svg = {}; p_svg["active"] = False; p_svg["out"] = ""; p_svg["height"] = 0; p_svg["width"] = 0; 
p_space = [ {}, {} ]; p_space[0]["scalefactor"] = None; p_space[1]["scalefactor"] = None
p_line = {}; p_line["props"] = ""
p_ar = {}; p_ar["active"] = False   # autorange
p_clust = {}
p_clust["mode"] = None; 
p_clust["xofslist"] = (0,0,4, 0,-4,4,-4,-4, 4, 0,-6,0,6, 4,-8,4,8,-4,-8,-4, 8, 0,  0,10,-10, 4,  4,10,-10,-4, -4,10,-10, 8,-8,-8, 8)
p_clust["yofslist"] = (0,4,0,-4, 0,4,-4, 4,-4,-6, 0,6,0,-8, 4,8,4,-8,-4, 8,-4,10,-10, 0,  0,10,-10, 4,  4,10,-10,-4, -4, 8,-8, 8,-8)



### primary user-visible funtions........


def svgbegin( width=None, height=None, fluidsize=False, browser=None, testgrid=None, bgcolor=None, notag=False ):
    # begin a new svg graphic
    global p_svg
    p_svg["out"] = "<svg "
    w3str = "xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\""
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
    p_svg["out"] += " " + w3str + ">\n" 
    if notag == True:  p_svg["out"] = ""
    p_svg["out"] += "<!-- SVG graphic by SVGdatashapes ... SVGdatashapes.com -->\n"  # this must remain intact per Terms of Use
    p_svg["height"] = height; p_svg["width"] = width   # set globals
    _init()   # initialize the graphics state.... always do this here
    if bgcolor != None:  rect( 0, 0, width, height, bgcolor )
    if testgrid != None:   _render_testgrid( width, height, 100 )
    # setline(); settext(); # set default line and text props
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


def xspace( svgrange=None, datarange=None, catlist=None, reverse=False, allint=False, log=False ):
    return _setspace( 'X', svgrange, datarange, catlist, reverse=reverse, allint=allint, log=log )


def yspace( svgrange=None, datarange=None, catlist=None, reverse=False, allint=False, log=False ):
    return _setspace( 'Y', svgrange, datarange, catlist, reverse=reverse, allint=allint, log=log )


def findrange( testval=None, erramt=0.0, finish=False, nearest=None, addlpad=None ):
    # find suitable numeric axis min and max.  This function is called repeatedly for each row of data, 
    # allowing programmer flexibility with regard to stacked bars, clustered bars, etc.
    # When finally called with finish=True it returns a dict with members axmin, axmax, and others.
    # On degenerate case (no useful values encountered) it returns None.
    global p_ar
    if p_ar["active"] == False:    # initialize
        p_ar["nvals"] = 0; p_ar["nbadvals"] = p_ar["allint"] = True; p_ar["allpos"] = True; p_ar["allneg"] = True;
        p_ar["minval"] = 9.99e+99; p_ar["maxval"] = -9.99e+99

    if finish == True:
        # compute min and max and return results
        if testval != None: raise AppError( "findrange() cannot have both testval= and finish=True in same call" )

        if p_ar["nvals"] == 0 or p_ar["active"] == False: return None

        if nearest != None:
            try: nearest = float(nearest)
            except: raise ValueError( "if nearest= is specified it must be numeric" )
            if nearest <= 0.0: raise ValueError( "if nearest= is specified it must be a number > 0" )
        if addlpad != None and ( type(addlpad) is not int or addlpad <= 0 ): raise ValueError( "if addlpad= is specified it must be an integer > 0" )

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
    
    try: fval = float( testval ) + float( erramt )
    except: p_ar["nbadvals"] += 1; return False

    p_ar["nvals"] += 1
    if fval < p_ar["minval"]:  p_ar["minval"] = fval
    if fval > p_ar["maxval"]:  p_ar["maxval"] = fval
    if fval != math.floor( fval ):  p_ar["allint"] = False
    if fval < 0.0:  p_ar["allpos"] = False
    elif fval > 0.0:  p_ar["allneg"] = False
    return True


def uniqcats( datarows=None, column=None, handlenulls="ignore" ):
    # get a unique list of categories from user data set.  Result category list is ordered as encountered.
    # handlenulls can be one of "ignore", "keep", "spacers"
    dfindex = _getdfindex( column, datarows )
    catlist = [] 
    prevcat = ""
    for row in datarows:
        if dfindex == -1: strval = row[column]  # dict rows
        else:  strval = row[dfindex] 

        if strval == None or strval == "": 
            if handlenulls == "keep": pass
            elif handlenulls == "ignore": continue     
            elif handlenulls == "spacers": catlist.append( "" )
 
        if strval == prevcat:  continue   # skip adjacent duplicates quickly
        prevcat = strval

        dup = False
        for cat in catlist:    # see if we have cat already... if so skip it...
            if cat == strval: dup = True; break
        if dup == True: continue
        catlist.append( strval )
    return catlist


def columninfo( datarows=None, column=None, distrib=False, distbinsize=None, accumcol=None, percentiles=False, categorical=False ):
    if datarows == None: raise AppError( "columninfo() expecting mandatory arg 'datarows'" )
    if column == None: raise AppError( "columninfo() expecting mandatory arg 'column'" )
    if categorical == True:
        return _catinfo( datarows, column, distrib=True, accumcol=accumcol )
    else:
        return _numinfo( datarows, column, distrib=distrib, distbinsize=distbinsize, accumcol=accumcol, percentiles=percentiles )


def plotdeco( title=None, outline=False, shade=None, opacity=1.0, xlabel=None, ylabel=None, y2label=None, 
              titlepos="left", xlabeladj=None, ylabeladj=None, y2labeladj=None, rectadj=None ):
    global p_text
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "plotdeco(): plot area has not yet been set up yet." )

    titleadj = 0
    if outline != None or shade != None:  
        mx1 = my1 = mx2 = my2 = 0
        if rectadj != None: 
            if type(rectadj) is int: mx1 = my1 = -rectadj; mx2 = my2 = rectadj
            else:
                try: mx1 = rectadj[0]; my1 = rectadj[1]; mx2 = rectadj[2]; my2 = rectadj[3];
                except: pass
            titleadj=my2
        rect( nmin('X')+mx1, nmin('Y')+my1, nmax('X')+mx2, nmax('Y')+my2, color=shade, opacity=opacity, outline=outline )

    rothold = p_text["rotate"] 
    if title != None: 
        _gtooltip( "begin" )
        if titlepos == "center": txt( (nmin("X")+nmax("X"))/2.0, nmax("Y")+(titleadj+5), title, anchor="middle" )
        elif titlepos == "right": txt( nmax("X"), nmax("Y")+(titleadj+5), title, anchor="end" )
        else: txt( nmin("X"), nmax("Y")+(titleadj+5), title, anchor="start" )
        _gtooltip( "end" )
    if xlabel != None:
        xofs = 0; yofs = -60; xadj = 0; yadj = 0  # was -48
        if xlabeladj != None:
            try: xadj = float(xlabeladj[0]); yadj = float(xlabeladj[1])    # see if specified as (xadj, yadj)
            except: raise AppError( "plotdeco() is expecting xlabeladj as 2 member numeric list, but got: " + str(xlabeladj) )
        _gtooltip( "begin" ); txt( ((nmin("X")+nmax("X"))/2.0)+(xofs+xadj), nmin("Y")+(yofs+yadj), xlabel, anchor="middle" ); _gtooltip( "end" )
    if ylabel != None:
        xofs = -60; yofs = 0; xadj = 0; yadj = 0   # was -40
        if ylabeladj != None:
            try: xadj = float(ylabeladj[0]); yadj = float(ylabeladj[1]);
            except: raise AppError( "plotdeco() is expecting ylabeladj as 2 member numeric list, but got: " + str(ylabeladj) )
        p_text["rotate"] = -90
        _gtooltip( "begin" ); txt( nmin("X")+(xofs+xadj), ((nmin("Y")+nmax("Y"))/2.0)+(yofs+yadj), ylabel, anchor="middle" ); _gtooltip( "end" )
    if y2label != None:
        xofs = 60; yofs = 0; xadj = 0; yadj = 0    # was 40
        if ylabeladj2 != None:
            try: xadj = float(y2labeladj[0]); yadj = float(y2labeladj[1]); 
            except: raise AppError( "plotdeco() is expecting y2labeladj as 2 member numeric list, but got: " + str(y2labeladj) )
        p_text["rotate"] = 90
        _gtooltip( "begin" ); txt( nmax("X")+(xofs+xadj), ((nmin("Y")+nmax("Y"))/2.0)+(yofs+yadj), y2label, anchor="middle" ); _gtooltip( "end" )
    p_text["rotate"] = rothold
    return True


def xaxis( axisline=True, inc=None, tics=None, stubs=True, grid=False, 
           loc=None, stubformat=None, divideby=None, stubcull=None, stublist=None, stubrotate=None ):
    return _axisrender( axis='X', axisline=axisline, inc=inc, tics=tics, stubs=stubs, grid=grid, 
           loc=loc, stubformat=stubformat, divideby=divideby, stubcull=stubcull, stublist=stublist, 
           stubrotate=stubrotate )
    

def yaxis( axisline=True, inc=None, tics=None, stubs=True, grid=False, 
           loc=None, stubformat=None, divideby=None, stubcull=None, stublist=None, stubrotate=None ):
    return _axisrender( axis='Y', axisline=axisline, inc=inc, tics=tics, stubs=stubs, grid=grid, 
           loc=loc, stubformat=stubformat, divideby=divideby, stubcull=stubcull, stublist=stublist, 
           stubrotate=stubrotate )
    

def _axisrender( axis=None, axisline=True, inc=None, tics=None, stubs=True, grid=False, 
               loc=None, stubformat=None, divideby=None, stubcull=None, stublist=None, stubrotate=None ):
    # render an axis scale
    global p_space, p_text
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( axis.lower() + "axis(): plot area has not yet been set up yet." )
    iax = _getiax( axis )
    if axis.upper() == "X": othax = "Y"
    else: othax = "X"

    # get 'loc' and handle loc+ofs and loc-ofs constructs...  (ofs handling added 18 Aug '16)
    if loc == None: loc = "min"
    a = nmin(axis); b = nmax(axis)
    ofs = 0.0
    loc = loc.replace( " ", "" )
    if "+" in loc:
        chunks = loc.split("+")
        if len( chunks ) != 2: raise AppError( "axisrender(): invalid loc= construct: " + str(loc) )
        loc = chunks[0]; ofs = float(chunks[1])
    elif "-" in loc:
        chunks = loc.split("-")
        if len( chunks ) != 2: raise AppError( "axisrender(): invalid loc= construct: " + str(loc) )
        loc = chunks[0]; ofs = float(chunks[1]) * -1.0

    if loc in ["right", "top", "max"]:     loc = "max"; c = nmax(othax)      ; d = nmin(othax) + ofs
    elif loc in ['left', 'bottom', 'min']: loc = "min"; c = nmin(othax) + ofs; d = nmax(othax) 
    else: raise AppError( "axisrender(): invalid loc= construct: "+ str(loc) )

    if stubcull != None and type(stubcull) is not int: raise AppError( "axisrender(): stubcull= must be integer, got: "+ str(stubcull) )
        
    if axisline == True:
        if axis.upper() == "X":  lin( a, c, b, c ); lin( b, c, a, c )
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
        val = valstart-valinc
        prevdrawn = -500.0
        while val <= valend:
            val += valinc
            if inspace( axis, val ) == False: val += valinc; continue
            if stubcull != None and math.fabs(nu( axis, val ) - prevdrawn) < stubcull:  continue
            if axis.upper() == "X":   lin( nx( val ), c, nx( val ), ticend )
            else:   lin( c, ny( val ), ticend, ny( val ) )
            prevdrawn = nu( axis, val ) 


    if grid == True and stublist == None:   # grid for stublist done below...
        gridend = d
        val = valstart-valinc
        prevdrawn = -500.0
        while val <= valend:
            val += valinc
            if inspace( axis, val ) == False:   val += valinc; continue
            if stubcull != None and math.fabs(nu( axis, val ) - prevdrawn) < stubcull:  continue
            if axis.upper() == "X":   lin( nx( val ), c, nx( val ), gridend )
            else:   lin( c, ny( val ), gridend, ny( val ) )
            prevdrawn = nu( axis, val ) 

    if stubs == True:
        txtadj = 0.0
        xstubanchor = "middle"

        # we spend a fair amt of effort here fine-tuning rotated stubs... rotate = -90 to 90
        rot0 = p_text["rotate"]
        if stubrotate == None:      # default to rotate=45 when appropriate....
            if axis.upper() == "X":      # see if any X axis stubs will be long (> 3 chars)...
                if iscat == True:
                    for cat in p_space[iax]["catlist"]:   
                        if len( cat ) > 3:  p_text["rotate"] = 45; break
                elif stublist != None: 
                    for pair in stublist:
                        if len( pair[1] ) > 3:  p_text["rotate"] = 45; break
                elif valend >= 1000:   p_text["rotate"] = 45
        else: p_text["rotate"] = stubrotate

        rotate = p_text["rotate"]   

        if tics > 0: tics_clr = tics   # adjust stub placement by tics, but only if downward/outward  (18 Aug '16)
        else: tics_clr = 0             
        
        if loc == "max":
            if axis.upper() == "X" and rotate > 0 and rotate <= 90:  xstubanchor = "end"; stubstart = c
            elif axis.upper() == "X" and rotate < 0 and rotate >= -90:   xstubanchor = "start"; stubstart = c
            else:   stubstart = c + tics_clr + 2
        else:
            if axis.upper() == "X":
                if iscat == True or stublist != None:
                    if iscat == True: basis = p_space[iax]["natinc"]
                    elif stublist != None: basis = p_text["height"]   
                    if rotate > 0 and rotate <= 90:
                        xstubanchor = "start"; stubstart = c - (tics_clr+5)
                        # if rotate <= 60:   txtadj = basis * 0.3
                        # else:   txtadj = basis * 0.15
                        txtadj = basis * 0.15
                    elif rotate < 0 and rotate >= -90:
                        xstubanchor = "end"; stubstart = c - (tics_clr+5)
                        # if rotate >= -60:   txtadj = basis * -0.3
                        # else:   txtadj = basis * -0.15
                        txtadj = basis * -0.15
                    else: stubstart = (c - tics_clr) - p_text["height"]
                else:
                    stubstart = (c - tics_clr) - p_text["height"]
            else:
                stubstart = (c - tics_clr) -2

        if axis.upper() == "Y":
            txtadj = p_text["height"] * 0.3   # vertical centering of Y stub texts 


        # render the stubs... 3 scenarios: stublist, categories, or numerics
        _gtooltip( "begin" )

        if stublist != None:   # list of (numval, label) pairs...
            gridend = d
            if stubformat == None: stubformat = "%s"
            # try:
            for pair in stublist:
                val = float( pair[0] )
                if inspace( axis, val ) == False:  continue
                outstr = stubformat % pair[1] 
                if axis.upper() == "X":
                    txt( nx(val)-txtadj, stubstart, outstr, anchor=xstubanchor )
                    if tics != 0.0: lin( nx( val ), c, nx( val ), ticend )
                    if grid == True:   lin( nx(val), c, nx(val), gridend )
                else:
                    txt( stubstart, ny(val)-txtadj, outstr, anchor="end" )
                    if tics != 0.0:    lin( c, ny(val), ticend, ny(val) )
                    if grid == True:   lin( c, ny(val), gridend, ny(val) )
            # except: raise AppError( "axisrender(): error rendering " + axis + " axis from stublist" )

        elif p_space[iax]["scaletype"] == "categorical":
            if stubformat == None: stubformat = "%s"
            for cat in p_space[iax]["catlist"]:
                if cat == None or cat == "":  continue   # skip spacers
                outstr = stubformat % cat
                if axis.upper() == "X": txt( nx( cat )-txtadj, stubstart, outstr, anchor=xstubanchor )
                else: txt( stubstart, ny( cat )-txtadj, outstr, anchor="end" )

        else:   # numeric
            if stubformat == None: stubformat = "%g"
            if divideby == None: divideby = 1
            try:
                prevdrawn = -500.0
                val = valstart - valinc
                while val <= valend:
                    val += valinc
                    if inspace( axis, val ) == False:  continue
                    if stubcull != None and math.fabs(nu( axis, val ) - prevdrawn) < stubcull:  continue
                    outstr = stubformat % (val/divideby)
                    if axis.upper() == "X":  txt( nx( val )-txtadj, stubstart, outstr, anchor=xstubanchor )
                    else:  txt( stubstart, ny( val )-txtadj, outstr, anchor="end" )
                    prevdrawn = nu( axis, val ) 
            except:
                raise AppError( "axisrender(): error while generating numeric stubs for " + str(axis) + " axis" )

        _gtooltip( "end" )
        p_text["rotate"] = rot0    # restore...
    return True


def bar( x=None, y=None, ybase=None, width=8, color="#afa", opacity=1.0, outline=False, adjust=0.0, horiz=False ):
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
    if ybase > y: 
        ytmp = y; y = ybase; ybase = ytmp;  # downward bars
    f = width/2.0
    _gtooltip( "begin" )
    if horiz == True: rect( nx(ybase), (ny(x)-f)+adjust, nx(y), (ny(x)+f)+adjust, color=color, opacity=opacity, outline=outline )
    else:             rect( (nx(x)-f)+adjust, ny(ybase), (nx(x)+f)+adjust, ny(y), color=color, opacity=opacity, outline=outline )
    _gtooltip( "end" )
    return True


def errorbar( x=None, y=None, erramt=None, ymin=None, ymax=None, tailsize=5, adjust=0.0, horiz=False ):
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
        lin( nx(ymin), ny(x)+adjust, nx(ymax), ny(x)+adjust )
        lin( nx(ymin), (ny(x)+adjust)-f, nx(ymin), (ny(x)+adjust)+f ); lin( nx(ymax), (ny(x)+adjust)-f, nx(ymax), (ny(x)+adjust)+f )
    else:             
        lin( nx(x)+adjust, ny(ymin), nx(x)+adjust, ny(ymax) )
        lin( (nx(x)+adjust)-f, ny(ymin), (nx(x)+adjust)+f, ny(ymin) ); lin( (nx(x)+adjust)-f, ny(ymax), (nx(x)+adjust)+f, ny(ymax) )
    return True


def datapoint( x=None, y=None, diameter=5.0, color=None, opacity=0.7, outline=None, xadjust=0, yadjust=0 ):
    # render a circle data point                                   
    global p_clust
    if p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "datapoint(): plot area has not been set up yet." )
    if x == None or y == None:  return False   # tolerate None coords... render nothing
    if color == None and outline == None:  raise AppError( "datapoint() 'color' or 'outline' must be specified" )
    natx = nx(x)+xadjust; naty = ny(y)+yadjust;
    cofsx = 0.0; cofsy = 0.0;
    if p_clust["mode"] != None:    # clustering...
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
        else:
            p_clust["prevx"] = natx; p_clust["prevy"] = naty;
            p_clust["ndup"] = 0

    _gtooltip( "begin" )
    circle( natx+cofsx, naty+cofsy, diameter=diameter, color=color, opacity=opacity, outline=outline )
    _gtooltip( "end" )
    return True
        

def setclustering( mode=None, offset=0.8, tolerance=0.0, dampen=1 ):
    # set clustering parameters for datapoint()
    global p_clust
    try: testnum = float(offset) + tolerance + dampen
    except: AppError( "setclustering() is expecting numeric 'offset',  'tolerance', or 'dampen' parameter" )
    p_clust["mode"] = mode; p_clust["offset"] = float(offset); p_clust["tol"] = float(tolerance); p_clust["dampen"] = int(dampen)
    p_clust["ndup"] = 0; p_clust["prevx"] = 0.0; p_clust["prevy"] = 0.0;
    return True


def label( text=None, x=None, y=None, anchor="start", xadjust=0, yadjust=0 ):
    # render a piece of text at data location (x, y) or in svg units at (xadjust, yadjust), or a combination of the two
    if text == None: return False    # render nothing
    if (x != None or y != None) and p_space[0]["scalefactor"] == None or p_space[1]["scalefactor"] == None:
        raise AppError( "label(): data units location (x, y) was given but plot area has not been set up yet." )
    if x == None: natx = xadjust
    else: natx = nu( 'X', x ) + xadjust
    if y == None: naty = yadjust
    else: naty = (nu( 'Y', y ) + yadjust) - (p_text["height"]*0.3)
    _gtooltip( "begin" )
    txt( natx, naty, text, anchor=anchor )
    _gtooltip( "end" )
    return True


def rectangle( x=None, y=None, width=None, height=None, color="#afa", opacity=1.0, outline=False, adjust=None ):
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
    except: raise AppError( "rectangle(): invalid args" )

    mx1 = 0; my1 = 0; mx2 = 0; my2 = 0
    if adjust != None:
        if type(adjust) is int: mx1 = my1 = -adjust; mx2 = my2 = adjust;
        else:
            try: mx1 = adjust[0]; my1 = adjust[1]; mx2 = adjust[2]; my2 = adjust[3];
            except: pass

    if width  == "all": nx1 = nmin("X"); nx2 = nmax("X")
    else: nx1 = nx(x)-(natwidth/2.0); nx2 = nx(x)+(natwidth/2.0)
    if height == "all": ny1 = nmin("Y"); ny2 = nmax("Y")
    else: ny1 = ny(y)-(natheight/2.0); ny2 = ny(y)+(natheight/2.0)
    _gtooltip( "begin" )
    rect( nx1+mx1, ny1+my1, nx2+mx2, ny2+my2, color=color, opacity=opacity, outline=outline )
    _gtooltip( "end" )
    return True


def curvebegin( stairs=False, fill=None, opacity=1.0, onbadval="bridge", band=False, adjust=0.0 ):
    global p_curve
    p_curve["stairs"] = stairs; p_curve["fill"] = fill; p_curve["opacity"] = opacity;
    p_curve["onbad" ] = onbadval; p_curve["band"] = band; p_curve["x"] = p_curve["y"] = None;
    p_curve["adjust"] = adjust;
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

    adjust = p_curve["adjust"]
    if adjust == None: adjust = 0.0
    if p_curve["band"] == True or p_curve["fill"] != None: 
        startingpt = (nx(prevx)+adjust,ny(prevy))
        polygon( ( startingpt, (nx(x)+adjust,ny(y)), (nx(x)+adjust,ny(y2)), (nx(prevx)+adjust,ny(prevy2)), startingpt ), \
                                 color=p_curve["fill"], opacity=p_curve["opacity"] )
    elif p_curve["stairs"] == True: 
        lin( nx(prevx)+adjust, ny(prevy), nx(x)+adjust, ny(prevy) ); lin( nx(x)+adjust, ny(prevy), nx(x)+adjust, ny(y) ); 
    else: lin( nx(prevx)+adjust, ny(prevy), nx(x)+adjust, ny(y) )

    return True


def line( x1=None, y1=None, x2=None, y2=None ):
    # draw a line in data space, with 'min' and 'max' supported
    if x1 == None or y1 == None or x2 == None or y2 == None: raise AppError( "line() is expecting 4 args x1, y1, x2, y2" )
    lin( nu('X',x1), nu('Y',y1), nu('X',x2), nu('Y',y2) )
    return True


def arrow( x1=None, y1=None, x2=None, y2=None, headlen=18, headwid=0.3, tiptype="solid", tipcolor="#888", 
           opacity=1.0, direction=None, magnitude=None ):
    # draw an arrow in data space with tip at x2, y2.  r is length of arrowhead; w is theta for arrowhead stoutness

    if x1 == None or y1 == None: raise AppError( "arrow() is expecting args x1, y1" )
    if (x2 == None or y2 == None) and (direction == None or magnitude == None): 
        raise AppError( "arrow() not all required args were supplied" )

    halfpi = 1.5707963
    # do everyting in svg units...
    x1 = nx(x1); y1 = ny(y1); 
    if x2 != None: x2 = nx(x2); y2 = ny(y2); 
    elif direction != None:
        theta = (direction / 360.0) * (4.0*halfpi)
        x2 = x1 + (magnitude * math.cos(theta)); y2 = y1 + (magnitude * math.sin(theta))

    lin( x1, y1, x2, y2 )
        
    vx = x2 - x1; vy = y2 - y1;
    if vx == 0.0 and y2 > y1: th0 = halfpi; # avoid divide by zero 
    elif vx == 0.0 and y1 > y2: th0 = -(halfpi); # avoid divide by zero 
    else: th0 = math.atan( vy / vx );

    th1 = th0 + headwid; th2 = th0 - headwid;
    r = headlen
    if x2 < x1: ax1 = x2+(r*math.cos(th1)); ay1 = y2+(r*math.sin(th1)); ax2 = x2+(r*math.cos(th2)); ay2 = y2+(r*math.sin(th2));
    else:       ax1 = x2-(r*math.cos(th1)); ay1 = y2-(r*math.sin(th1)); ax2 = x2-(r*math.cos(th2)); ay2 = y2-(r*math.sin(th2));
    if tiptype == "solid": polygon(  ((x2,y2), (ax1,ay1), (ax2,ay2) ), color=tipcolor, opacity=opacity, outline=False )
    elif tiptype[:4] == "line": lin( x2, y2, ax1, ay1 ); lin( x2, y2, ax2, ay2 )
    elif tiptype[:4] == "barb": lin( x2, y2, ax1, ay1 ); 
    return True


def pieslice( pctval=None, startval=0.0, color="#ccc", outline=False, opacity=1.0, placement="right", showpct=False ):
    # render a piegraph slice.   pctval controls size of slice and is 0.0 to 1.0.
    # startval controls where (radially) the slice "starts" and is also 0.0 to 1.0.

    if pctval == None or pctval <= 0.0: return False
    elif pctval > 1.0: raise AppError( "pieslice() pctval= must be a number between 0.00 and 1.00" )

    if startval == None or startval < 0.0 or startval > 8:  raise AppError( "pieslice() startval= out of range" )

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
    txttheta = (theta+endtheta)/2.0               # for placing text percentage, if needed

    pts = []
    # do the two straight edges...
    pts.append( ( cx + (radius * math.cos( endtheta )), cy + (radius * math.sin( endtheta )) ) ); 
    pts.append( (cx, cy) )
    pts.append( ( cx + (radius * math.cos( theta )), cy + (radius * math.sin( theta )) ) )  

    while theta > endtheta:     # now do curved outer edge
        theta -= 0.03 
        pts.append( ( cx + (radius * math.cos( theta )), cy + (radius * math.sin( theta )) ) )

    _gtooltip( "begin" )
    polygon( pts, color=color, outline=outline, opacity=opacity )

    if showpct != False:
        txtrad = radius * 0.7
        if showpct == True: showpct = "%.0f"
        pctstr = showpct % (pctval*100.0)
        tx = cx+(txtrad*math.cos(txttheta))
        ty = cy+(txtrad*math.sin(txttheta))
        txt( tx, ty, pctstr+"%", anchor="middle" )

    _gtooltip( "end" )

    return True


def legenditem( sample='square', label=None, color=None, outline=None, width=None ):
    # post a legend entry, to be rendered later using legendrender()
    global p_leg, p_tt
    if label == None: raise AppError( "legenditem() is expecting mandatory 'label' arg" )
    if width == None:   # make a rough guess of line length
        width = ((label.find("\n")+1) * (p_text["height"] *0.7))+15;  # contains a newline
        if width <= 0: width = (len(label) * (p_text["height"] *0.7)+15);  # usual case...
    if sample in [ "circle", "square" ]:
        if color == None: raise AppError( "legenditem() is expecting 'color' arg with sample " + str(sample) )
        p_leg.append( { "shape":sample, "color":color, "label":label, "outline":outline, "width":width } )
    elif sample == "line":
        p_leg.append( { "shape":"line", "lineprops":p_line["props"], "label":label, "width":width } )
    else: raise AppError( "legenditem() unrecognized 'sample' arg: " + str(sample) )
    p_leg[-1]["tooltip"] = p_tt.copy(); p_tt = {}   # take a copy of any current tooltip settings, then clear p_tt
    return True


def legendrender( location=None, format="down", sampsize=6, linelen=20, title=None, xadjust=0, yadjust=0 ):
    # render the legend using entries posted earlier
    global p_leg, p_tt

    if len( p_leg ) == 0: raise AppError( "legendrender(): no legend entries defined yet, use legenditem() first" )
    if location != None and location not in [ "top", "bottom" ]: 
        raise AppError( "legendrender(): invalid value for 'location' arg, got: " + location )

    if location == None and xadjust == 0 and yadjust == 0: location = "top" 

    if location == "top": xpos = nmin("X")+5+xadjust; ypos = nmax("Y")-p_text["height"]+yadjust
    elif location == "bottom": xpos = nmin("X")+5+xadjust; ypos = nmin("Y")+3+yadjust
    elif location == None: xpos = xadjust; ypos = yadjust

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
        elif row["shape"] == "circle": circle( x+(sampw-(sampsize/2.0)), y+halfln, sampsize+1, color=row["color"], outline=row["outline"] )
        elif row["shape"] == "square": rx = x+(sampw-(sampsize)); rect( rx, y, rx+sampsize, y+(sampsize), color=row["color"], outline=row["outline"] )
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
    if title == None and url == None: raise AppError( "tooltip() is expecting 'title' and/or 'url' args" )
    if bs_popover == True and ( title == None or content == None ): raise AppError( "tooltip() is expecting 'title' and 'content' args for bootstrap popover" )
    p_tt = {}
    p_tt["title"] = title; p_tt["url"] = url; p_tt["target"] = target; p_tt["content"] = content; p_tt["popover"] = bs_popover;
    return True


def groupbegin( id=None, css=None, style=None, transform=None ):
    # start an svg <g> group
    p_svg["out"] += "<g"
    if id != None: p_svg["out"] += " id=" + quo(id) 
    if css != None: p_svg["out"] += " class=" + quo(css)
    if style != None: p_svg["out"] += " style=" + quo(style) 
    if transform != None: p_svg["out"] += " transform=" + quo(transform)
    p_svg["out"] += ">\n"
    return True


def groupend():
    # end an svg <g> group  
    p_svg["out"] += "</g>\n"
    return True


def vec2d( invect ):
    # convert a 1-D array to 2-D representation for compatibility with anything that uses _getdfindex()
    out = []
    for val in invect: 
        out.append( (val,) )
    return out



### user-visible low-level drawing 

def lin( x1, y1, x2, y2, props=None ):
    # draw line from x1,y1 to x2,y2 (native) using current line properties. (props arg is used internally to override)
    global p_svg
    try: testnum = float(x1) + y1 + x2 + y2
    except: raise AppError( "lin() is expecting four numeric values: " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) )
    if props == None:  props = p_line["props"]
    p_svg["out"] += "<polyline points=\"" + str2f(x1) + "," + str2f(_flip(y1)) + " " + \
         str2f(x2) + "," + str2f(_flip(y2)) + "\" " + props + " />\n"
    return True

def txt( x, y, txt, anchor=None ):
    # render text at x,y (native) using current text properties
    global p_svg
    txt = str(txt)
    try: testnum = float(x) + y 
    except: raise AppError( "txt() is expecting two numeric values: " + str(x) + " " + str(y) )
    if p_text["adjust"] != None and len(p_text["adjust"]) == 2: x += p_text["adjust"][0]; y += p_text["adjust"][1]   
    p_svg["out"] += "<text x=" + quo( str2f(x) ) + " y=" + quo( str2f(_flip(y)) ) + " " + p_text["props"]
    if anchor != None:  # allows app to override
        if anchor not in ["start", "middle", "end"]: raise AppError( "txt() is expecting anchor of either 'start', 'middle', or 'end', but got: " + str(anchor) )
        if anchor != "start": p_svg["out"] += " text-anchor=" + quo( anchor ) + " "
    elif p_text["anchor"] != "start": p_svg["out"] += " text-anchor=" + quo( p_text["anchor"] ) + " "   # "start" is svg hard default
    if p_text["rotate"] != 0:
        p_svg["out"] += "transform=\"rotate(" + str(p_text["rotate"]) + " " + str2f(x) + "," + str2f(_flip(y)) + ")\" "
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

def rect( x1, y1, x2, y2, color="#e0e0e0", opacity=1.0, outline=False ):
    # render shaded rectangle with lower-left at x1,y1 and upper right at x2,y2  (native)
    global p_svg
    try: testnum = float(x1) + y1 + x2 + y2
    except: raise AppError( "rect() is expecting four numeric values, but got: " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) )
    p_svg["out"] += "<rect x=" + quo(x1) + " y=" + quo(str2f(_flip(y2))) + " width=" + quo(str2f(x2-x1)) + \
                     " height=" + quo(str2f(y2-y1)) + " "
    if color == None: color = "none"
    _polyparms( color, opacity, outline )
    p_svg["out"] += "/>\n"
    return True

def circle( x, y, diameter, color="#e0e0e0", opacity=1.0, outline=False ):
    # render a circle
    global p_svg
    try: testnum = float(x) + y + diameter
    except: raise AppError( "circle() is expecting x, y, diameter as numeric values, but got " + str(x) + " " + str(y) + " " + str(diameter) )
    p_svg["out"] += "<circle cx=" + quo(str2f(x)) + " cy=" + quo(str2f(_flip(y))) + " r=" + quo(str2f(diameter/2.0)) + " "
    _polyparms( color, opacity, outline )
    p_svg["out"] += "/>\n"
    return True

def ellipse( x, y, width, height, color="#e0e0e0", opacity=1.0, outline=False ):
    global p_svg
    try: testnum = float(x) + y + height + width
    except: raise AppError( "ellipse() is expecting x, y, height, width as numeric values, but got " + str(x) + " " + str(y) + " " + str(height) + " " + str(width) )
    p_svg["out"] += "<ellipse cx=" + quo(str2f(x)) + " cy=" + quo(str2f(_flip(y))) + " rx=" + quo(str2f(width/2.0)) + " ry=" + quo(str2f(height/2.0)) + " "
    _polyparms( color, opacity, outline )
    p_svg["out"] += "/>\n"
    return True

def polygon( ptlist, color="#e0e0e0", opacity=1.0, outline=False ):
    # render a polygon
    global p_svg
    p_svg["out"] += "<polygon points=\""
    for pt in ptlist:
        p_svg["out"] += str2f(pt[0]) + "," + str2f(_flip(pt[1])) + " "
    if color == None: raise AppError( "the color= arg is mandatory for polygon()" )
    p_svg["out"] += "\" "
    _polyparms( color, opacity, outline )
    p_svg["out"] += "/>\n"
    return True

def comment( text ):      # embed a comment in the result SVG...
    global p_svg
    p_svg["out"] += "<!-- " + text + " -->\n"; return True



### user-visible functions for setting text, line, color, symbol properties

def settext( ptsize=None, color=None, opacity=None, anchor=None, rotate=None, adjust=False, css=False, style=False, reset=False ):
    # Set text properties for subsequent text rendering.
    # If reset==True, we'll go to 10pt, black, opacity=1.0, anchor="start", rotate=0, adjust=None, css=None (svg hard defaults)
    # Otherwise, only the specified attributes change, others remain as before.
    # Aside from reset==True, ptsize should always be specified so we can do proper layouts relative to text size (not enforced however).
    # In the svg, css seems to take precedence over the svg-specific font-size and fill statements, so we should be ok there.

    global p_text

    if p_svg["active"] != True: _init()         # in case svgbegin() hasn't been called yet

    if reset == True or ptsize != None:         # ptsize
        if ptsize == None: ptsize = 10
        p_text["ptsize"] = ptsize   
        p_text["height"] = (ptsize/72.0)*100.0
    
    if reset == True or color != None:          # color
        if color == None: color = "#000"
        p_text["color"] = color
    
    if reset == True or opacity != None:        # opacity 
        if opacity == None: opacity = 1.0
        p_text["opacity"] = opacity
    
    if reset == True or anchor != None:         # anchor
        if anchor == None or anchor not in ["start", "middle", "end"]: anchor = "start"
        p_text["anchor"] = anchor
    
    if reset == True or rotate != None:         # rotate 
        if rotate == None: rotate = 0
        if type( rotate ) is int or type( rotate ) is float: 
            p_text["rotate"] = rotate

    if reset == True or adjust != False:        # adjust  (ofsx,ofsy)  ... note False vs. None 
        if adjust == False: adjust = None
        if adjust != None: 
            try: testnum = adjust[0] + adjust[1]
            except: raise AppError( "settext() is expecting adjust as 2 member numeric list, but got: " + str(adjust) )
        p_text["adjust"] = adjust

    if reset == True or css != False:      # css .... note False vs. None; user can specify  css=None
        if css == False: css = None
        p_text["class"] = css

    if reset == True or style != False:      # style .... note False vs. None; user can specify  style=None
        if style == False: style = None
        p_text["style"] = style

    # Now build the props string to be included with each svg text call.  
    # For brevity, omit ptsize when 10, color when black, and opacity when 1.0 ... these are the svg hard defaults 
    p_text["props"] = ""; 
    if p_text["class"] != None: p_text["props"] += "class=" + quo(p_text["class"]) + " "
    if p_text["style"] != None: p_text["props"] += "style=" + quo(p_text["style"]) + " "
    if p_text["ptsize"] != 10: p_text["props"] += "font-size=\"" + str(p_text["ptsize"]) + "pt\" "
    if p_text["color"] not in [ "black", "#000", "#000000" ]: p_text["props"] += "fill=" + quo(p_text["color"]) + " "   
    if p_text["opacity"] != 1.0: p_text["props"] += "fill-opacity=" + quo(p_text["opacity"]) + " "  

    return True


def setline( width=None, color=None, opacity=None, dash=False, css=False, style=False, reset=False ):
    # set line properties for subsequent line rendering...
    # if reset==True we'll go to width=1.0, color=black, opacity=1.0, dash=None, css=None (SVG hard defaults)
    # Otherwise, only the specified attributes change, others remain as before.

    global p_line

    if p_svg["active"] != True: _init()          # in case svgbegin() hasn't been called yet
    
    if reset == True or width != None:           # width
        if width == None: width = 1.0
        p_line["width"] = width

    if reset == True or color != None:           # color
        if color == None: color = "#000"
        p_line["color"] = color

    if reset == True or opacity != None:         # opacity
        if opacity == None: opacity = 1.0
        p_line["opacity"] = opacity

    if reset == True or dash != False:            # dash .... note False vs. None
        if dash == False: dash = None
        p_line["dash"] = dash

    if reset == True or css != False:           # css .... note False vs. None; user can specify  css=None
        if css == False: css = None
        p_line["class"] = css

    if reset == True or style != False:           # style .... note False vs. None; user can specify  style=None
        if style == False: style = None
        p_line["style"] = style

    # Now build a string to be included with each svg line call.  
    # For brevity, omit width when 1.0, color when black, opacity when 1.0, dash when None,  ... these are the svg hard defaults 
    p_line["props"] = ""; 
    if p_line["class"] != None: p_line["props"] += "class=" + quo(p_line["class"]) + " "
    if p_line["style"] != None: p_line["props"] += "style=" + quo(p_line["style"]) + " "
    if p_line["width"] != 1.0: p_line["props"] += "stroke-width=" + quo(p_line["width"]) + " " 
    # if p_line["color"] not in [ "black", "#000", "#000000" ]:   
    p_line["props"] += "stroke=" + quo(p_line["color"]) + " "     # lines always need a stroke attribte
    if p_line["opacity"] != 1.0: p_line["props"] += "stroke-opacity=" + quo(p_line["opacity"]) + " " 
    if p_line["dash"] != None: p_line["props"] += "stroke-dasharray=" + quo(p_line["dash"]) + " " 

    return True




### user-visible low-level dataspace-to-nativespace conversion 

def nx( dataval ):
    # for an x location in data space, return equivalent native coordinate
    return nu( "X", dataval )

def ny( dataval ):
    # for a Y location in data space, return equivalent native coordinate
    return nu( "Y", dataval )

def nu( axis, dataval ):
    # for an x or Y location in data space, return equivalent native coordinate
    # 'min' and 'max' are also supported

    if dataval == 'min': return nmin(axis)
    elif dataval == 'max': return nmax(axis)

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



### internal-only functions 

def _init():
    # initialize the environment / state
    global p_svg, p_space, p_text, p_line, p_clust, p_curve, p_leg, p_tt, p_ar, p_dtformat
    p_space[0]["scalefactor"] = None; p_space[1]["scalefactor"] = None
    if p_svg["active"] != True:  # settext() or setline() might have been called before svgbegin(), if so we don't want to clobber
        p_text["ptsize"] = 10; p_text["color"] = "#000"; p_text["opacity"] = 1.0;  
        p_text["anchor"] = "start"; p_text["rotate"] = 0; p_text["adjust"] = None; p_text["class"] = None; p_text["style"] = None; p_text["props"] = ""; 
        p_text["height"] =  (p_text["ptsize"]/72.0)*100.0
        p_line["width"] = 1.0; p_line["color"] = "#000"; p_line["opacity"] = 1.0; \
        p_line["dash"] = None; p_line["class"] = None; p_line["style"] = None; p_line["props"] = ""; 
    p_clust["mode"] = None
    p_curve["x"] = p_curve["y"] = None; p_curve["adjust"] = None;
    p_leg = []
    p_tt = {} 
    p_ar = {}; p_ar["active"] = False
    p_dtformat = "%Y-%m-%d"
    p_svg["active"] = True
    return True


def _setspace( axis, svgrange, datarange, catlist, reverse=False, allint=False, log=False ):
    # invoke either _numspace() or _catspace() for the given axis
    if axis == 'X': funcname = "xspace()"
    elif axis == 'Y': funcname = "yspace()"
    # set up X space with numeric or categorical scaling
    if p_svg["active"] == False:
        raise AppError( funcname + ": no active graphic begun yet, see svgbegin()" )
    try:
        poslo = svgrange.poslo; poshi = svgrange.poshi;    # could be set by xspace/yspace, when doing multipanel
    except:
        try:
            poslo = int(svgrange[0]); poshi = int(svgrange[1])
        except:
            raise ValueError( funcname + " expecting 'svgrange' as a tuple of two integers eg. (110, 450)" )
    if poslo >= poshi:
        raise AppError( funcname + " got invalid 'svgrange', first int in tuple must be < second int." )
    # now do the work, depending on whether we're doing a numeric vs. categorical space
    if catlist != None:  return _catspace( axis, poslo, poshi, catlist, reverse=reverse )
    else:
        if datarange == None: datarange = (0,100)   # set an arbitrary data range for eg. pie graphs
        return _numspace( axis, poslo, poshi, datarange, reverse=reverse, allint=allint, log=log )


def _numspace( axis, poslo, poshi, datarange, log=None, reverse=False, allint=False ):    
# def numspace( axis=None, axmin=None, axmax=None, poslo=None, poshi=None, log=None, reverse=False, allint=False ):    
    # set up a numeric X or Y space (linear or log)
    global p_space
    iax = _getiax( axis )           # axis already validated
    _spacepos( iax, poslo, poshi )  # set the native coords for this space (poslo,poshi already validated)
    if log == True:
        log = "log"

    try:
        axmin = datarange.axmin; axmax = datarange.axmax   # could be a tuple returned by findrange() or columninfo()
    except:
        try: axmin = float(datarange[0]); axmax = float(datarange[1])  # it could be specified explicitly
        except: 
            raise ValueError( "expecting 'datarange' as a tuple of two numbers eg. (0.0, 100.0)" )
    if axmin > axmax:
             raise AppError( "in datarange tuple, first value must always be less than the 2nd value (see also reverse= )" )

    if allint == False:
        try: allint = datarange.allint    # this could be set by findrange() or columninfo(); also allow explicit override
        except: pass

    if log in ["log", "log+1"]:
        if axmin < 0.0:
             raise AppError( "negative axis min not allowed in log space" )
        p_space[iax]["scaletype"] = log
    else:
        p_space[iax]["scaletype"] = "numeric"

    # compute the tic increment... 
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


def _catspace( axis, poslo, poshi, catlist, reverse=False ):
# def catspace( axis=None, catlist=None, poslo=None, poshi=None, reverse=False ):
    # set up a categorical X or Y space 
    global p_space
    iax = _getiax( axis )            # axis already validated
    _spacepos( iax, poslo, poshi )   # set the native coords for this space, (poslo,poshi already validated)
    try: catlist = catlist.catlist   # could be a tuple as returned by catinfo()
    except: pass
    p_space[iax]["min"] = 0
    p_space[iax]["max"] = len( catlist )
    p_space[iax]["inc"] = 1
    p_space[iax]["scaletype"] = "categorical"
    p_space[iax]["catlist"] = catlist

    p_space[iax]["reverse"] = False
    if axis.upper() == "Y" and reverse == False:   p_space[iax]["reverse"] = True  # Y cats are normally top to bottom
    elif axis.upper() == "X" and reverse == True:   p_space[iax]["reverse"] = True
   
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


def _numinfo( datarows, numcol, distrib=False, distbinsize=None, accumcol=None, percentiles=False ):
    # Return some characteristics of a numeric data column
    # Has options for frequency distributions and percentiles for boxplots

    dfindex = _getdfindex( numcol, datarows )

    # go thru the data and find min, max, and some other characteristics...
    nvals = nbadvals = 0
    sum = sumsq = 0.0
    allint = allpos = allneg = numsorted = True; 
    minval = 9.99e+99; maxval = -9.99e+99; prevval = maxval; 

    for row in datarows:
        if dfindex == -1: strval = row[numcol]   # dict rows
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

    distout = None
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

        if accumcol != None: tfindex = _getdfindex( accumcol, datarows )

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
            if dfindex == -1:  strval = row[numcol]   # dict rows
            else: strval = row[dfindex]
            try: fval = float( strval )
            except: continue

            if accumcol != None:
                if tfindex == -1: tallyval = row[accumcol]  # dict rows
                else: tallyval = row[tfindex]
            else: tallyval = 1

            for drow in dist:
                if fval < (drow["binmid"]+halfbin): drow["accum"] += tallyval; break

        # convert result to array of namedtuples
        distout = []
        Distrow = collections.namedtuple( "Distrow", ["binmid", "binlo", "accum"] )
        for drow in dist:
            distout.append( Distrow( drow["binmid"], drow["binlo"], drow["accum"] ) )

    pcl = None
    if percentiles == True:
        if numsorted == False: raise AppError( "numinfo(): pcttiles=True requires data to be sorted in numeric order (low to high)" )
        pcl = _percentiles( datarows, numcol, dfindex )

    # prepare namedtuple result....
    Numinfo = collections.namedtuple( "Numinfo", ["min", "max", "nvals", "nbad", "allint", "numsorted", 
                                          "mean", "sd", "sem", "sum", "distribution", "distbinsize", "percentiles" ] )
    return Numinfo( min, max, nvals, nbadvals, allint, numsorted, mean, sd, sem, sum, distout, binsize, pcl )


def _catinfo( datarows, catcol, distrib=False, accumcol=None ):
    # return some characteristics of a categorical data column.
    # Option for frequency distributions 

    if datarows == None: raise AppError( "catinfo() expecting mandatory arg 'datarows'" )
    if catcol == None: raise AppError( "catinfo() expecting mandatory arg 'catcol'" )

    catlist = uniqcats( datarows=datarows, column=catcol, handlenulls="keep" )
    dfindex = _getdfindex( catcol, datarows )

    dist = None
    if distrib == True:   # run a freq distribution
        if accumcol != None: tfindex = _getdfindex( accumcol, datarows )
        dist = []
        for cat in catlist: dist.append( { "term":cat, "accum":0 } ) 
        try:
            for row in datarows:
                if dfindex == -1:  strval = row[catcol]
                else:  strval = row[dfindex]
                if accumcol != None:
                    if tfindex == -1:   tallyval = row[accumcol]  # dict rows
                    else: tallyval = row[tfindex]                  
                else: tallyval = 1
                bin = catlist.index( strval ) 
                dist[bin]["accum"] += tallyval  
        except: raise AppError( "catinfo(): frequency distribution error" )

    # prepare namedtuple result
    Catcol_info = collections.namedtuple( "Catcol_info", ["catlist", "distribution"] )  
    return Catcol_info( catlist, dist )



def _flip( yval ): 
    # translate our native Y units (lower-left origin) to svg's (upper-left origin)
    return p_svg["height"] - yval


def quo( val ):
    # return val enclosed in double quotes.  
    return '"' + str(val) + '"'
    # if type( val ) is int or type( val ) is float: return "\"" + str( val ) + "\""
    # else: return "\"" + val + "\""


def str2f( val ):
    # return str() of val, with val rounded to 2 decimal places (for use with svg native coordinates)
    return str( "{:.2f}".format( val ).replace(".00", "" ) ) 


def _getdfindex( colname=None, datarows=None ):
    if type( colname ) is int: return colname

    # determine index (first=0) of the data column of interest, or -1 if data rows are dict
    if datarows == None:  raise AppError( "expecting datarows= " )
    elif len(datarows) < 1:  raise AppError( "datarows= has zero rows" )
    elif len(datarows[0]) < 1: raise AppError( "first row in datarows= is empty" )
    elif len(datarows[0]) == 1: return 0         # one column per row, index has to be 0
    elif type( datarows[0] ) is dict: 
        try: teststr = datarows[0][colname]       # test to see if colname is a valid dict member
        except: raise KeyError( "dict member '" + colname + "' not found in datarows=" )
        return -1  # data rows are dict and colname seems valid
    try:  dfindex = int( colname )     # test for an int colname eg. "2"
    except:
        raise AppError( "unrecognized data column dict element name: " + str(colname) + ", or dataset not a dict" )
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
    if iax != 0 and iax != 1: raise AppError( "invalid axis argument" )
    try: p_space[iax]["poslo"] = float(poslo); p_space[iax]["poshi"] = float(poshi)
    except: raise ValueError( "native unit values must be numeric, got: " + str(poshi) + " " + str(poslo)  )


def _polyparms( color, opacity, outline ):
    # this code shared by several routines above 
    if outline == True: p_svg["out"] += p_line["props"] + " "
    if color != None: p_svg["out"] += "fill=" + quo(color) + " "
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


def _render_testgrid( width, height, inc ):
    # render a test grid showing our pixel units
    setline( width=0.5, color="#a0a0a0", dash="5,3" )
    settext( ptsize=11, color="#d08080", anchor="middle", opacity=0.5 )
    curx = inc
    while curx <= width:
        lin( curx, 0.0, curx, height ); txt( curx, 0.0, str(curx) ); curx += inc

    settext( ptsize=11, color="#d08080", anchor="start", opacity=0.5 )
    cury = inc
    while cury <= height:
        lin( 0.0, cury, width, cury ); txt( 0.0, cury, str(cury) ); cury += inc

    setline( width=0.5, color="#a0a0a0" ); lin( 0, 0, width, 0 ); lin( 0, 0, 0, height ); 
    txt( 0.0, 0.0, "0" )
    settext( ptsize=11, color="#d08080", anchor="end", opacity=0.5 )
    txt( width-10, height-20, "SVG units" )
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


def _percentiles( datarows, colname, dfindex ):
    # compute 5th, 25th, 50th, 75th, and 95th percentiles on a data column

    nums= []
    # first we must make a vector of values, leaving out any non-numerics...
    for row in datarows:
        if dfindex == -1:  strval = row[colname]   # access by dict member name
        else: strval = row[dfindex]
        try: fval = float( strval )
        except: continue
        nums.append( fval )
    nvals = len( nums )
    if nvals < 3: raise AppError( "not enough numeric values to compute percentiles" )
    cell = nvals//20; 
    if nvals % 20 != 0: p5 = nums[cell]; 
    else: p5 = (nums[cell-1] + nums[cell])/2.0

    cell = nvals//4; 
    if nvals % 4 != 0: p25 = nums[cell]; 
    else: p25 = (nums[cell-1] + nums[cell])/2.0

    cell = nvals//2; 
    if nvals % 2 != 0: p50 = nums[cell]; 
    else: p50 = (nums[cell-1] + nums[cell])/2.0

    cell = (nvals-(nvals//4))-1; 
    if nvals % 4 != 0: p75 = nums[cell]; 
    else: p75 = (nums[cell] + nums[cell+1])/2.0

    cell = (nvals-(nvals//20))-1; 
    if nvals % 20 != 0: p95 = nums[cell]; 
    else: p95 = (nums[cell] + nums[cell+1])/2.0

    Percentiles = collections.namedtuple( "Percentiles", ["p5", "p25", "median", "p75", "p95"] )
    return Percentiles( p5, p25, p50, p75, p95 )
