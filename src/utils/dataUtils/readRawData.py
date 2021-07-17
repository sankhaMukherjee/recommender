import csv, os

def getColumns(fileName:str) -> [str]:
    
    with open(fileName) as f:
        reader = csv.reader(f)
        columns = reader.__next__()

    return columns

def separateColumns(fileName:str, dataFolder:str):

    try:
        columns = getColumns(fileName)
        os.makedirs(dataFolder, exist_ok=True)

        filePointers = []
        for c in columns:
            fileName1 = os.path.join( dataFolder, f'{c}.txt' )
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

