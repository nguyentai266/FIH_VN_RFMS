import asyncio

import httpx
from bs4 import BeautifulSoup

soup = BeautifulSoup()

async def test_real_login():
    # Bật follow_redirects=True để nó tự chuyển hướng sau khi login thành công
    async with httpx.AsyncClient(follow_redirects=True) as client:
        
        # 🚨 SẾP ĐỔI THÀNH LINK LOGIN THỰC TẾ TRÊN WEB XƯỞNG NHA
        login_url = "http://10.239.73.165:8095/auth/login" 
        
        # Nhìn đúng tên trường 'username' và 'password' trong HTML sếp gửi
        payload = {
            "username": "taint1",
            "password": "Quenmeroi102@" # Mật khẩu chuẩn của sếp
        }
        
        print("⏳ Đang dập lệnh Login bằng Form Data...")
        # 🌟 Chí mạng: Phải dùng data= chứ KHÔNG DÙNG json=
        response = await client.post(login_url, data=payload)
        
        print(f"Mã phản hồi từ server: {response.status_code}")
        print("🍪 Cookies sau khi bấm Login:", client.cookies)
        
        # Kiểm tra xem trong HTML trả về còn chữ "Please sign in" không
        if "please sign in" in response.text.lower():
            print("❌ Thất bại! Vẫn bị kẹt ở trang Login. Khả năng cao là sai URL Login hoặc sai mật khẩu.")
        else:
            print("🎉 NGON RỒI! Đã vượt ải thành công. Đang cào thử trang trạm...")
            # Thử cào trang data trạm luôn bằng con client đã có cookie xịn này
            data_res = await client.get("http://10.239.73.165:8095/4CS4/")
            print(data_res.text) # In thử 500 ký tự đầu xem có bảng chưa
            # Đoạn code kiểm tra xem bảng có dữ liệu thật hay chỉ là khung rỗng
            table = soup.find('table')
            if table:
                print("📋 Cấu trúc thẻ table cào được:")
                # In thử thuộc tính của table xem có chữ "data-url" hay không
                print(table.attrs) 
                
                rows = table.find_all('tr')
                print(f"👉 Số dòng thực tế trong HTML thô: {len(rows)}")

asyncio.run(test_real_login())