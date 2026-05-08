import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.logger import db_logger


def load_json(filename):
    try:
        root_dir = Path(__file__).parent.parent
        print(root_dir)
        config_path=os.path.join(root_dir,'config',filename)
        config_data=json.load(open(config_path,'r',encoding='utf-8'))
        db_logger.info(f"Load config file [{filename}] successfuly....")
        return config_data
            
    except FileNotFoundError:
        db_logger.error(f"Error load config, file {filename} not found..")
        raise
    except Exception as e:
        db_logger.error(f"Error alarm: {e}", exc_info=True)
        raise
db_config=load_json('db_config.json')