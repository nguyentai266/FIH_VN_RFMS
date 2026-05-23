import asyncio
import json

import httpx
import pandas as pd

request=httpx.request
session=httpx.AsyncClient(verify=False)

async def do_login(username,password) -> object:
    url = "http://10.239.73.165:8095/api/auth/login"
    payload = {"username": username, 
               "password": password}
    
    rev = request('POST',url=url, json=payload)
    
    
    if rev.status_code == 200: return rev.json()
    else: return None


async def get_record_list(auth,project:str,dut_id:str,test_mode:str):
    url= "http://10.239.73.165:8095/api/test_record_list"
    payload = {
        "project": project,
        "dut_list": dut_id,
        "query_type": "single",
        "user_id": auth['user_id'],
        "user_token": auth['user_token'],
        'test_mode':test_mode.upper()
    }
    record_list = request('POST',url, json=payload)
    if record_list:
        return record_list.json()['test_records']
    else: return None


async def get_record_detail(auth,project,test_start,record_main_id):
        url = "http://10.239.73.165:8095/api/test_record_detail"
        payload={
            'project':project,
            'user_token':auth['user_token'],
            'user_id':auth['user_id'],
            'test_start':test_start,
            'record_main_id':record_main_id    
        }
        record_detail = request('GET',url,params=payload)
        if record_detail:
            return record_detail.json()

async def get_station_info(auth,project):
    url = f"http://10.239.73.165:8095/{project}/"
    cookies={
        'user_id':auth['user_id'],
        'user_token':auth['user_token']
    }
    stations= await session.get(url,cookies=cookies)
    print(stations)

def convert_json2csv(json_data) -> None:
    if json_data:
        log_name=(json_data.get('json_log_name')).replace('.json','.csv')
        metadata = json_data.get('test_metadata', {})
        dut_id = metadata.get('dut_id')
        project = metadata.get('project')
        station_id = metadata.get('station_id')
        test_result = json_data.get('test_result')
        device_config = metadata.get('device_config')
       
        data=[]
        for phase_key in json_data['test_items']:
          
            for item_data in json_data['test_items'][phase_key]['measurements']:
                data.append({'phase':phase_key,'measurement':item_data['measurement_name'],'value':item_data['measured_value'],'low_limit':item_data['min'],'high_limit':item_data['max'],'result':item_data['measurement_result'],'low_limit2':"",'high_limit2':""})
        info= f"dut_id:{dut_id} result:{test_result} time:19.97 device_config: {device_config} station_id: {station_id}\n"
        with open(log_name,'w') as f:
            f.write(info)
        
        df=pd.DataFrame(data=data)
        df.to_csv(log_name,index=False,mode="a")



async def run():
    auth = await do_login('taint1','Quenmeroi102@')
    print(auth)
    if auth:
        record_list = await get_record_list(auth,'4CS4',dut_id='63130DLKY0000H',test_mode='DEBUG')

        #json_data=await get_record_detail(auth,'4CS4',1779064482194,1040086)
        #convert_json2csv(json_data)
        #await get_station_info(auth,'4CS4')
asyncio.run(run())