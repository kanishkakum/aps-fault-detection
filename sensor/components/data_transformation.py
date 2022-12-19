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

class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
          data_transformation_config:config_entity.DataTransformationConfig,
          data_ingestion_artifact:artifact_entity.DataIngestionArtifact
        except Exception as e:
          raise SensorException(e, sys)


    @classmethod(f)
    def get_data_transfer_object(cls):
        try:
            pass

        except Exception as e:
            raise SensorException(e, sys)        
