import logging
import os
from datetime import datetime
import os

#create file name for logging
LOG_FILE_NAME= f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

#create file path
LOG_FILE_PATH = os.path.join(os.getcwd(),"logs")

#create log folder if not exist
os.makedirs(LOG_FILE_PATH, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)