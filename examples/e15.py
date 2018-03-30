
import svgdatashapes as s

def example15():                                   # venn diagram example

    s.svgbegin( width=800, height=750 )

    # textstyle = 'font-family: sans-serif; font-weight: bold;' 
    textstyle = 'font-family: sans-serif; ' 
    s.settext( ptsize=16, color="#228", anchor="middle", style=textstyle )

    # ccf   
    s.ellipse( 400, 400, 750, 500, color="#ffdab9", opacity=0.5 )


    s.ellipse( 150, 640, 280, 150, color="#ddf", opacity=0.5 )
    s.txt( 150, 650, "Mouse strain\ncomparison studies" )

    s.ellipse( 400, 675, 300, 150, color="#dfd", opacity=0.5 )
    s.txt( 400, 685, "Population studies\nand QTL archives" )

    s.ellipse( 650, 640, 280, 150, color="#fdf", opacity=0.5 )
    s.tooltip( title="Click here to see a list", url="https://phenome.jax.org/procedures" )
    s._gtooltip( "begin" )
    s.txt( 650, 650, "Phenotyping methods\nand protocols" )
    s._gtooltip( "end" )

    
    s.settext( ptsize=14, style='font-family: sans-serif;' )

    s.ellipse( 190, 140, 220, 110, color="#dff", opacity=0.5 )
    s.tooltip( title="", url="https://phenome.jax.org/centers" )
    s._gtooltip( "begin" )
    s.txt( 190, 140, "Contributing centers\nand investigators" )
    s._gtooltip( "end" )

    s.ellipse( 400, 120, 220, 110, color="#ffa", opacity=0.5 )
    s.tooltip( title="", url="https://phenome.jax.org/about" )
    s._gtooltip( "begin" )
    s.txt( 400, 120, "Helpful user\nresources" )
    s._gtooltip( "end" )

    s.settext( ptsize=15 )
    s.ellipse( 610, 140, 220, 110, color="#cfa", opacity=0.5 )
    s.tooltip( title="", url=None )
    s._gtooltip( "begin" )
    s.txt( 610, 140, "Analysis tools\nand views" )
    s._gtooltip( "end" )



    doword( 280, 520, "Behavior", size=20, rotate=10, url="/procedures?listmode=behavior" )
    doword( 280, 430, "Aging", size=18, rotate=-2, url="/studies/aging" )
    doword( 330, 390, "ITP", size=15, rotate=3, url="/projects/ITP1" )
    doword( 300, 335, "Reproducibility", size=14, rotate=-4, url=None )
    doword( 450, 420, "Environment", size=15, rotate=-6, url=None )
    doword( 460, 350, "Colony mgmt", size=14, rotate=3, url=None )
    doword( 600, 440, "Alcohol", size=15, rotate=-5, url="/interventions" )
    doword( 690, 400, "Diet", size=16, rotate=-3, url="/interventions" )

    doword( 150, 470, "SNPs", size=20, rotate=-8, url="/snp/retrievals" )
    doword( 130, 400, "Genes", size=15, rotate=2, url="/markers/search" )
    doword( 660, 490, "Drug studies", size=16, rotate=6, url="/interventions" )
    doword( 480, 530, "Physiology", size=20, rotate=-4, url="/procedures" )
    doword( 410, 480, "Function", size=15, rotate=0, url=None )
    doword( 550, 380, "Toxicity", size=15, rotate=3, url="/interventions" )
    doword( 680, 350, "Pathogens", size=15, rotate=-9, url="/interventions" )

    # switch to courier
    s.settext( style='font-family: courier;' )

    doword( 140, 320, "C57BL/6J", size=17, color="#777", rotate=-9, url="/strains" )
    doword( 220, 220, "NOD/ShiLtJ", size=14, color="#777", rotate=5, url="/strains" )
    doword( 540, 290, "FVB/NJ", size=16, color="#777", rotate=-2, url="/strains" )
    doword( 650, 300, "KOMP", size=16, color="#777", rotate=0, url="/panels" )
    doword( 620, 230, "BXD", size=18, color="#777", rotate=3, url="/panels" )
    doword( 350, 290, "Collaborative\nCross", size=14, color="#777", rotate=0, url="/panels" )
    doword( 440, 240, "DO", size=16, color="#777", rotate=1, url="/panels" )
    doword( 430, 200, "QTL Archive", size=14, color="#777", rotate=-8, url="/panels" )

    # return the svg.  The caller could then add it in to the rendered HTML.
    return s.svgresult()



def doword( x, y, word, size=14, color="#77c", rotate=0, title="", url=None ):
    # do one word in the middle area
    s.settext( ptsize=size, color=color, anchor="middle", rotate=rotate )
    if url != None:
        s.tooltip( title=title, url="https://phenome.jax.org" + url )
        s._gtooltip( "begin" )

    s.txt( x, y, word )

    if url != None:
        s._gtooltip( "end" )
    return True
