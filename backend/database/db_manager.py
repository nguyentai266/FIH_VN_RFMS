import asyncio
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import aiomysql

from core.load_config import config_json
from core.logger import db_logger

# Lấy đường dẫn của thư mục gốc (YieldTrackingSupport) và nhét vào não của Python


class DB_manager():
    def __init__(self) -> None:
        config_path="config/config.json"

        self.config=json.load(open(config_path))
        
    
    async def db_connector(self):
        self.connector=await aiomysql.connect(**self.config["mysql_setting"])
        return self.connector
async def test_db():
    mysql = DB_manager()
    # Phải có chữ 'await' ở đây để chờ kết nối thực sự diễn ra
    connector = await mysql.db_connector() 
    db_logger.info("connected DB")
    print("Connected", connector)
    
    # Nhớ đóng kết nối sau khi test xong
    connector.close()

if __name__ == ("__main__"):
    asyncio.run(test_db())




