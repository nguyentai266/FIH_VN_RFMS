import asyncio
import json
from pathlib import Path

import httpx
import pandas as pd
import urllib3
from fastapi import HTTPException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config_path='config_api.yaml'
session = httpx.AsyncClient(verify=False)
#session.options()

class GetDataAPI():
    def __init__(self) -> None:
        current_path=Path(__file__).parent
        self.template=json.load(open(current_path/"template.json",'r'))
        self.offline = True
    async def login(self,user,password):
        url = self.template['login']['url']
        payload = self.template['login']['payload']
        payload['u']=user
        payload['p']=password
        try:
            if self.offline == True :
                return {
                "status": "success", 
                "message": "Đăng nhập thành công", 
                "token": "fih_vn_secret_token_123" # Token để dùng cho các bước sau
            }
            return
            response = await session.post(url, json=payload)
            if response.status_code == 200 and response.json()['success'] == True:
                return {
                "status": "success", 
                "message": "Đăng nhập thành công", 
                "token": "fih_vn_secret_token_123" # Token để dùng cho các bước sau
            }
            else:
                raise HTTPException(status_code=401,detail="Username or Password wrong!!!")
        except Exception as e:
            
            raise HTTPException(status_code=500,detail="Server Connection Failed!!!")
            
        
    async def get_yield(self,list_station):
        key="get_yield"
        url = self.template[key]['url']
        payload = self.template[key]['payload']
        try:
            response = await session.post(url,json=payload)
            data=json.loads(response.json()["d"])
            filtered_groups = [item for item in data if item['GROUP_NAME'] in list_station]
            df=pd.DataFrame(filtered_groups)
            return filtered_groups
        except Exception as e:
            pass
    
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
        return list([{"Text":item["Text"],"Value":item["Value"]} for item in response.json()['d']])






if __name__=="__main__":
    # 1. Tạo một hàm main bất đồng bộ để bọc code lại
    async def main():
        api = GetDataAPI()
        u = "V1531673"
        p = "Taidepzai102@@"
        
        # Bây giờ bạn có thể dùng await thoải mái bên trong hàm này
        result = await api.login(user=u, password=p)
        print("ok:", type(result))
        
        line = await api.get_route_names(family="4CS4",section="ASSY")
        print(line)
        # Nếu muốn test thêm hàm get_groups thì gọi tiếp ở đây:
        # if headers:
        #     groups = await api.get_groups(header=headers, family="...", section="...")
        #     print(groups)

    # 2. Dùng asyncio để kích hoạt hàm main() chạy
    asyncio.run(main())
    
     
    