import json
from utils.dataUtils import readRawData as rD

def main():

    config = json.load(open('config/preprocessing.json'))
    todo   = config['TODO']

    if todo['separateColumns']:
        print('Separating Raw Data Columns')
        rD.separateColumns( config['rawData'], config['dataStaging'] )
    
    

    return

if __name__ == "__main__":
    main()
