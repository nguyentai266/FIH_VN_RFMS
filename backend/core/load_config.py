import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.logger import db_logger


def load_json():
    try:
        
        root_dir = Path(__file__).parent.parent
        print(root_dir)
        config_path=os.path.join(root_dir,'config/config.json')
        config_data=json.load(open(config_path,'r',encoding='utf-8'))
        db_logger.info("[OK] Loaded JSON config MySQL setting....")
        return config_data['mysql_setting']
            
    except FileNotFoundError:
        db_logger.error(f"Config file not found..")
        raise
    except Exception as e:
        db_logger.error(f"Error alarm: {e}", exc_info=True)
        raise
config_json=load_json()