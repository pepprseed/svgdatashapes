
import minplot as p

def test_distribs():

    # This tests the frequency distribution capabilities of numinfo() and catinfo()
    # as well as the percentile computation capability of numinfo().
    
    outstr = ''
    
    dataset1 = ( (1,2), (1,3), (1,4), (1,5), (2,1), (2,1), (3,1), (4,1), (4,1), (4,1), (5,2), (5,2), (6,3), (6,3), (6,3), 
           (7,4), (7,4), (7,4), (8,5), (9,2), (9,2), (9,2), (9,2), (9,2) )
    
    outstr += '\n----\n\nNumeric distribtion result:\n'
    
    p.datacolumns( [ 'f1', 'f2'] )
    result = p.numinfo( numcol='f1', datarows=dataset1, distrib=True, distbinsize=2, accumcol='f2' )
    outstr += str(result.distribution)
    
    outstr += '\n----\n\nPercentiles result:\n'
    
    result = p.numinfo( numcol='f1', datarows=dataset1, percentiles=True )
    outstr += str(result.percentiles)
    
    
    # for row in result['distribution']:
    #    print str(row)
    
    outstr += '\n----\n\nCategorical distribution result:\n'
    
    dataset2 = ( [ 'red', 4 ], ['green', 2], ['red', 8 ], ['blue', 1 ], ['green', 7] )
    
    p.datacolumns( [ 'f1', 'f2' ] )
    result = p.catinfo( catcol='f1', datarows=dataset2, distrib=True, accumcol='f2' )
    
    for row in result.distribution:
        outstr += str(row) + '\n'
    

    outstr += '\n----\n\nnuminfo Using 1D array via vec2d() ...\n'
    vector = [ 5, 2, 7, 11, 15, 21 ]
    datarows = p.vec2d( vector )
    result = p.numinfo( datarows=datarows, numcol=0, distrib=True, distbinsize=5 )
    outstr += str(result.distribution)

    outstr += '\n----\n\ncatinfo Using 1D array via vec2d() ...\n'
    vector = [ 'red', 'red', 'red', 'blue' ]
    datarows = p.vec2d( vector )
    result = p.catinfo( datarows=datarows, catcol=0, distrib=True )
    outstr += str(result.distribution)

    
    return outstr
