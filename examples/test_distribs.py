
import minplot as p

def test_distribs():

    # This tests the frequency distribution capabilities of numinfo() and catinfo()
    # as well as the percentile computation capability of numinfo().
    
    outstr = ""
    
    dataset1 = ( (1,2), (1,3), (1,4), (1,5), (2,1), (2,1), (3,1), (4,1), (4,1), (4,1), (5,2), (5,2), (6,3), (6,3), (6,3), 
           (7,4), (7,4), (7,4), (8,5), (9,2), (9,2), (9,2), (9,2), (9,2) )
    
    outstr += "\n----\n\nNumeric distribtion result:\n"
    
    p.datafieldnames( ( "f1",  "f2") )
    result = p.numinfo( numfield="f1", datarows=dataset1, distrib=True, distbinsize=1, accumfield="f2" )
    outstr += str(result.distribution)
    
    outstr += "\n----\n\nPercentiles result:\n"
    
    result = p.numinfo( numfield="f1", datarows=dataset1, percentiles=True )
    outstr += str(result.percentiles)
    
    
    # for row in result["distribution"]:
    #    print str(row)
    
    outstr += "\n----\n\nCategorical distribution result:\n"
    
    dataset2 = ( [ "red", 4 ], ["green", 2], ["red", 8 ], ["blue", 1 ], ["green", 7] )
    
    p.datafieldnames( ( "f1", "f2" ) )
    result = p.catinfo( catfield="f1", datarows=dataset2, distrib=True, accumfield="f2" )
    
    for row in result.distribution:
        outstr += str(row) + "\n"
    
    
    return outstr
