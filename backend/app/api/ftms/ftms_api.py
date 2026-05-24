import asyncio
import json

import httpx
import pandas as pd
from bs4 import BeautifulSoup

request=httpx.request

class FTMSApiServices():
    def __init__(self) -> None:
        self.client = None
        self.session =None
        self.auth = {}
    async def __aenter__(self):
        self.client = httpx.AsyncClient(follow_redirects=True)
        return self
    async def __aexit__(self):
        if self.client:
            await self.client.aclose()

    async def api_login(self,username,password) ->object:
        if self.client is None:
            self.client =  httpx.AsyncClient(follow_redirects=True)

        try:
           
            api_url = "http://10.239.73.165:8095/api/auth/login"
            api_res = await self.client.post(url=api_url, json={"username": username, "password": password})
            
            
            web_url = "http://10.239.73.165:8095/auth/login"
            await self.client.post(url=web_url, data={"username": username, "password": password})
            
            if api_res.status_code == 200:
                self.auth = api_res.json()
                print("Login OK")
                return True
            return False
        except Exception as e:
            print(f"Error Login: {e}")
            return False
        


    async def get_record_list(self,project:str,dut_id:str,test_mode:str):
        url= "http://10.239.73.165:8095/api/test_record_list"
        payload = {
            "project": project,
            "dut_list": dut_id,
            "query_type": "single",
            "user_id": self.auth['user_id'], 
            "user_token": self.auth['user_token'],
            'test_mode':test_mode.upper()
        }

        
        record_list = await self.client.post(url, json=payload)   # type: ignore
        if record_list.status_code == 200:
            return record_list.json()['test_records']
        else: return None


    async def get_record_detail(self,project,test_start,test_end,record_main_id):
            url = "http://10.239.73.165:8095/api/test_record_detail"
            payload={
                'project':project,
                'user_token': self.auth['user_token'],
                'user_id': self.auth['user_id'],
                'test_start':test_start,
                'record_main_id':record_main_id    
            }
            record_detail = await self.client.get(url,params=payload) # type: ignore
            if record_detail.status_code == 200:
                return record_detail.json()
            else: return None

    async def get_station_info(self,project):
        
        url = f"http://10.239.73.165:8095/{project}"
        
        data= await self.client.get(url=url)   # type: ignore
        #print(data.text)
        return data
       
    @staticmethod
    def convert_json2csv(json_data):
        
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
            '''with open(log_name.replace(".csv",".json"),'w') as f:
                json.dump(json_data,f,indent=4,ensure_ascii=False)'''
import pandas as pd
from bs4 import BeautifulSoup


def export_ftms_to_csv_clean(html_text, csv_filename="ftms_stations_clean.csv"):
    """
    Hàm lọc dữ liệu FTMS: Chỉ lấy dòng có IP, trích xuất 5 cột cốt lõi ra DataFrame & CSV.
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    table = soup.find('table')
    
    if not table:
        print("❌ Không tìm thấy bảng nào trong HTML để xử lý.")
        return None
        
    tbody = table.find('tbody')
    rows = tbody.find_all('tr') if tbody else table.find_all('tr')
    
    cleaned_data = []
    
    for row in rows:
        cells = row.find_all('td')
        # Kiểm tra điều kiện số cột (đảm bảo không bốc nhầm dòng trống/dòng lỗi)
        if len(cells) < 7:
            continue
            
        # 1. Lấy IP trước để check điều kiện
        ip_address = cells[2].text.strip()
        
        # 🌟 ĐIỀU KIỆN CHÍ MẠNG: Có IP thì lấy, "None" hoặc trống là bỏ qua luôn
        if not ip_address or "none" in ip_address.lower():
            continue
            
        # 2. Bốc các trường còn lại theo đúng yêu cầu của sếp
        project = cells[3].text.strip()          # Dự án (TK4, 4CS4...)
        line = cells[4].text.strip()             # Line (FVN-N1F-T01...)
        station_id = cells[5].text.strip()       # Station ID đầy đủ
        station_type = cells[6].text.strip()     # Tên trạm / Loại trạm (SMT-FLASH...)
        
        # Đút vào mảng dữ liệu sạch
        cleaned_data.append({
            "IP": ip_address,
            "Dự Án": project,
            "Line": line,
            "Station ID": station_id,
            "Tên Trạm": station_type
        })
        
    # 🚀 BƯỚC 3: Đổ vào Pandas DataFrame
    df = pd.DataFrame(cleaned_data)
    
    print(f"📊 Đã tạo xong DataFrame! Tổng cộng có {len(df)} trạm hợp lệ (đã lọc bỏ trạm lỗi IP).")
    
    # In thử data cho sếp check ngay trên Terminal
    if not df.empty:
        print("\n👀 Xem trước 2 dòng đầu tiên:")
        print(df.head(2).to_string())
        
        # 🚀 BƯỚC 4: Xuất thẳng ra file CSV chuẩn chỉnh
        # Sử dụng encoding='utf-8-sig' để sếp click đúp mở bằng Excel không bao giờ lỗi font
        df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
        print(f"💾 Đã xuất file CSV ngon lành tại: {csv_filename}")
    else:
        print("⚠️ Không có dữ liệu nào thỏa mãn điều kiện có IP.")
        
    return df
async def run():
    
    api = FTMSApiServices()
    await api.api_login(username='taint1',password="Quenmeroi102@")
    data = await api.get_station_info(project='4CS4')
    export_ftms_to_csv_clean(data)

    #await get_station_info(project='4CS4')
    #record_list = await api.get_record_list(project='4CS4',dut_id='63130DLKY0000H',test_mode='DEBUG')
    #json_data=await api.get_record_detail(project="4CS4",test_start=1778904004416,test_end=1778904037255,record_main_id=999248)
    
asyncio.run(run())