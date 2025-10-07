#!/usr/bin/env python3
from gpiozero import MotionSensor
from picamera import PiCamera
from time import sleep
from datetime import datetime

# 設定 PIR 感應器的 GPIO 腳位 (請根據你的接線修改)
pir = MotionSensor(26)  # 假設接在 GPIO 4

# 設定相機
camera = PiCamera()
camera.rotation = 180  # 旋轉 180 度

print("PIR 感應器啟動中...")
print("等待感應器穩定...")
sleep(2)  # 讓 PIR 感應器穩定

print("準備就緒!等待偵測動作...")

try:
    while True:
        # 等待偵測到動作
        pir.wait_for_motion()
        print("偵測到動作!")
        
        # 倒數 5 秒
        for i in range(5, 0, -1):
            print(f"倒數 {i} 秒...")
            sleep(1)
        
        # 拍照
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"motion_{timestamp}.jpg"
        camera.capture(filename)
        print(f"已拍攝照片: {filename}")
        
        # 等待沒有動作後再繼續偵測
        print("等待動作停止...")
        pir.wait_for_no_motion()
        print("繼續偵測中...")
        sleep(1)  # 避免連續觸發

except KeyboardInterrupt:
    print("\n程式已停止")
finally:
    camera.close()