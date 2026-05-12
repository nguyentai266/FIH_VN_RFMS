import os
import smtplib
from email.message import EmailMessage


def send_internal_mail(image_path, space_email):
    print("⏳ Đang chuẩn bị gói hàng...")
    
    msg = EmailMessage()
    msg['Subject'] = "📊 BÁO CÁO YIELD RATE - D26 LINE 01"
    
    # Bạn có thể fake một cái email người gửi cho ngầu (VD: rfms_bot@fih-foxconn.com)
    # Vì gửi nội bộ không pass nên server thường không xác minh email người gửi
    msg['From'] = "rfms@fih-foxconn.com" 
    msg['To'] = "dungpt@fih-foxconn.com" 
    msg.set_content("Báo cáo Yield Rate cập nhật tự động. Chi tiết anh em xem ảnh đính kèm bên dưới 👇")

    # Đính kèm ảnh
    print("📎 Đang đính kèm ảnh...")
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            image_name = os.path.basename(image_path)
        msg.add_attachment(image_data, maintype='image', subtype='png', filename=image_name)
    except Exception as e:
        print(f"❌ Lỗi đọc file ảnh: {e}")
        return

    # KẾT NỐI MÁY CHỦ NỘI BỘ VÀ BẮN (KHÔNG CẦN PASSWORD)
    # THAY DÒNG NÀY BẰNG IP HOẶC TÊN MIỀN SMTP CỦA XƯỞNG!
    SMTP_SERVER = "mail.fihtdc.com" # Hoặc điền IP: "10.20.30.40"
    SMTP_PORT = 25 # Cổng mặc định của SMTP nội bộ thường là 25
    
    print(f"🚀 Đang bắn qua máy chủ {SMTP_SERVER}:{SMTP_PORT}...")
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # Không cần starttls(), không cần login()
            server.send_message(msg)
            print("✅ ĐÃ GỬI THÀNH CÔNG VÀO NHÓM CHAT!")
    except Exception as e:
        print(f"❌ LỖI KẾT NỐI: {e}\n(Bạn hãy check lại chính xác IP của máy chủ SMTP xưởng nhé)")

# Chạy thử
if __name__ == "__main__":
    send_internal_mail("pro_dashboard.png", "rfms@fih-foxconn.com")
