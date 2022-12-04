import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
def get_collection_as_dataframe(database_name:str,database_collection:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {database_collection}")
        df=pd.DataFrame(list(mongo_client[database_name][database_collection].find()))
        logging.info(f"foundn columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column : _id")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")    
        return df
    except Exception as e:
        raise SensorException(e, sys)    