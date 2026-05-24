import requests
from bs4 import BeautifulSoup

# 1. URL sếp cần lấy data
url = "http://10.239.73.165:8095/4CS4/"

# 2. Bê nguyên xi cục Cookie từ ảnh của sếp vào đây
# (Đây là thẻ bài giúp bypass bước Login)
my_cookies = {
    "session": "5252070e-b7cc-450d-8f5c-ca67fb640552",
    "local-username": "taint1",
    "local-logintype": "LDAP",
    "local-userid": "300",
    "local-token": "28a840973370d18cef2b50c2c9e3d75ba31607ce19ec0fe6ac368772396e3506"
}

# Giả lập luôn cái User-Agent cho giống y hệt Google Chrome của sếp
my_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

print("⏳ Đang cắm vòi hút data từ server...")

# 3. Thực hiện gọi GET request, đính kèm Cookie
response = requests.get(url, cookies=my_cookies, headers=my_headers)

# 4. Kiểm tra và vắt dữ liệu
if response.status_code == 200:
    print("✅ Lấy HTML thành công! Đang bóc tách bảng...")
    
    # Ném nguyên cục HTML thu được vào thớt BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # === TỪ ĐÂY SẾP DÙNG BEAUTIFULSOUP ĐỂ TÌM TABLE ===
    # Ví dụ: Tìm cái bảng chứa dữ liệu log
    table = soup.find('table')
    
    if table:
        rows = table.find('tbody').find_all('tr')
        print(f"👉 Tìm thấy {len(rows)} dòng dữ liệu trong bảng!")
        
        # In thử dữ liệu dòng đầu tiên cho sếp xem
        first_row_cells = rows[0].find_all('td')
        first_row_data = [cell.text.strip() for cell in first_row_cells]
        print("Dòng 1:", first_row_data)
    else:
        print("Không tìm thấy thẻ <table> nào trong trang này.")
        
else:
    print(f"❌ Thất bại! Server trả về mã: {response.status_code}")