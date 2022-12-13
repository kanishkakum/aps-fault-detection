from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logger
import os,sys
from scipy.stats import ks2_samp

class DataValidation:

    def __init__(self, data_validation_config:config_entity.DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config=data_validation_config

        except:
            raise SensorException(e, sys)    


    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:

