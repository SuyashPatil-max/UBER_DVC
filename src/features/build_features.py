import pandas as pd 
import yaml 
from pathlib import Path
import logging
from sklearn.model_selection import train_test_split 

logging.basicConfig(
    level = logging.INFO, 
    format = "%(asctime)s - %(name)s- %(levelname)s - %(message)s"
)


def load_paths() : 
    try : 
        logging.info("Loading all the paths : ")
        path = Path(__file__).resolve().parents[2]
        raw_path = path/'data'/'raw'/'raw_data.csv'
        process_path = path/"data"/"processed"

        process_path.mkdir(parents = True , exist_ok = True)
        processed_path = path/'data'/'processed'

        try : 
            logging.info("Checking the params file paths...")
            params_path = path/'params.yaml'
        
        except Exception as e : 
            logging.error(f"{params_path} deos not exits")
            raise e
        logging.info("Returning all the paths : ")
        
        return {
                'params' : params_path ,
                'raw_data' : raw_path , 
                'processed_path' : processed_path 
        }
    
    except Exception as e : 
          logging.error(f"loading paths failed due to {e}")
          raise e 


def load_params(params_path) : 

    try : 
        logging.info("Loadin params...")
        with open(params_path , 'r') as f : 
            params = yaml.safe_load(f) 
        logging.info("Loading params completed ")
        
        return params 

    except Exception as e : 
        logging.error(f"Loading params failde due to : {e}")
        raise e 


def load_data(raw_path : str) -> pd.DataFrame : 
    try : 
        logging.info("Loading the data... ")
        df = pd.read_csv(raw_path)
        logging.info(f"Data loaded with shape {df.shape}")

        return df 

    except Exception as e : 
        logging.error(f"Data not loaded due to {e}")
        raise e 

def time_of_day(hour):
    try:
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"

    except Exception as e:
        logging.error(f"Time of day extraction failed due to: {e}")
        raise e 


def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"
    

def date_time_features(df):
    try:
        logging.info("Starting date and time feature engineering...")

        df['Date'] = pd.to_datetime(df['Date'])
        df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['DayOfWeek'] = df['Date'].dt.day_name()
        df['DayOfWeek_Num'] = df['Date'].dt.dayofweek
        df['Quarter'] = df['Date'].dt.quarter
        df['IsWeekend'] = (df['Date'].dt.dayofweek >= 5).astype(int)
        df['Hour'] = df['Time'].dt.hour
        df['Minute'] = df['Time'].dt.minute
        df['TimeOfDay'] = df['Hour'].apply(time_of_day)
        df['Season'] = df['Month'].apply(get_season)

        df.drop(columns=['Date', 'Time'], inplace=True)

        logging.info("Date and time feature engineering completed.")

        return df

    except Exception as e:
        logging.error(f"Date-Time feature engineering failed due to: {e}")
        raise


def split_data(params, df) -> pd.DataFrame : 
    try : 
        logging.info("Splinting of data started...")
        X_train, X_test, y_train, y_test = train_test_split(df.drop(['Booking Status'] , axis =1 ), 
                                                            df['Booking Status'] , 
                                                            test_size = params['build_feature']['test_size'],
                                                            random_state = params['build_feature']['random_state'])
        logging.info(f"Spliting data completed with {X_train.shape , X_test.shape}")

        return X_train ,X_test ,y_train,y_test 

    except Exception as e : 
        logging.error(f"spliting data failed due to : {e}")
        raise e 


def save_data(X_train ,X_test ,y_train ,y_test , processed_path) : 
    try : 
        logging.info("Saving the data started...")
        X_train_path = processed_path/"X_train.csv"
        X_test_path = processed_path/"X_test.csv"
        y_train_path = processed_path/"y_train.csv"
        y_test_path = processed_path/"y_test.csv"

        X_train.to_csv(X_train_path , index = False )
        X_test.to_csv(X_test_path , index = False )
        y_train.to_csv(y_train_path , index = False )
        y_test.to_csv(y_test_path , index = False )

    except Exception as e : 
        logging.error(f"Saving data failed due to : {e}")
        raise e 


def main() : 
    try : 
        logging.info("Starting the process")

        paths = load_paths() 
        params_path = paths['params']
        raw_path = paths['raw_data']
        process_path = paths['processed_path']

        params = load_params(params_path)
        df = load_data(raw_path)

        df = date_time_features(df)
        X_train ,X_test ,y_train, y_test = split_data(params , df )
        save_data(X_train ,X_test ,y_train ,y_test ,process_path)

        logging.info("Processing completed : ")
    except Exception as e : 
        logging.error(f"Processes failed due to : {e}")
        raise e 


if __name__ == "__main__" : 
    main() 

        


