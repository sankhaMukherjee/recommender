import csv, os, json
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as tDel

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

def preprocessing(stagingFolder, refDate):

    categoricalList(stagingFolder, 'country')
    categoricalList(stagingFolder, 'cast')
    categoricalList(stagingFolder, 'director')
    categoricalList(stagingFolder, 'listed_in')

    releaseYear(stagingFolder, refDate)
    dateAdded(stagingFolder, refDate)

    categorical(stagingFolder, 'rating')

    duration(stagingFolder)

    return

def categoricalList(stagingFolder, fileNameStart):

    strings = []

    inpFile = os.path.join(stagingFolder, 'columns', f'{fileNameStart}.txt')
    outFile = os.path.join(stagingFolder, 'columnsMeta', f'{fileNameStart}.txt')

    with open( inpFile ) as fInp:
        for l in fInp:
            l = l.strip().split('\t')
            if len(l) == 1:
                continue
            
            strings += [c.strip() for c in l[1].split(',')]

    strings = [s for s in strings if s != '']
    strings = sorted(list(set(strings)))

    # Reserve 0 for unknown
    stringsMappings        = {c:(i+1) for i,c in enumerate(strings)}
    stringsReverseMappings = {(i+1):c for i,c in enumerate(strings)}

    os.makedirs(os.path.join(stagingFolder, 'columnsMeta'), exist_ok=True)

    with open(os.path.join(stagingFolder, 'columnsMeta', f'{fileNameStart}Mappings.txt'), 'w') as fOut:
        json.dump( stringsMappings, fOut)

    with open(os.path.join(stagingFolder, 'columnsMeta', f'{fileNameStart}ReverseMappings.txt'), 'w') as fOut:
        json.dump( stringsReverseMappings, fOut)

    with open(inpFile) as fInp, open(outFile, 'w') as fOut:
        for l in fInp:
            l = l.strip().split('\t')
            if len(l) == 1:
                result = [0]
            else:
                l      = [l.strip() for l in l[1].split(',')]
                result = sorted(list(set([ stringsMappings.get(m, 0) for m in l])))
            result = json.dumps(result)
            fOut.write( result + '\n' )


    return

def categorical(stagingFolder, fileNameStart):

    strings = []

    inpFile = os.path.join(stagingFolder, 'columns', f'{fileNameStart}.txt')
    outFile = os.path.join(stagingFolder, 'columnsMeta', f'{fileNameStart}.txt')

    with open( inpFile ) as fInp:
        for l in fInp:
            l = l.strip().split('\t')
            if len(l) == 1:
                continue
            
            strings.append(l[1].strip())

    strings = [s for s in strings if s != '']
    strings = sorted(list(set(strings)))

    stringsMappings        = {c:(i+1) for i,c in enumerate(strings)}
    stringsReverseMappings = {(i+1):c for i,c in enumerate(strings)}

    os.makedirs(os.path.join(stagingFolder, 'columnsMeta'), exist_ok=True)

    with open(os.path.join(stagingFolder, 'columnsMeta', f'{fileNameStart}Mappings.txt'), 'w') as fOut:
        json.dump( stringsMappings, fOut)

    with open(os.path.join(stagingFolder, 'columnsMeta', f'{fileNameStart}ReverseMappings.txt'), 'w') as fOut:
        json.dump( stringsReverseMappings, fOut)

    with open(inpFile) as fInp, open(outFile, 'w') as fOut:
        for l in fInp:
            l = l.strip().split('\t')
            if len(l) == 1:
                result = 0
            else:
                result = stringsMappings.get(l[1], 0)
            # result = json.dumps(result)
            fOut.write( f'{result}' + '\n' )


    return 

def releaseYear(stagingFolder, refDate):

    inpFile = os.path.join(stagingFolder, 'columns', f'release_year.txt')
    outFile = os.path.join(stagingFolder, 'columnsMeta', f'release_year.txt')
    with open(inpFile) as f:
        rows = [ l.strip().split('\t')[1] for l in f]
        rows = [ int(r) for r in rows ]
        rows = [ (refDate-dt(r,1,1)).days for r in rows ]
        maxRows, minRows = max(rows), min(rows)
        rows = [ (r-minRows)/( maxRows-minRows ) for r in rows]

    with open(outFile, 'w') as fOut:
        toWrite = '\n'.join([f'{r:.6f}' for r in rows])
        fOut.write( toWrite )

    return

def dateAdded(stagingFolder, refDate):

    inpFile = os.path.join(stagingFolder, 'columns', f'date_added.txt')
    outFile = os.path.join(stagingFolder, 'columnsMeta', f'date_added.txt')
    with open(inpFile) as f:
        rows = [ l.strip().split('\t') for l in f]
        rows = [ (r[1] if len(r)==2 else 'December 15, 2017') for r in rows]
        rows = [ dt.strptime(r, '%B %d, %Y') for r in rows ]
        rows = [ (refDate-r).days for r in rows ]
        maxRows, minRows = max(rows), min(rows)
        rows = [ (r-minRows)/( maxRows-minRows ) for r in rows]

    with open(outFile, 'w') as fOut:
        toWrite = '\n'.join([f'{r:.6f}' for r in rows])
        fOut.write( toWrite )

    return

def duration(stagingFolder):

    inpFile = os.path.join(stagingFolder, 'columns', f'duration.txt')
    outFile = os.path.join(stagingFolder, 'columnsMeta', f'duration.txt')
    with open(inpFile) as f:
        rows = [ l.strip().split('\t')[1] for l in f]
        rows = [ ( (0, float(r.split()[0]) ) if 'Season' in r else (float(r.split()[0]), 0)) for r in rows]
        rows1, rows2 = zip(*rows)
        rows1 = ( np.array(rows1) - min(rows1) )/( max(rows1) - min(rows1) )
        rows2 = ( np.array(rows2) - min(rows2) )/( max(rows2) - min(rows2) )

        rows = list(zip(rows1, rows2))

        # print(rows)
        
    with open(outFile, 'w') as fOut:
        for r in rows:
            fOut.write(json.dumps(r) + '\n')


    return
