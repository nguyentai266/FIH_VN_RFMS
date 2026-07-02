#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import autoit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# 1. Cấu hình Chrome Options để giảm thiểu việc bị Google phát hiện Bot
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Mở full màn hình
options.add_experimental_exclusion_switches(["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Khởi khởi động trình duyệt Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 2. Selenium mở trang đăng nhập tài khoản Google
    print("🚀 Selenium đang mở trang login Google...")
    driver.get("https://accounts.google.com/")

    # 3. Nhập Email bằng Selenium (Đợi tối đa 10s cho ô nhập xuất hiện)
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
    )
    email_input.send_keys("tai_khoan_cua_sep@gmail.com")
    
    # Click nút Tiếp theo (Next)
    next_button = driver.find_element(By.ID, "identifierNext")
    next_button.click()
    print("➡️ Đã nhập Email.")

    # Chờ 3 giây để trang web chuyển đổi luồng password
    time.sleep(3)

    # 4. 🎯 KHỐI PHỐI HỢP AUTOIT (XỬ LÝ POPUP HỆ ĐIỀU HÀNH)
    # Trong môi trường doanh nghiệp (Google Workspace), khi ấn Next Email, hệ thống thường bật 
    # popup "Windows Security" bắt quét vân tay, nhập mã PIN Yubikey hoặc đăng nhập mạng nội bộ (Proxy Auth).
    # Lúc này Selenium không can thiệp được, ta gọi AutoIt vào việc:
    
    window_title = "Windows Security" # Tên cửa sổ popup hệ thống hiện lên
    if autoit.win_exists(window_title):
        print(f"🚨 Phát hiện cửa sổ bảo mật hệ thống: '{window_title}'!")
        autoit.win_activate(window_title)
        autoit.win_wait_active(window_title, 3)
        
        # Giả lập gõ mã PIN / Mật khẩu hệ thống và ấn Enter
        autoit.send("ma_pin_bao_mat_cua_sep")
        autoit.send("{ENTER}")
        print("✅ AutoIt đã bẻ khóa thành công cửa sổ Windows Security!")
        
    else:
        # Nếu không có popup của Windows, Selenium tiếp tục nhập mật khẩu trên trang web như bình thường
        print("🔒 Không có popup hệ thống, tiếp tục nhập mật khẩu trên Web bằng Selenium...")
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys("mat_khau_cua_sep")
        
        password_next = driver.find_element(By.ID, "passwordNext")
        password_next.click()
        print("✅ Đã nhập mật khẩu thành công.")

    # Đợi 5 giây để trang hoàn tất đăng nhập vào màn hình chính
    time.sleep(5)
    print("🎉 Đăng nhập hoàn tất!")

except Exception as e:
    print(f"❌ Có lỗi xảy ra trong luồng tự động hóa: {e}")

finally:
    # Đóng trình duyệt, giải phóng tài nguyên RAM
    driver.quit()
    print("🔒 Đã đóng trình duyệt an toàn.")    print("🔒 Đã đóng trình duyệt an toàn.")