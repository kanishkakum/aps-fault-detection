from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sklearn.preprocessing import Pipeline 
import os,sys
from typing import Optional
import pandas as pd
import yaml 
from sensor import utils
import numpy as np 
from sensor.config import TARGET_COLUMN

from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler

class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
          data_transformation_config:config_entity.DataTransformationConfig 
          data_ingestion_artifact:artifact_entity.DataIngestionArtifact
        except Exception as e:
          raise SensorException(e, sys)


    @classmethod(f)
    def get_data_transfer_object(cls)->Pipeline:
        try:
            simple_imputer= SimpleImputer(strategy="constant",fill_value=0)
            robust_scaler= RobustScaler()
            pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('RobustScaler',robust_scaler)
                ])
            return pipeline    

        except Exception as e:
            raise SensorException(e, sys)        
    def initiate_data_transformation(self,)->DataTransformationArtifact:
        try:
            #reading train and test df
            train_df= pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            #selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            #transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            #transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            #transforming input features
            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)