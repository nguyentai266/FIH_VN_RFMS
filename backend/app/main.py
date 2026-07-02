import os

import httpx
from api.ifuse.ifuse_api import IfuseApi
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

api_services=IfuseApi()
app = FastAPI(title="FIH VN - RFMS Backend")

# 1. Cấu hình CORS (Chỉ dùng khi đang code, React chạy port 5173 gọi sang port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đường dẫn giả định của API bên bộ phận IT
#IT_SERVER_URL = "http://10.0.x.x/api/v1"

# ---------------------------------------------------------
# PHẦN 1: API ĐĂNG NHẬP (LÀM TRUNG GIAN GỌI SANG IT)
# ---------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/v1/login")
async def login(request: LoginRequest):
    return await api_services.login(user=request.username,
                                    password=request.password)


# ---------------------------------------------------------
# PHẦN 2: API LẤY TỈ LỆ TEST RATE (XỬ LÝ LẠI DỮ LIỆU)
# ---------------------------------------------------------
@app.get("/api/dashboard/test-rate")
async def get_dashboard_data():
    """
    Lấy cục dữ liệu to từ IT, lọc lại cho gọn gàng rồi gửi cho React vẽ biểu đồ Recharts
    """
    
    async with httpx.AsyncClient() as client:
        try:
            # Code thực tế sẽ gọi: await client.get(f"{IT_SERVER_URL}/test-records")
            
            # GIẢ LẬP cục dữ liệu thô kệch mà IT Server trả về:
            raw_data_from_it = [
                {"date": "2026-04-15", "test_log_pass": 400, "test_log_fail": 20, "operator": "A", "line": "L1"},
                {"date": "2026-04-16", "test_log_pass": 300, "test_log_fail": 15, "operator": "B", "line": "L1"},
                {"date": "2026-04-17", "test_log_pass": 500, "test_log_fail": 10, "operator": "A", "line": "L2"},
            ]
            
            # CHẾ BIẾN LẠI DỮ LIỆU (Giống cách bạn làm Pandas)
            clean_data_for_react = []
            for item in raw_data_from_it:
                total = item["test_log_pass"] + item["test_log_fail"]
                rate = round((item["test_log_pass"] / total) * 100, 1) if total > 0 else 0
                
                clean_data_for_react.append({
                    "name": item["date"],
                    "pass": item["test_log_pass"],
                    "fail": item["test_log_fail"],
                    "rate": rate
                })
                
            return {"status": "success", "data": clean_data_for_react}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))




# ---------------------------------------------------------
# PHẦN 3: TUYỆT CHIÊU GỘP REACT VÀ FASTAPI LÀM 1 (CHỈ DÙNG KHI CHẠY THỰC TẾ)
# ---------------------------------------------------------
# Lưu ý: Các API (/api/...) phải được khai báo TRƯỚC đoạn code này.
# Đoạn này báo FastAPI hãy hiển thị thư mục 'dist' (code React đã đóng gói) khi truy cập http://localhost:8000/
'''
frontend_build_path = "../frontend/dist"

if os.path.exists(frontend_build_path):
    app.mount("/", StaticFiles(directory=frontend_build_path, html=True), name="frontend")'''

