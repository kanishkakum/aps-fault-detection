from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
import os,sys
from xgboost import XGBClassifier
from sensor import utils
from sklearn.    
class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact
                ):

        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys) 

    def train_model(self,x,y):
        try:
            xgb_clf =  XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
         
            raise SensorException(e, sys)

    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            model = self.train_model(x=x_train,y=y_train)

        except Exception as e:
            raise Exception(e,sys)          