import json
from utils.dataUtils import readRawData as rD
from datetime import datetime as dt

def main():

    config = json.load(open('config/preprocessing.json'))
    todo   = config['TODO']

    if todo['separateColumns']:
        print('Separating Raw Data Columns')
        rD.separateColumns( config['rawData'], config['dataStaging'] )

    if todo['preprocessing']:
        print('Separating Raw Data Columns')
        refDate = dt(*config['refDate'])
        rD.preprocessing( config['dataStaging'], refDate )
    
    

    return

if __name__ == "__main__":
    main()
