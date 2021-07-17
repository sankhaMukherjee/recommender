import csv, os, json

# ----------------------------------------------
# Raw data to Columns
# ----------------------------------------------

def getColumns(fileName):
    
    with open(fileName) as f:
        reader = csv.reader(f)
        columns = reader.__next__()

    return columns

def separateColumns(fileName, dataFolder):

    try:
        columns = getColumns(fileName)
        os.makedirs(dataFolder, exist_ok=True)

        filePointers = []
        for c in columns:
            fileName1 = os.path.join( dataFolder, 'columns', f'{c}.txt' )
            filePointers.append( open(fileName1, 'w') )

        with open(fileName) as f:
            reader = csv.reader(f)
            for i, rows in enumerate(reader):
                if i == 0: continue 

                for colNum, row in enumerate(rows):
                    filePointers[colNum].write(  f'[{i}]\t'  + row.strip() + '\n' )

    except Exception as e:
        print(f'Unable to separate the columns: {e}')
        raise

    finally:
        # Close all the file pointers
        for f in filePointers:
            f.close()

    return

# ----------------------------------------------
# Columnar data to 
# ----------------------------------------------

def preprocessing(stagingFolder):

    processCountry(stagingFolder)

    return

def processCountry(stagingFolder):

    countries = []
    countryMappings = {}

    inpFile = os.path.join(stagingFolder, 'columns', 'country.txt')
    with open( inpFile ) as fInp:
        for l in fInp:
            l = l.strip().split('\t')
            if len(l) == 1:
                continue
            
            countries += [c.strip() for c in l[1].split(',')]

    countries = sorted(list(set(countries)))
    countries = [c for c in countries if c != '']
    
    # Reserve 0 for unknown
    countryMappings        = {c:(i+1) for i,c in enumerate(countries)}
    countryReverseMappings = {(i+1):c for i,c in enumerate(countries)}

    os.makedirs(os.path.join(stagingFolder, 'columnsMeta'), exist_ok=True)

    with open(os.path.join(stagingFolder, 'columnsMeta', 'countryMappings.txt'), 'w') as fOut:
        json.dump( countryMappings, fOut)

    with open(os.path.join(stagingFolder, 'columnsMeta', 'countryReverseMappings.txt'), 'w') as fOut:
        json.dump( countryReverseMappings, fOut)

    outFile = os.path.join(stagingFolder, 'columnsMeta', 'country.txt')
    with open(inpFile) as fInp, open(outFile, 'w') as fOut:
        for l in fInp:
            l = l.strip().split('\t')
            if len(l) == 1:
                result = [0]
            else:
                l      = [l.strip() for l in l[1].split(',')]
                result = sorted(list(set([ countryMappings.get(m, 0) for m in l])))
            result = json.dumps(result)
            fOut.write( result + '\n' )

    return