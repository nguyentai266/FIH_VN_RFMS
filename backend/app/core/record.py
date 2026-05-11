# backend/app/main.py
import sys

from loguru import logger

# XÓA CẤU HÌNH MẶC ĐỊNH CỦA LOGURU
logger.remove()

# 1. IN RA MÀN HÌNH (CÓ MÀU CODE ĐẸP MẮT)


# 2. GHI VÀO FILE LOG TỔNG HỢP (TỰ ĐỘNG CHIA FILE)
from loguru import logger

# Xóa cấu hình in ra console mặc định để tự custom lại
logger.remove()

# ---------------------------------------------------------
# 1. LOG TỔNG HỢP: Hứng TOÀN BỘ mọi thứ (Không dùng filter)
# ---------------------------------------------------------
logger.add(
    "logs/tong_hop.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    encoding="utf-8"
)

# ---------------------------------------------------------
# 2. LOG RIÊNG CHO API: Chỉ hứng log từ thư mục 'api'
# ---------------------------------------------------------
# Giải thích filter: Kiểm tra xem chữ "api" có nằm trong đường dẫn file không
logger.add(
    "logs/api_requests.log",
    filter=lambda record: "api" in record["name"], 
    rotation="5 MB",
    level="INFO",
    encoding="utf-8"
)

# ---------------------------------------------------------
# 3. LOG RIÊNG CHO SERVICES: Chỉ hứng log từ thư mục 'services'
# ---------------------------------------------------------
logger.add(
    "logs/services_logic.log",
    filter=lambda record: "services" in record["name"] or "tracking_worker" in record["name"],
    rotation="5 MB",
    level="INFO",
    encoding="utf-8"
)

# ---------------------------------------------------------
# 4. IN RA MÀN HÌNH CONSOLE (Để Dev nhìn lúc code)
# ---------------------------------------------------------
logger.add(sys.stderr, level="DEBUG", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>")

