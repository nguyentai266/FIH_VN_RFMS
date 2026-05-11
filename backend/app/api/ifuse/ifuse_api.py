import asyncio
import json
from pathlib import Path

import httpx
import pandas as pd
import urllib3
from core.logger import logger, worker_logger
from fastapi import HTTPException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = httpx.AsyncClient(verify=False)
#session.options()

class IfuseApi():
    def __init__(self) -> None:
        current_path=Path(__file__).parent
        self.template=json.load(open(current_path/"ifuse_template.json",'r'))
        self.offline = True
    async def login(self, user, password):
        url = self.template['login']['url']
        payload = self.template['login']['payload']
        payload['u'] = user
        payload['p'] = password
        
        try:
            response = await session.post(url, json=payload)
            
            if response.status_code == 200:
                
                if '"success":true' in response.text: 
                    res_json = response.json()
                    if res_json.get('success') == True: 
                        worker_logger.info(f"Login OK, Username:{user}")
                        logger.info(f"Login OK, Username:{user}")
                        return {
                            "success": True, 
                            "message": "Login OK",
                            "cookies": session.cookies 
                        }
                else:
                    worker_logger.info(f"Login Error, Username: {user}, Message: {response.text}")
                    logger.info(f"Login Error, Username: {user}, Message: {response.text}")
                    return {
                        "success": False, 
                        "message": response.text,
                        "cookies": None 
                        }
    
            else:
                worker_logger.error("Server Permission Denied")
                logger.error("Server Permission Denied")
                raise HTTPException(status_code=response.status_code, detail=f"Ifuse Server Error: {response.status_code}")
                
        except httpx.ConnectError:
            worker_logger.error("Connection Wrong, Check Lan Ethernet")
            logger.error("Connection Wrong, Check Lan Ethernet")
            raise HTTPException(status_code=503, detail="Check connect ethernet")
            
        except httpx.TimeoutException:
            worker_logger.error("Server Overload")
            logger.error("Server Overload")
            raise HTTPException(status_code=504, detail="Server Overload (Timeout).")
            
        except httpx.RequestError as e:
            # Lỗi mạng chung chung
            raise HTTPException(status_code=502, detail=f"API: {str(e)}")
            
        except Exception as e:
            print(f"Lỗi hệ thống: {e}")
            raise HTTPException(status_code=500, detail="Internal Type")
        
    async def get_yield(self,list_station,section,family,timeFrom,timeTo,route):
        key="get_yield"
        url = self.template[key]['url']
        payload = self.template[key]['payload']
        payload['section'] = section
        payload['family'] = family
        payload['timeFrom'] = timeFrom
        payload['timeTo'] = timeTo
        payload['route'] = route
        try:
            response = await session.post(url,json=payload)
            data=json.loads(response.json()["d"])
            filtered_groups = [item for item in data if item['GROUP_NAME'] in list_station]
            df=pd.DataFrame(filtered_groups)
            return filtered_groups
        except Exception as e:
            print(e)
    
    async def get_groups(self,family,section):
        key="list_group_name"
        url = self.template[key]['url']
        payload = self.template[key]['payload']
        payload["family"]=family
        payload["section"]=section

        response= await session.post(url,json=payload)
        
        return list([item["Value"] for item in response.json()['d']])
    
    async def get_lines(self,family,section):
        key="list_line_name"
        url = self.template[key]['url']
        payload = self.template[key]['payload']
        payload["Family"]=family
        payload["section"]=section

        response=await session.post(url,json=payload)
        return list([item["Value"] for item in response.json()['d']])
    
    async def get_familys(self,section):
        key="list_family_name"
        url = self.template[key]['url']
        payload = self.template[key]['payload']
        payload["section"]=section

        response=await session.post(url,json=payload)
        return list([item["Value"] for item in response.json()['d']])
    
    async def get_route_names(self,family,section):
        key="list_route_name"
        url = self.template[key]['url']
        payload = self.template[key]['payload']
        payload["family"]=family
        payload["section"]=section

        response=await session.post(url,json=payload)
        return list([{"Text": item["Text"],"Value": item["Value"]} for item in response.json()['d']])






if __name__=="__main__":
    # 1. Tạo một hàm main bất đồng bộ để bọc code lại
    async def main():
        api = IfuseApi()
        u = "V1531673"
        p = "Taidepzai102@@"
        stations= ["FATP-RF-5GMMW-COMBO","FATP-RF-CELL","FATP-RF-WIFIBT","FATP-AUDIO"]
        # Bây giờ bạn có thể dùng await thoải mái bên trong hàm này
        result = await api.login(user=u, password=p)
       # res = await api.get_yield(stations)
        #print(res)
        
        
        #line = await api.get_route_names(family="4CS4",section="ASSY")
        #print(line)

    asyncio.run(main())
    
     
    