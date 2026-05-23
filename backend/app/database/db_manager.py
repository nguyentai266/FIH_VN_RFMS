import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import aiomysql
from core.config import db_config
from core.logger import db_logger


async def db_connector():
    try:
        connector=await aiomysql.connect(**db_config["mysql_setting"])
        return connector
    except aiomysql.DatabaseError:
        db_logger.error("Cannot connect database, pls check the system.")
    
async def test_db():
    
    # Phải có chữ 'await' ở đây để chờ kết nối thực sự diễn ra
    connector = await db_connector()
    if connector: 
        db_logger.info("Connected MySql database")
        print("Connected", connector)
        connector.close()
        print(connector)
    

if __name__ == ("__main__"):
    asyncio.run(test_db())




