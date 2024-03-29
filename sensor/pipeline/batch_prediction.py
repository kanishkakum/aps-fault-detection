from sensor.pipeline.training_pipeline import start_training_pipeline
from sensor.predictor import ModelResolver
from sensor.logger import logging
from sensor.exception import SensorException
import pandas as pd 
from datetime import datetime
from sensor.utils import load_object
import sys,os
import numpy as np 

PREDICTION_DIR="prediction"

def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info("creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading input file: {input_file_path}")
        df=pd.read_csv(input_file_path)
        df.replace({"na":np.NAN},inplace=True)

        logging.info("loading transformer to transform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
        

        input_feature_name = list(transformer.feature_names_in_)
        input_arr = transformer.transform(df[input_feature_name])

        logging.info("loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)

        logging.info("Target encoder to convert numerical data to categorical data")
        target_encoder  = load_object(file_path=model_resolver.get_latest_target_encoder_path())

        cat_prediction = target_encoder.inverse_transform(prediction)

        df["prediction"]=prediction
        df["cat_pred"]=cat_prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path=os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path

    except Exception as e:
        raise SensorException(e, sys)    