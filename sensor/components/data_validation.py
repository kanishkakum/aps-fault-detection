from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logger
import os,sys
from scipy.stats import ks2_samp
import pandas as pd
import yaml 
from sensor import utils
import numpy as np 

class DataValidation:

    def __init__(self, data_validation_config:config_entity.DataValidationConfig,
    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()

        except:
            raise SensorException(e, sys)  


    def drop_missing_values_column(self,df:pd.DataFrame)->Option[pd.DataFrame]:
        """ 
        This function basically removes those columns which have more than 30% missing values
        """
        try:
            threshold=self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            #selecting column name which contain null
            drop_column_names = null_report[null_report>threshold].index
            self.validation_error["dropped columns"]=drop_column_names
            df.drop(list(drop_column_names),axis=1,inplace=True)

            #return None if no column left
            if len(df.column)==0:
                return None
            return df
                

        except:
            raise SensorException(e, sys)


    def is_required_columns_exist(self,base_df:pd.DataFrame,current_df:pd.DataFrame)->bool:
        try:
            
            base_columns=base_df.columns
            current_columns=current_df.columns

            missing_columns=[]
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error["Missing column"]=missing_columns
                return False
            return True     
        except Exception as e:
            raise SensorException(e, sys)       


    
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame):
        try:
            drift_report=dict()

            base_columns=base_df.columns
            current_columns=current_df.columns
            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]
                #null hypothesis is that both column are drawn from the same distribution
                same_distribution=ks2_samp(base_data,current_data)
                #null hypothesis accepted
                if same_distribution.pvalue>0.05:
                    drift_report[base_column]={
                        "pvalues":same_distribution.pvalue,
                        "same distribution": True
                    }
                # rejecting null hypothesis    
                else:
                    drift_report[base_column]={
                        "pvalues":same_distribution.pvalue,
                        "same_distribution": False
                    }
            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise SensorException(e, sys)        

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            base_df=pd.read_csv(data_validation_config.base_file_path)
            base_df=base_df.replace({"na":np.NAN},inplace=True)
            #base_df has na as null
            base_df=self.drop_missing_values_column(df=base_df)

            train_df=pd.read_csv(data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(data_ingestion_artifact.test_file_path)

            train_df=self.drop_missing_values_column(df=train_df)
            test_df=self.drop_missing_values_column(df=test_df)

            train_df_columns_status= self.is_required_columns_exist(base_df=base_df, current_df=train_df)
            test_df_columns_status= self.is_required_columns_exist(base_df=base_df, current_df=test_df)

            if train_df_columns_status:
                self.data_drift(base_df=base_df, current_df=train_df)
            if test_df_columns_status:
                self.data_drift(base_df=base_df, current_df=test_df)    


        except Exception as e:
            raise SensorException(e, sys)

       