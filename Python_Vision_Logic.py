import cv2
import numpy as np
import serial
import time

# ---------------- SERIAL SETUP ----------------
ser = serial.Serial('COM5', 9600)   # ⚠️ CHANGE COM PORT
time.sleep(2)

last_cmd = ""
buffer = []

# ---------------- CAMERA ----------------
url = "http://192.168.4.1:81/stream"
cap = cv2.VideoCapture(url)

def send_command(cmd):
    global last_cmd

    if cmd != last_cmd:
        ser.write(cmd.encode())
        print("Sent:", cmd)
        last_cmd = cmd


while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error")
        break

    # Resize for speed
    frame = cv2.resize(frame, (320, 240))

    # Blur + HSV
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # -------- BLUE MASK --------
    lower_blue = np.array([100, 120, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # -------- RED MASK --------
    lower_red1 = np.array([0, 120, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 50])
    upper_red2 = np.array([180, 255, 255])

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask_red1, mask_red2)

    h, w = mask.shape

    # Split into 3 regions
    left = mask[:, 0:w//3]
    center = mask[:, w//3:2*w//3]
    right = mask[:, 2*w//3:w]

    left_sum = np.sum(left)
    center_sum = np.sum(center)
    right_sum = np.sum(right)

    # -------- DECISION --------
    if np.sum(red_mask) > 10000:
        direction = "STOP"
        cmd = 'S'

    elif left_sum > center_sum and left_sum > right_sum:
        direction = "LEFT"
        cmd = 'L'

    elif right_sum > center_sum and right_sum > left_sum:
        direction = "RIGHT"
        cmd = 'R'

    elif center_sum > 5000:
        direction = "FORWARD"
        cmd = 'F'

    else:
        direction = "SEARCH"
        cmd = 'S'

    # -------- SMOOTHING --------
    buffer.append(cmd)
    if len(buffer) > 5:
        buffer.pop(0)

    final_cmd = max(set(buffer), key=buffer.count)

    send_command(final_cmd)

    # -------- DISPLAY --------
    cv2.putText(frame, f"DIR: {direction}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.line(frame, (w//3, 0), (w//3, h), (255, 255, 255), 1)
    cv2.line(frame, (2*w//3, 0), (2*w//3, h), (255, 255, 255), 1)

    cv2.imshow("Camera", frame)
    cv2.imshow("Blue Mask", mask)
    cv2.imshow("Red Mask", red_mask)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
