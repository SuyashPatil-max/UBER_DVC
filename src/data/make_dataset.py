import pandas as pd
import logging
from pathlib import Path


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

    logging.info("All the paths are returned :")
    return {
        'data_path' : data_path , 
        'raw_data' : raw_data
    }


def load_data(data_path : str)->pd.DataFrame : 

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
    
        df = load_data(data_path)
        df = preprocess(df) 
        save_data(df , raw_data_path)

    except Exception as e : 
       logging.error(f"Main failed due to {e}")
       raise e 


if __name__ == "__main__" : 
    main() 
    logging.info("Making data completed : ")


    