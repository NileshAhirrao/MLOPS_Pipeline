import pandas as pd
import os
from sklearn.model_selection import train_test_split
import logging
import yaml


# Logs directory 
logs_dir='Logs'
os.makedirs(logs_dir,exist_ok=True)

#Logging config
logger=logging.getLogger('data_ingestion')
logger.setLevel('DEBUG')

#Logging on console
console_hand=logging.StreamHandler()
console_hand.setLevel('DEBUG')


#Logs on File using FileHandler
log_file_path=os.path.join(logs_dir,'data_ingestion.log')
file_hand=logging.FileHandler(log_file_path)
file_hand.setLevel('DEBUG')

# setup Formatter in logger
formatter=logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
console_hand.setFormatter(formatter)
file_hand.setFormatter(formatter)

logger.addHandler(console_hand)
logger.addHandler(file_hand)

def load_params(param_path:str)->dict:
    try:
        with open(param_path,'r') as file:
            params=yaml.safe_load(file)
            logger.debug(f'Parameters are retrived successfully :%s',params)
            return params
    except FileNotFoundError as e:
        logger.error(f'File is not found: %s',param_path)
        raise
    except yaml.YAMLError as e:
        logger.error(f'Issue with YAML File : %s',e)
        raise
    except Exception as e:
        logger.error(f'Some unexpected error occured : %s',e)  
        raise      


def load_data(data_url:str)->pd.DataFrame:
    try:
        df=pd.read_csv(data_url)
        logger.debug('data is loaded from %s',data_url)
        return df
    except pd.errors.ParserError as e:
        logger.error('Failed to parse CSV file: %s',e)
        raise
    except Exception as e:
        logger.error('Unexpected error occured while loading data : %s',e)
        raise


def Preprocess_Data(df:pd.DataFrame)->pd.DataFrame:

    try:
        df.drop(columns = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace = True)
        df.rename(columns = {'v1': 'target', 'v2': 'text'}, inplace = True)
        logger.debug('Data Preprocessing is completed')
        return df
    except KeyError as e:
        logger.error('Missing column in Dataaset: %s',e)
        raise
    except Exception as e:
        logger.error('Unexpected error occured while Preprocessing: %s',e)
        raise


def Save_Data(train_data:pd.DataFrame,test_data:pd.DataFrame,data_path:str)->None:
    try:
        raw_data_path=os.path.join(data_path,'raw')
        os.makedirs(raw_data_path,exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path,"train_data.csv"),index=False)
        test_data.to_csv(os.path.join(raw_data_path,"test_data.csv"),index=False)
        logger.debug('Train and test data are stored on Raw location: %s',raw_data_path)
    except Exception as e:
        logger.error('Unexpected error occured during data save: %s',e)
        raise

def main():
    try:
        #test_size=0.2
        params=load_params(param_path='params.yaml')
        test_size=params['data_ingestion']['test_size']

        
        data_path='https://raw.githubusercontent.com/vikashishere/Datasets/main/spam.csv'
        df=load_data(data_url=data_path)

        final_df=Preprocess_Data(df)
        train_data,test_data=train_test_split(final_df,test_size=test_size,random_state=2)
        Save_Data(train_data,test_data,data_path='./data')
        logger.debug('Train/Test file saved on ./data path')

    except Exception as e:
        logger.error('Faile to complete the Data Ingestion Process: %s',e)
        print(f"Error : {e}")


if __name__=='__main__':
    main()














