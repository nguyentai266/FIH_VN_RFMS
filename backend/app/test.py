import asyncio

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
    res= await api.get_yield(**request)
    card= buffer.draw_dashboard(res,'4CS4','4CS4_FVN-E2F3-G01',"2026-05-12 08:00","2026-05-12 20:00")
    notify_send_message(card)
    print(res)
    asyncio.run(api_c())
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. Xác thực bằng file JSON của Service Account
SCOPES = ['https://www.googleapis.com/auth/chat.messages.create']
creds = service_account.Credentials.from_service_account_file('service-account-key.json', scopes=SCOPES)
chat = build('chat', 'v1', credentials=creds)

# 2. Upload file ảnh lên Google trước
file_metadata = {'name': 'yield_report.png'}
media = MediaFileUpload('pro_dashboard.png', mimetype='image/png')
attachment = chat.media().upload(parent='spaces/XXXXX', body=file_metadata, media_body=media).execute()

# 3. Gửi tin nhắn kèm theo cái ảnh vừa upload
message = {
    'text': 'Đây là báo cáo Yield Rate mới nhất!',
    'attachment': [attachment]
}
chat.spaces().messages().create(parent='spaces/XXXXX', body=message).execute()