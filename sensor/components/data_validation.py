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
        except:
            raise e        


    
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
                        "pvalues":same_distribution.pvalue
                        "same_distribution": True
                    }
                # rejecting null hypothesis    
                else:
                    drift_report[base_column]={
                        "pvalues":same_distribution.pvalue
                        "same_distribution": False
                    }    



    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            