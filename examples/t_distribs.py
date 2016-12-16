
import svgdatashapes as s

def test_distribs():

    # This tests the frequency distribution capabilities of numinfo() and catinfo()
    # as well as the percentile computation capability of numinfo().
    
    outstr = ''
    
    dataset1 = ( (1,2), (1,3), (1,4), (1,5), (2,1), (2,1), (3,1), (4,1), (4,1), (4,1), (5,2), (5,2), (6,3), (6,3), (6,3), 
           (7,4), (7,4), (7,4), (8,5), (9,2), (9,2), (9,2), (9,2), (9,2) )
    
    outstr += '\n----\n\nNumeric distribtion result:\n'
    
    result = s.columninfo( column=0, datarows=dataset1, distrib=True, distbinsize=2, accumcol=1 )
    outstr += str(result.distribution)
    
    outstr += '\n----\n\nPercentiles result:\n'
    
    result = s.columninfo( column=0, datarows=dataset1, percentiles=True )
    outstr += str(result.percentiles)
    
    
    # for row in result['distribution']:
    #    print str(row)
    
    outstr += '\n----\n\nCategorical distribution result:\n'
    
    dataset2 = ( [ 'red', 4 ], ['green', 2], ['red', 8 ], ['blue', 1 ], ['green', 7] )
    
    result = s.columninfo( column=0, categorical=True, datarows=dataset2, distrib=True, accumcol=1 )
    
    for row in result.distribution:
        outstr += str(row) + '\n'
    

    outstr += '\n----\n\nnuminfo Using 1D array via vec2d() ...\n'
    vector = [ 5, 2, 7, 11, 15, 21 ]
    datarows = s.vec2d( vector )
    result = s.columninfo( datarows=datarows, column=0, distrib=True, distbinsize=5 )
    outstr += str(result.distribution)

    outstr += '\n----\n\ncatinfo Using 1D array via vec2d() ...\n'
    vector = [ 'red', 'red', 'red', 'blue' ]
    datarows = s.vec2d( vector )
    result = s.columninfo( categorical=True, datarows=datarows, column=0, distrib=True )
    outstr += str(result.distribution)

    
    return outstr
