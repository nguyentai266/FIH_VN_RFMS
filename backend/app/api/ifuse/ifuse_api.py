import asyncio
import json
from pathlib import Path

import httpx
import pandas as pd
import urllib3
from core.logger import logger, worker_logger
from fastapi import HTTPException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class IfuseApi():
    def __init__(self) -> None:
        current_path = Path(__file__).parent
        with open(current_path / "ifuse_template.json", 'r', encoding='utf-8') as f:
            self.template = json.load(f)
        self.offline = True
        self.session = None

    async def __aenter__(self):
       
        self.session = httpx.AsyncClient(verify=False, follow_redirects=True)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()

    async def _send_request(self, key: str, payload_updates: dict) -> httpx.Response:
        if self.session is None:
            self.session = httpx.AsyncClient(verify=False, follow_redirects=True)
            
        url = self.template[key]['url']
       
        payload = self.template[key]['payload'].copy()
        payload.update(payload_updates)
        
        try:
            data = await self.session.post(url, json=payload, timeout=20.0)
            #print(data.text)
            return data
        except httpx.RequestError as e:
           
            if url.startswith("https://"):
                fallback_url = url.replace("https://", "http://")
                worker_logger.warning(f"Error with method {key}.Retry with HTTP: {fallback_url}")
                
                
                self.template[key]['url'] = fallback_url
                return await self.session.post(fallback_url, json=payload, timeout=20.0)
            raise e 

    async def login(self, user, password):
        try:
            
            response = await self._send_request('login', {'u': user, 'p': password})
            
            if response.status_code == 200:
                if '"success":true' in response.text: 
                    res_json = response.json()
                    if res_json.get('success') == True: 
                        worker_logger.info(f"Login OK, Username: {user}")
                        logger.info(f"Login OK, Username: {user}")
                        return {
                            "success": True, 
                            "message": "Login OK",
                            "cookies": self.session.cookies if self.session else None
                        }
                
                worker_logger.info(f"Login Error, Username: {user}, Message: {response.text}")
                logger.info(f"Login Error, Username: {user}, Message: {response.text}")
                return {"success": False, "message": response.text, "cookies": None}
    
            else:
                worker_logger.error(f"Server Permission Denied: {response.status_code}")
                logger.error(f"Server Permission Denied: {response.status_code}")
                raise HTTPException(status_code=response.status_code, detail=f"Ifuse Server Error: {response.status_code}")
                
        except httpx.ConnectError:
            worker_logger.error("Connection Wrong, Check Lan Ethernet")
            logger.error("Connection Wrong, Check Lan Ethernet")
            raise HTTPException(status_code=503, detail="Check connect ethernet")
            
        except httpx.TimeoutException:
            worker_logger.error("Server Overload (Timeout)")
            logger.error("Server Overload (Timeout)")
            raise HTTPException(status_code=504, detail="Server Overload (Timeout).")
            
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"API Request Error: {str(e)}")
            
        except Exception as e:
            print(f"System Error: {e}")
            raise HTTPException(status_code=500, detail="Internal System Type Error")
        
    async def get_yield(self, list_station, section, family, timeFrom, timeTo, route):
        try:
            updates = {
                'section': section, 'family': family, 
                'timeFrom': timeFrom, 'timeTo': timeTo, 'route': route
            }
            response = await self._send_request('get_yield', updates)
            data = json.loads(response.json()["d"])

            
            filtered_groups = [item for item in data if item.get('GROUP_NAME') in list_station]
            return filtered_groups
        except Exception as e:
            worker_logger.error(f"Error in get_yield: {e}")
            return []
    
    async def get_groups(self, family, section):
        try:
            response = await self._send_request('list_group_name', {"family": family, "section": section})
            return list([item["Value"] for item in response.json()['d']])
        except Exception as e:
            return []
    
    async def get_lines(self, family, section):
        try:
            response = await self._send_request('list_line_name', {"Family": family, "section": section})
            return list([item["Value"] for item in response.json()['d']])
        except Exception as e:
            return []
    
    async def get_familys(self, section):
        try:
            response = await self._send_request('list_family_name', {"section": section})
            return list([item["Value"] for item in response.json()['d']])
        except Exception as e:
            return []
    
    async def get_route_names(self, family, section):
        try:
            response = await self._send_request('list_route_name', {"family": family, "section": section})
            return list([{"Text": item["Text"], "Value": item["Value"]} for item in response.json()['d']])
        except Exception as e:
            return []
    async def get_product_info(self,SN):
        try:
            response = await self._send_request('get_product_info',{"sn": SN})
            return response.json().get('d',[])
        except Exception as e:
            return []



if __name__ == "__main__":
    async def main():
        u = "V1531673"
        p = "Taidepzai102@@"
        stations = ["FATP-RF-5GMMW-COMBO", "FATP-RF-CELL", "FATP-RF-WIFIBT", "FATP-AUDIO"]
        
        
        async with IfuseApi() as api:
            
            login_res = await api.login(user=u, password=p)
            print("🔑 Kết quả Login:", login_res)
            
            if login_res.get("success"):
                
                routes = await api.get_route_names(family="4CS4", section="ASSY")
                print("🏁 Danh sách Route thu về:", routes)
                
                
                yield_data = await api.get_yield(
                    list_station=stations,
                    section="ASSY",
                    family="4CS4",
                    timeFrom="2026-05-01 08:00:00",
                    timeTo="2026-05-02 08:00:00",
                    route="ALL"
                )
                print(f"📊 Thu về {len(yield_data)} bản ghi Yield dữ liệu.")

   
    asyncio.run(main())


    #"Message": "The session is timeout,pls relogin.",