
import requests
from requests import session
import os
from dotenv import find_dotenv, load_dotenv
import logging #to log intermediate messages

def extract_data(url, file_path, payload):
    '''
    extract data from kaggle
    '''
    #setup session
    with session() as c:
        c.post('https://www.kaggle.com/account/login', data=payload)
        with open(file_path, 'wb') as handle:
            response = c.get(url, stream=True)
            for block in response.iter_content(1024): # to save in chuncks of 1024 bytes.            
                handle.write(block) # to write blocks of bytes.

def main(project_dir):
    '''
    main method
    '''
    logger = logging.getLogger(__name__) #logging instance
    logger.info('getting raw data')
    
    payload = {
    'action': 'login',
    'username': os.environ.get("KAGGLE_USERNAME"),
    'password': os.environ.get("KAGGLE_PASSWORD")
    }

    #urls
    train_url = 'https://www.kaggle.com/c/titanic/download/train.csv'
    test_url = 'https://www.kaggle.com/c/titanic/download/test.csv'

    #files paths
    #to join directories from the root directory without any issue between linux and windows
    raw_data_path = os.path.join(os.path.pardir, 'data', 'raw') 
    train_data_path = os.path.join(raw_data_path, 'train.csv')
    test_data_path = os.path.join(raw_data_path, 'test.csv')

    #extract data
    extract_data(train_url, train_data_path, payload)
    extract_data(test_url, test_data_path, payload)
    logger.info('downloaded raw training and test data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main(project_dir)