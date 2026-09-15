import pandas as pd
import logging
from pathlib import Path
import yaml
from sklearn.model_selection import train_test_split

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(name)s- %(levelname)s - %(message)s"
)

def load_paths():
    logging.info("Setting all the paths :")
    path = Path(__file__).resolve().parents[2]
    raw_path = path/"data"/"raw"
    raw_path.mkdir(parents = True ,exist_ok =True)
    raw_train_path = raw_path/"train.csv"
    raw_test_path = raw_path/"test.csv"
    params_path =path/"params.yaml"

    logging.info("All the paths are returned :")
    return {
        'params_path' : params_path ,
        'raw_train' : raw_train_path ,
        'raw_test' : raw_test_path
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


def split_data(df, params) -> pd.DataFrame :
    # Splitting here, on the raw data, is what keeps the test set completely
    # unseen by any later fitting step (PowerTransformer / OrdinalEncoder /
    # LabelEncoder in build_features.py). Stratified on the target since
    # Completed/Incomplete is heavily imbalanced (~10:1).
    try :
        logging.info("Splitting raw data into train/test before any feature engineering...")
        train_df, test_df = train_test_split(
            df,
            test_size = params['build_feature']['test_size'],
            random_state = params['build_feature']['random_state'],
            stratify = df['Booking Status']
        )
        logging.info(f"Split completed with train shape {train_df.shape} and test shape {test_df.shape}")

        return train_df, test_df

    except Exception as e :
        logging.error(f"Splitting raw data failed due to : {e}")
        raise e


def save_data(data, data_path ) :
    try :
        logging.info(f"Saving data to {data_path} ... ")
        data.to_csv(data_path, index = False)

    except Exception as e :
        logging.error(f"saving failed due to {e}")
        raise e


def main() :
    try :
        paths = load_paths()
        params_path = paths['params_path']

        params = load_params(params_path)
        url = params['data_ingestion']['url']

        df = load_data(url)
        df = preprocess(df)
        train_df, test_df = split_data(df, params)

        save_data(train_df, paths['raw_train'])
        save_data(test_df, paths['raw_test'])

    except Exception as e :
       logging.error(f"Main failed due to {e}")
       raise e


if __name__ == "__main__" :
    main()
    logging.info("Making data completed : ")
