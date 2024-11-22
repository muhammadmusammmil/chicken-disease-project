import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from pathlib import Path
from typing import Any
import base64
from box import ConfigBox


#for read yaml file and return
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:

    try:
        print(f"Checking for tile atr: {path_to_yaml}")
        if not os.path.exists(path_to_yaml):
            raise FileNotFoundError(f"{path_to_yaml} does not exist")
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded succesfully")
            return ConfigBox(content)
        
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

#for create directories
@ensure_annotations
def create_directories(path_to_directories:list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at {path}") 


#for save json
@ensure_annotations
def save_json(path:Path, data:dict):
    with open(path, "w")as f:
        json.dump(data, f, indent=4)
        
    logger.info(f"json file saved  at: {path}")


#for load json
def load_json(path:Path)-> ConfigBox:
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


#for save binary file
@ensure_annotations
def save_bin(data: Any, path: Path):
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved at: {path}")


#for load binary data 
def load_bin(path:Path) -> Any:
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

#for get size in kb
def get_size(path:Path) -> str:
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

#for decode Image
def decode_image(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64decode(f.read())
    
    