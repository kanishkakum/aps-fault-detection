from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logger
import os,sys
from scipy.stats import ks2_samp
import pandas as pd

class DataValidation:

    def __init__(self, data_validation_config:config_entity.DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config=data_validation_config

        except:
            raise SensorException(e, sys)  


    def is_existing_columns_exist(self,)->bool:
        pass

    def drop_missing_values_column(self,df:pd.DataFrame,threshold:float=0.3)->Option[pd.DataFrame]:
        """ 
        This function basically removes those columns which have more than 30% missing values
        """
        try:
            null_report = df.isna().sum()/df.shape[0]
            #selecting column name which contain null
            drop_column_names = null_report[null_report>threshold].index
            df.drop(list(drop_column_names),axis=1,inplace=True)

            #return None if no column left
            if len(df.column)==0:
                return None
            return df
                

        except:
            raise SensorException(e, sys)







    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:

