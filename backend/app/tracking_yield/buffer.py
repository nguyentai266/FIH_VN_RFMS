

def generate_yield_table_payload(data):
    # 1. Khởi tạo Header của bảng (Căn lề độ rộng từng cột)
    # Lấy 20 ký tự cho Group, các cột số lấy 8-9 ký tự
    table_str = "```\n"
    table_str += "|           Station Name           | Total | First Fail | Retest Pass | Final Fail |\n"
    table_str += "|----------------------------------|-------|------------|-------------|------------|\n"
                 
    # 2. Đổ dữ liệu vào từng dòng
    for row in data:
        # Cắt ngắn tên nếu quá dài và căn trái (ljust)
        group = str(row.get('GROUP_NAME', ''))[:20].ljust(20)
        
        # Ép kiểu int() để bỏ số .0 ở đuôi, sau đó căn phải (rjust)
        total = str(int(row.get('COUNT_TOTAL', 0))).rjust(5)
        first_fail = str(int(row.get('FIRST_FAIL', 0))).rjust(8)
        retest_pass = str(int(row.get('RETEST_PASS', 0))).rjust(8)
        final_fail = str(int(row.get('FINAL_FAIL', 0))).rjust(7)
        
        # Nối vào bảng
        table_str += f"| {group} | {total} | {first_fail} | {retest_pass} | {final_fail} |\n"
    
    table_str += "```"
    
    # 3. Gói thành JSON chuẩn Google Chat
    payload = {
        "text": f"Yield Report*\n{table_str}"
    }
    
    return payload

def generate_yield_card_v2(data_list):
    # Khởi tạo danh sách các Widget (Từng hàng của bảng)
    widgets_list = []

    # ==========================================
    # 1. TẠO HÀNG TIÊU ĐỀ (HEADER ROW)
    # ==========================================
    widgets_list.append({
        "columns": {
            "columnItems": [
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": "<b>Station Name</b>"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": "Total"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": "FirstPass"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": "FirstFail"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": "RetestPass"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": "FinalFail"}}]
                },
            ]
        }
    })
    
    # Kẻ một đường gạch ngang phân cách tiêu đề
    widgets_list.append({"divider": {}})

    # ==========================================
    # 2. ĐỔ DỮ LIỆU TỪNG TRẠM VÀO CÁC HÀNG
    # ==========================================
    for row in data_list:
        group = str(row.get('GROUP_NAME', ''))
        total = int(row.get('COUNT_TOTAL', 0))
        first_pass = int(row.get('FIRST_PASS', 0))
        first_fail = int(row.get('FIRST_FAIL', 0))
        retest_pass = int(row.get('RETEST_PASS', 0))
        final_fail = int(row.get('FINAL_FAIL', 0))

        # Nếu Final Fail lớn hơn 0 -> Bôi đậm và tô màu ĐỎ chót cho sếp chú ý!
        if final_fail > 0:
            fin_str = f"<font color=\"#ff0000\"><b>{final_fail}</b></font>"
        else:
            fin_str = f"<font color=\"#00ff00\">{final_fail}</font>" # Màu xanh nếu an toàn

        # Nối các chỉ số lại (Dùng dấu / để tiết kiệm không gian ngang)
        metrics_str = f"{total} / {first_fail} / {retest_pass} / {fin_str}"

        # Thêm 1 hàng mới vào thẻ
        widgets_list.append({
            "columns": {
            "columnItems": [
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": f"<b>{group}</b>"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": f"{total}"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": f"{first_pass}"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": f"{first_fail}"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": f"{retest_pass}"}}]
                },
                {
                    "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                    "widgets": [{"textParagraph": {"text": f"{final_fail}"}}]
                },
            ]
        }
    })

    # ==========================================
    # 3. ĐÓNG GÓI THÀNH PAYLOAD HOÀN CHỈNH
    # ==========================================
    payload = {
        "cardsV2": [
            {
                "cardId": "yield_report_card",
                "card": {
                    "header": {
                        "title": "📊 YIELD RATE REPORT",
                        "subtitle": "Báo cáo theo thời gian thực",
                        "imageUrl": "https://cdn-icons-png.flaticon.com/512/8336/8336043.png",
                        "imageType": "CIRCLE"
                    },
                    "sections": [
                        {
                            "widgets": widgets_list
                        }
                    ]
                }
            }
        ]
    }
    
    return payload

import os

from PIL import Image, ImageDraw, ImageFont

# Thư mục xuất ảnh
OUTPUT_DIR = "images_export"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD_PATH = "C:\\Windows\\Fonts\\tahomabd.ttf"
FONT_REG_PATH = "C:\\Windows\\Fonts\\tahoma.ttf"

def draw_dashboard(data_list, project, line, start_time, end_time, filename="pro_dashboard.png"):
    # --- 1. CẤU HÌNH MÀU SẮC (UI/UX) ---
    COLOR_BG = (18, 22, 33)        # Xanh đen đậm
    COLOR_CARD = (30, 39, 58)      # Xanh xám
    COLOR_ACCENT = (56, 189, 248)  # Xanh dương neon (Điểm nhấn cho Project/Line)
    COLOR_TEXT_MAIN = (255, 255, 255)
    COLOR_TEXT_DIM = (160, 174, 192)
    COLOR_SUCCESS = (72, 187, 120) # Xanh lá
    COLOR_WARNING = (236, 201, 75) # Vàng cam (Cho cột Retest %)
    COLOR_DANGER = (245, 101, 101) # Đỏ

    # --- 2. TÍNH TOÁN KÍCH THƯỚC ---
    width = 1000  # Mở rộng ngang để chứa thêm cột
    row_height = 50
    header_height = 120 # Tăng height để chứa thêm thông tin Project/Line
    kpi_card_height = 120
    footer_height = 40
    
    total_height = header_height + kpi_card_height + (len(data_list) + 1) * row_height + footer_height + 60
    
    img = Image.new('RGB', (width, total_height), color=COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Nạp font
    font_title = ImageFont.truetype(FONT_BOLD_PATH, 32)
    font_kpi_val = ImageFont.truetype(FONT_BOLD_PATH, 36)
    font_kpi_lab = ImageFont.truetype(FONT_REG_PATH, 16)
    font_meta = ImageFont.truetype(FONT_REG_PATH, 20)
    font_table_h = ImageFont.truetype(FONT_BOLD_PATH, 18)
    font_table_d = ImageFont.truetype(FONT_REG_PATH, 18)

    # --- 3. VẼ TIÊU ĐỀ & THÔNG TIN DỰ ÁN (HEADER) ---
    draw.text((40, 20), "YIELD RATE REPORT", font=font_title, fill=COLOR_TEXT_MAIN)
    draw.line([(40, 60), (width - 40, 60)], fill=(45, 55, 72), width=1)
    # Chuỗi thông tin Meta (Project, Line, Time)
    meta_text = f"Project: {project}   |   Line: {line}   |   Time: {start_time} - {end_time}"
    draw.text((40, 70), meta_text, font=font_meta, fill=COLOR_ACCENT)

    # Kẻ một đường line mờ ngăn cách header
    draw.line([(40, 105), (width - 40, 105)], fill=(45, 55, 72), width=1)

    # --- 4. VẼ CÁC THẺ KPI TÓM TẮT ---
    total_all = sum(int(row['COUNT_TOTAL']) for row in data_list)
    final_fail_all = sum(int(row['FINAL_FAIL']) for row in data_list)
    first_fail_all = sum(int(row['FIRST_FAIL']) for row in data_list)
    first_pass_all = sum(int(row['FIRST_PASS']) for row in data_list)
    retest_all = sum(int(row['RETEST_PASS']) for row in data_list)

    rpy_overall_rate= f"{(retest_all/total_all)*100:.2f}%" if total_all > 0 else "N/A"
    ffy_overall_rate= f"{(final_fail_all/total_all)*100:.2f}%" if total_all > 0 else "N/A"

    fpy_overall_rate= f"{(first_pass_all/total_all)*100:.2f}%" if total_all > 0 else "N/A"
    #overall_yield = f"{(1 - (fail_all/total_all))*100:.2f}%" if total_all > 0 else "N/A"

    kpis = [
        {"label": "FIRST PASS RATE", "value": fpy_overall_rate, "color": COLOR_SUCCESS},
        {"label": "RETEST PASS RATE", "value": rpy_overall_rate, "color": COLOR_TEXT_MAIN},
        {"label": "FINAL FAIL RATE", "value": ffy_overall_rate, "color": COLOR_DANGER}
    ]

    card_w = (width - 120) // 3
    for i, kpi in enumerate(kpis):
        x_start = 40 + i * (card_w + 20)
        draw.rounded_rectangle([x_start, 125, x_start + card_w, 225], radius=12, fill=COLOR_CARD)
        draw.text((x_start + 20, 145), kpi['label'], font=font_kpi_lab, fill=COLOR_TEXT_DIM)
        draw.text((x_start + 20, 170), kpi['value'], font=font_kpi_val, fill=kpi['color'])

    # --- 5. VẼ BẢNG DỮ LIỆU ---
    table_y_start = 260
    # Thêm cột RETEST %
    headers = ["Station Name", "Total Input", "First Fail", "Retest Pass", "Final Fail", "Retest Rate"]
    # Chia lại tọa độ x cho 7 cột (Tổng width 1150)
    col_x = [70, 350, 480, 590, 710, 830] 

    # Vẽ nền Header bảng
    draw.rounded_rectangle([40, table_y_start, width - 40, table_y_start + row_height], radius=8, fill=COLOR_CARD)
    for i, h_text in enumerate(headers):
        draw.text((col_x[i], table_y_start + 16), h_text, font=font_table_h, fill=COLOR_TEXT_DIM)

    # Vẽ các dòng dữ liệu
    for idx, row in enumerate(data_list):
        y_pos = table_y_start + (idx + 1) * row_height + 10
        
        draw.line([(40, y_pos + row_height - 5), (width - 40, y_pos + row_height - 5)], fill=(45, 55, 72))

        # Lấy các chỉ số
        station_name = row['GROUP_NAME']
        total_input = int(row['COUNT_TOTAL'])
        first_fail = int(row['FIRST_FAIL'])
        retest_pass = int(row['RETEST_PASS'])
        final_fail = int(row['FINAL_FAIL'])
        
        # Tính phần trăm Retest
        retest_rate = (retest_pass / total_input * 100) if total_input > 0 else 0.0

        # Đổ data text
        draw.text((col_x[0], y_pos + 15), station_name, font=font_table_d, fill=COLOR_TEXT_MAIN)
        draw.text((col_x[1], y_pos + 15), str(total_input), font=font_table_d, fill=COLOR_TEXT_MAIN)
        draw.text((col_x[2], y_pos + 15), str(first_fail), font=font_table_d, fill=COLOR_TEXT_MAIN)
        draw.text((col_x[3], y_pos + 15), str(retest_pass), font=font_table_d, fill=COLOR_TEXT_MAIN)
        
        # In Retest % (Màu vàng cam để dễ phân biệt)
        
        # Final Fail bôi đỏ nếu > 0
        final_color = COLOR_DANGER if final_fail > 0 else COLOR_TEXT_MAIN
        retest_color = COLOR_SUCCESS if retest_rate < 1 else (COLOR_WARNING if retest_rate < 3 else COLOR_DANGER )
        draw.text((col_x[4], y_pos + 15), str(final_fail), font=font_table_d, fill=final_color)
        draw.text((col_x[5], y_pos + 15), f"{retest_rate:.2f}%", font=font_table_d, fill=retest_color)


        # Trạng thái (Pill)
       

    # --- 6. LƯU ẢNH ---
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)
    print(f"ok: {filepath}")
    return filepath

# =========================================
# CÁCH CHẠY THỬ VỚI DATA MỚI
# =========================================
if __name__ == "__main__":
    test_data = [
        {'GROUP_NAME': 'FATP-AUDIO', 'COUNT_TOTAL': 160.0, 'FIRST_FAIL': 20.0, 'RETEST_PASS': 20.0, 'FINAL_FAIL': 1.0},
        {'GROUP_NAME': 'FATP-RF-5GMMW-COMBO', 'COUNT_TOTAL': 108.0, 'FIRST_FAIL': 2.0, 'RETEST_PASS': 2.0, 'FINAL_FAIL': 0.0},
        {'GROUP_NAME': 'FATP-RF-CELL', 'COUNT_TOTAL': 159.0, 'FIRST_FAIL': 1.0, 'RETEST_PASS': 1.0, 'FINAL_FAIL': 0.0}
    ]

    # Truyền thêm các tham số Project, Line, Time vào hàm
    draw_dashboard(
        data_list=test_data, 
        project="4CS4", 
        line="4CS4_FVN-E2F3-G01", 
        start_time="08:00", 
        end_time="20:00",
        filename="yield_d26_line02.png"
    )