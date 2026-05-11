from json import dumps

from httplib2 import Http

# Copy the webhook URL from the Chat space where the webhook is registered.
# The values for SPACE_ID, KEY, and TOKEN are set by Chat, and are included
# when you copy the webhook URL.
test_pay_load= {
    "cardsV2": [
        {
            "cardId": "table_report_card",
            "card": {
                "header": {
                    "title": "📋 DANH SÁCH THIẾT BỊ LỖI",
                    "subtitle": "Cập nhật lúc: 13:00 - 11/05/2026",
                    "imageUrl": "[https://cdn-icons-png.flaticon.com/512/1008/1008927.png](https://cdn-icons-png.flaticon.com/512/1008/1008927.png)",
                    "imageType": "CIRCLE"
                },
                "sections": [
                    {
                        "widgets": [
                            {
                                "columns": {
                                    "columnItems": [
                                        {
                                            "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                                            "widgets": [
                                                {
                                                    "textParagraph": {
                                                        "text": "<b><u>MÃ MÁY (MACHINE ID)</u></b><br><br>SMT-M01<br>SMT-M05<br>AOI-02"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                                            "widgets": [
                                                {
                                                    "textParagraph": {
                                                        "text": "<b><u>TÌNH TRẠNG LỖI</u></b><br><br><font color=\"#ff0000\">Kẹt băng tải</font><br><font color=\"#ff9900\">Nhiệt độ cao</font><br><font color=\"#ff0000\">Mất kết nối LAN</font>"
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
def main():
    """Google Chat incoming webhook quickstart."""
    url = "https://chat.googleapis.com/v1/spaces/AAQAKkrRG6w/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=f33fCHEzxgYeD8-qQUyDVCJbSQFG4rNIg5-hG-5WIIE"
    app_message = {
        "text": "Hello from a Python script!"
    }
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    pay_load = generate_table_payload(fake_db_data)
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(pay_load),
    )
    print(response)
def generate_table_payload(data_list):
    # Dòng tiêu đề bảng
    table_str = "```\n| Dây chuyền | PASS | FAIL |\n"
    table_str += "|------------|------|------|\n"
    
    # Lặp qua data từ Database để đắp thêm dòng
    for row in data_list:
        # Dùng ljust() để căn lề cho thẳng cột chữ
        line = str(row['line']).ljust(10)
        p_count = str(row['pass_qty']).ljust(4)
        f_count = str(row['fail_qty']).ljust(4)
        
        table_str += f"| {line} | {p_count} | {f_count} |\n"
    
    table_str += "```"
    
    # Đóng gói thành JSON chuẩn Google Chat
    payload = {
        "text": f"📊 *BÁO CÁO NHANH*\n{table_str}"
    }
    return payload

# Data mẫu lấy từ DB
fake_db_data = [
    {"line": "Line 01", "pass_qty": 900, "fail_qty": 12},
    {"line": "Line 02", "pass_qty": 850, "fail_qty": 5}
]

# Chạy thử

# Việc còn lại là truyền final_payload này vào httpx.post(...)

if __name__ == "__main__":
    main()