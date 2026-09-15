import pandas as pd
from pathlib import Path
import logging
from sklearn.preprocessing import OneHotEncoder ,LabelEncoder ,OrdinalEncoder
from sklearn.preprocessing import PowerTransformer
import pickle

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(name)s- %(levelname)s - %(message)s"
)


def load_paths() :
    try :
        logging.info("Loading all the paths : ")
        path = Path(__file__).resolve().parents[2]
        raw_train_path = path/'data'/'raw'/'train.csv'
        raw_test_path = path/'data'/'raw'/'test.csv'
        models_path = path/"models"

        process_path = path/"data"/"processed"
        process_path.mkdir(parents = True , exist_ok = True)

        logging.info("Returning all the paths : ")

        return {
                'models' :models_path ,
                'raw_train' : raw_train_path ,
                'raw_test' : raw_test_path ,
                'processed_path' : process_path
        }

    except Exception as e :
          logging.error(f"loading paths failed due to {e}")
          raise e


def load_data(data_path : str) -> pd.DataFrame :
    try :
        logging.info(f"Loading the data from {data_path} ... ")
        df = pd.read_csv(data_path)
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
        df['Quarter'] = df['Date'].dt.quarter
        df['IsWeekend'] = (df['Date'].dt.dayofweek >= 5).astype(int)
        df['Hour'] = df['Time'].dt.hour
        df['TimeOfDay'] = df['Hour'].apply(time_of_day)
        df['Season'] = df['Month'].apply(get_season)

        df.drop(columns=['Date', 'Time'], inplace=True)

        logging.info("Date and time feature engineering completed.")

        return df

    except Exception as e:
        logging.error(f"Date-Time feature engineering failed due to: {e}")
        raise


def category_encoder(train_df, test_df):
    # Fit ONLY on train — test_df only ever gets .transform()'d, so nothing
    # about the test set's category vocabulary leaks into the encoder.
    try:
        logging.info("Category encoding starting ")

        cate_cols = ['Vehicle Type', 'Payment Method',
                        'TimeOfDay','Season','Quarter','IsWeekend','DayOfWeek','Pickup Location','Drop Location']

        oe = OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1)
        le = LabelEncoder()

        train_df[cate_cols] = oe.fit_transform(train_df[cate_cols])
        test_df[cate_cols] = oe.transform(test_df[cate_cols])
        logging.info(f"Classes of oe are : {oe.categories_}")

        train_df['Booking Status'] = le.fit_transform(train_df['Booking Status'])
        test_df['Booking Status'] = le.transform(test_df['Booking Status'])
        logging.info("Caegory encoder done")

        return train_df, test_df, le, oe

    except Exception as e:
        logging.error(f"Error in category encoding: {e}")
        raise e


def preprocessing_nums(train_df, test_df) :
    # Same idea: PowerTransformer's lambdas / mean / std are estimated from
    # train_df only, then reused to transform test_df.
    try :
        logging.info("Starting nums preprocessing : ")

        nums_cols =  ['Avg VTAT', 'Avg CTAT', 'Booking Value', 'Ride Distance', 'Month',
       'Day', 'Hour']
        trf = PowerTransformer(standardize = True)
        train_df[nums_cols] = trf.fit_transform(train_df[nums_cols])
        test_df[nums_cols] = trf.transform(test_df[nums_cols])
        logging.info("nums preprocessing done ")

        return train_df, test_df, trf

    except Exception as e :
        logging.error("nums preprocessig failed ")
        raise e


def split_xy(train_df, test_df) -> pd.DataFrame :
    try :
        logging.info("Splitting features/target for train and test : ")
        X_train = train_df.drop(['Booking Status'], axis = 1)
        y_train = train_df['Booking Status']
        X_test = test_df.drop(['Booking Status'], axis = 1)
        y_test = test_df['Booking Status']
        logging.info(f"X_train shape {X_train.shape} , X_test shape {X_test.shape}")

        return X_train, X_test, y_train, y_test

    except Exception as e :
        logging.error(f"Splitting features/target failed due to : {e}")
        raise e


def save_data(X_train ,X_test ,y_train ,y_test , processed_path ,le_pkl ,oe, trf,models_path ) :
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

        logging.info("Loading ohe and le ")

        with open(models_path/"trf.pkl" , 'wb') as f :
                    pickle.dump(trf ,f)
        with open(models_path/"oe.pkl" , 'wb') as f :
                    pickle.dump(oe ,f)
        with open(models_path/"le_pkl.pkl" , 'wb') as f :
            pickle.dump(le_pkl ,f)

    except Exception as e :
        logging.error(f"Saving data failed due to : {e}")
        raise e


def main() :
    try :
        logging.info("Starting the process")

        paths = load_paths()
        raw_train_path = paths['raw_train']
        raw_test_path = paths['raw_test']
        process_path = paths['processed_path']
        models_path = paths['models']

        train_df = load_data(raw_train_path)
        test_df = load_data(raw_test_path)

        train_df = date_time_features(train_df)
        test_df = date_time_features(test_df)

        train_df, test_df, trf = preprocessing_nums(train_df, test_df)
        train_df, test_df, Le, oe = category_encoder(train_df, test_df)
        logging.info(f"data is {train_df.columns}")

        X_train, X_test, y_train, y_test = split_xy(train_df, test_df)
        save_data(X_train ,X_test ,y_train ,y_test ,process_path,Le, oe,trf,models_path)

        logging.info("Processing completed : ")
    except Exception as e :
        logging.error(f"Processes failed due to : {e}")
        raise e


if __name__ == "__main__" :
    main()
