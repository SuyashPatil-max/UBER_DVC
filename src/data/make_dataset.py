
import pandas as pd 
import logging 
from pathlib import Path 
import yaml 


logging.basicConfig(
    level = logging.INFO , 
    format="%(asctime)s - %(name)s- %(levelname)s - %(message)s"
)

def paths(): 
    logging.info("Setting all the paths :")
    path = Path(__file__).resolve().parents[2]
    data_path = path /"data"/"external"
    raw_data = path/"data"/"raw"/"raw_data.csv"
    processed_data = path/"data"/"processed"/"data.csv"

    logging.info("All the paths are returned :")
    return {
        'data_path' : data_path , 
        'raw_data' : raw_data, 
        'processed_data' : processed_data
    }


def load_data(data_path)->pd.DataFrame : 

    try : 
        logging.info("Loading the data ... ")
        df = pd.read_csv(data_path) 
        logging.info(f"Data loaded with shape : {df.shape}")
        return df

    except Exception as e : 
        logging.error(f"Data path is invalid  {data_path}")
        raise e 


def preprocess(df)->pd.DataFrame : 

    try : 
        df = df[df['Booking Status'].isin(['Completed', 'Incomplete'])]
        cols =  ['Cancelled Rides by Customer' ,'Reason for cancelling by Customer',
                     'Cancelled Rides by Driver','Driver Cancellation Reason',
                     'Incomplete Rides','Incomplete Rides Reason','Driver Ratings','Customer Rating']
        
        df = df.drop(cols, axis=1)
        return df 

    except Exception as e : 
        logging.error(f"Processing failed due to {e}")
        raise e 


def save_data(raw_data , process_data) : 
    pass 

def save_data(raw_data , processed_data) : 
    pass
def main() : 
    pass 

if __name__ == "__main__" :
    paths()