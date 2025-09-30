import RPi.GPIO as GPIO
import time

# ===== 馬達設定區 =====
SERVO_NAME = "MyServo_SG90_01"  # 幫你的馬達取個名字
servoPIN = 17

# 脈衝寬度設定 (單位: 秒)
MIN_PULSE_WIDTH = 0.0005   # 0.5ms (預設1ms，但很多馬達更小)
MAX_PULSE_WIDTH = 0.0025   # 2.5ms (預設2ms，但很多馬達更大)
FRAME_WIDTH = 0.020        # 20ms (50Hz)

# 計算對應的 duty cycle
FREQUENCY = 1 / FRAME_WIDTH  # 50Hz
MIN_DUTY = (MIN_PULSE_WIDTH / FRAME_WIDTH) * 100
MAX_DUTY = (MAX_PULSE_WIDTH / FRAME_WIDTH) * 100
CENTER_DUTY = (MIN_DUTY + MAX_DUTY) / 2

print(f"========== 伺服馬達校正程式 ==========")
print(f"馬達名稱: {SERVO_NAME}")
print(f"GPIO 針腳: {servoPIN}")
print(f"頻率: {FREQUENCY} Hz")
print(f"脈衝範圍: {MIN_PULSE_WIDTH*1000:.2f}ms ~ {MAX_PULSE_WIDTH*1000:.2f}ms")
print(f"Duty Cycle 範圍: {MIN_DUTY:.2f}% ~ {MAX_DUTY:.2f}%")
print(f"中心值: {CENTER_DUTY:.2f}%")
print(f"======================================\n")

# GPIO 初始化
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, FREQUENCY)
p.start(0)

def set_angle(angle):
    """根據角度設定 duty cycle (0-180度)"""
    duty = MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY)
    p.ChangeDutyCycle(duty)
    return duty

try:
    print("開始校正測試...")
    print("按 Ctrl+C 可以隨時停止\n")
    
    # 測試 1: 基本角度測試
    print("=== 測試 1: 基本角度測試 ===")
    angles = [0, 45, 90, 135, 180, 90, 0]
    for angle in angles:
        duty = set_angle(angle)
        print(f"角度: {angle:3d}° → Duty Cycle: {duty:.2f}%")
        time.sleep(2)
    
    time.sleep(1)
    
    # 測試 2: 中心位置微調測試
    print("\n=== 測試 2: 中心位置微調 (85-95度) ===")
    print("仔細觀察哪個角度最接近你要的 90 度")
    for angle in range(85, 96):
        duty = set_angle(angle)
        print(f"角度: {angle}° → Duty Cycle: {duty:.2f}%")
        time.sleep(1.5)
    
    time.sleep(1)
    
    # 測試 3: 連續掃描
    print("\n=== 測試 3: 連續掃描 ===")
    print("馬達將連續掃描 0-180 度...")
    for i in range(3):  # 重複 3 次
        print(f"掃描第 {i+1} 輪")
        for angle in range(0, 181, 5):
            set_angle(angle)
            time.sleep(0.1)
        for angle in range(180, -1, -5):
            set_angle(angle)
            time.sleep(0.1)
    
    # 回到中心
    print("\n回到中心位置...")
    set_angle(90)
    time.sleep(2)
    
    print("\n校正測試完成！")
    print("\n如果需要調整，請修改程式開頭的:")
    print("  MIN_PULSE_WIDTH (最小脈衝寬度)")
    print("  MAX_PULSE_WIDTH (最大脈衝寬度)")
    print(f"\n目前設定已儲存為: {SERVO_NAME}")

except KeyboardInterrupt:
    print("\n\n測試中斷")

finally:
    p.ChangeDutyCycle(0)  # 停止訊號
    time.sleep(0.5)
    p.stop()
    GPIO.cleanup()
    print("GPIO 已清理完成")


# ===== 校正結果記錄區 =====
# 完成校正後，請記錄以下資訊：
"""
馬達名稱: MyServo_SG90_01
日期: 2025/09/30
針腳: GPIO 17

校正結果:
- 0度實際 duty cycle: _____
- 90度實際 duty cycle: _____
- 180度實際 duty cycle: _____
- 最小脈衝寬度: _____ ms
- 最大脈衝寬度: _____ ms

備註:
- 中心偏移量: _____ 度
- 使用的電源: _____V
- 馬達型號: _____
"""