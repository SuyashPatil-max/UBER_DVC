import pandas as pd
import logging
from pathlib import Path
import yaml 

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(name)s- %(levelname)s - %(message)s"
)

def load_paths(): 
    logging.info("Setting all the paths :")
    path = Path(__file__).resolve().parents[2]
    data_path = path /"data"/"external"/'ncr_ride_bookings.csv'
    raw_path = path/"data"/"raw"
    raw_path.mkdir(parents = True ,exist_ok =True)
    raw_data = raw_path/"raw_data.csv"
    params_path =path/"params.yaml"

    logging.info("All the paths are returned :")
    return {
        'params_path' : params_path ,
        'data_path' : data_path , 
        'raw_data' : raw_data
    }

def load_params(params_path) : 
    try: 
        logging.info("Loading params file")
        with open(params_path ,'r') as f : 
            params = yaml.safe_load(f)
        logging.info("params loaded")
        return params 

    except Exception as e : 
        logging.error("Error in params loading")
        raise e 

    
def load_data(url: str)->pd.DataFrame : 

    try : 
        logging.info("Loading the data ... ")
        df = pd.read_csv(url) 
        logging.info(f"Data loaded with shape : {df.shape}")
        return df

    except Exception as e : 
        logging.error(f"Data url is invalid  {url}")
        raise e 


def preprocess(df)->pd.DataFrame : 

    try : 
        logging.info("Preprocessing of data starting...")
        df = df[df['Booking Status'].isin(['Completed', 'Incomplete'])]
        cols =  ['Booking ID','Customer ID','Cancelled Rides by Customer' ,'Reason for cancelling by Customer',
                     'Cancelled Rides by Driver','Driver Cancellation Reason',
                     'Incomplete Rides','Incomplete Rides Reason','Driver Ratings','Customer Rating']
        
        df = df.drop(cols, axis=1)
        logging.info(f"Shape of raw data : {df.shape}")
        return df 

    except Exception as e : 
        logging.error(f"Processing failed due to {e}")
        raise e 



def save_data(raw_data, raw_data_path ) : 
    try :
        logging.info("Saving the raw data... ")
        raw_data.to_csv(raw_data_path, index = False)

    except Exception as e : 
        logging.error(f"saving failed due to {e}")
        raise e 


def main() : 
    try : 
        paths = load_paths()
        data_path = paths['data_path']
        raw_data_path = paths['raw_data']
        params_path = paths['params_path']

        params = load_params(params_path)
        url = params['data_ingestion']['url']
    
        df = load_data(url)
        df = preprocess(df) 
        save_data(df , raw_data_path)

    except Exception as e : 
       logging.error(f"Main failed due to {e}")
       raise e 


if __name__ == "__main__" : 
    main() 
    logging.info("Making data completed : ")


    