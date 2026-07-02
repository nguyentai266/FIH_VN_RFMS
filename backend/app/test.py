import asyncio

import pandas as pd
from api.ifuse.ifuse_api import IfuseApi
from tracking_yield import buffer
from tracking_yield.webhook import notify_send_message

stations= ["FATP-RF-5GMMW-COMBO","FATP-RF-CELL","FATP-RF-WIFIBT","FATP-AUDIO"]
request={"list_station" : stations,
         "section": "ASSY",
         "family": "4CS4",
         "timeFrom": "2026-05-12 08:00",
         "timeTo": "2026-05-12 20:00",
         "route": 1948581966}
api = IfuseApi()

async def api_c():
    
    await api.login("V1531673","Taidepzai102@@")
    df = pd.read_csv('list_sn.csv')
    list_sn = df['sn'].to_list()
    for sn in list_sn:

        res= await api.get_product_info(SN=sn)
        info_imei = res[6]
        

asyncio.run(api_c())
asyncio.run(api_c())
