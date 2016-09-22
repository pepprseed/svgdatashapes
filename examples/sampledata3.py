# Return sample data based on 'setid' request .... to avoid cluttering up example code modules

def dictrows( setid ):

    plotdata = []
    plotdata.append( {'group':'A', 't1':14.4, 't1sem':2.3, 't2':17.3, 't2sem':4.3, 't3':23.5, 't3sem':6.4, 't4':20.7, 't4sem':5.8 } )
    plotdata.append( {'group':'B', 't1':16.2, 't1sem':3.8, 't2':18.9, 't2sem':3.3, 't3':25.2, 't3sem':11.2,'t4':25.7, 't4sem':6.1 } )
    plotdata.append( {'group':'C', 't1':11.3, 't1sem':3.0, 't2':13.6, 't2sem':5.8, 't3':17.3, 't3sem':3.9, 't4':22.3, 't4sem':6.8 } )
    plotdata.append( {'group':'D', 't1':18.8, 't1sem':5.2, 't2':None,'t2sem':None, 't3':27.8, 't3sem':7.3, 't4':29.7, 't4sem':8.1 } )
    plotdata.append( {'group':'E', 't1':17.6, 't1sem':6.8, 't2':19.2, 't2sem':4.5, 't3':22.7, 't3sem':7.8, 't4':23.8, 't4sem':5.3 } )
    plotdata.append( {'group':'F', 't1':13.9, 't1sem':2.2, 't2':17.6, 't2sem':2.4, 't3':20.1, 't3sem':4.2, 't4':24.8, 't4sem':7.2 } )
    plotdata.append( {'group':'G', 't1':13.2, 't1sem':3.5, 't2':19.8, 't2sem':6.3, 't3':None,'t3sem':None, 't4':26.7, 't4sem':5.8 } )
    plotdata.append( {'group':'H', 't1':14.3, 't1sem':3.0, 't2':13.6, 't2sem':4.8, 't3':16.3, 't3sem':4.9, 't4':20.3, 't4sem':3.8 } )
    
    if setid == 'mixedsign':   # same structure as above but convert to mixed sign 'updown' values 
        for row in plotdata:
            if row["t1"] != None: row["t1"] = row["t1"] - 20; 
            if row["t2"] != None: row["t2"] = row["t2"] - 20; 
            if row["t3"] != None: row["t3"] = row["t3"] - 20; 
            if row["t4"] != None: row["t4"] = row["t4"] - 20; 
        
    return plotdata

