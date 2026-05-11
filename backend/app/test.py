import asyncio

from api.ifuse.ifuse_api import IfuseApi
from tracking_yield import buffer
from tracking_yield.webhook import notify_send_message

stations= ["FATP-RF-5GMMW-COMBO","FATP-RF-CELL","FATP-RF-WIFIBT","FATP-AUDIO"]
request={"list_station" : stations,
         "section": "ASSY",
         "family": "4CS4",
         "timeFrom": "2026-05-11 08:00",
         "timeTo": "2026-05-11 20:00",
         "route": 1948581966}
api = IfuseApi()

async def api_c():
    await api.login("V1531673","Taidepzai102@@")
    res= await api.get_yield(**request)
    card= buffer.draw_pro_dashboard(res) 
    notify_send_message(card)
    print(res)
asyncio.run(api_c())
