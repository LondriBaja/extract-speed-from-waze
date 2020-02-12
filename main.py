import cv2
import numpy as np
import pytesseract
from PIL import Image
import pandas as pd
import json

file_path = 'segundo.mp4'
raw_folder_path = 'raw_files/'
output_folder_path = 'output/'

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"

def get_String(img):
    #img = cv2.medianBlur(img, 5)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    ret, img = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV) 
    cv2.imshow("number", img)
    
    result = pytesseract.image_to_string(img, config='--psm 10 --oem 3 digits')
    return result


cap = cv2.VideoCapture(raw_folder_path + file_path)

lastTime = 0

data_array = []

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        time = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
        frame = cv2.resize(frame, (720, 1488))
        
        resized = cv2.resize(frame, (360, 744))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = frame[1109:1170, 60:140]

        if time - lastTime > 0.1:
            speed = get_String(frame)
            try:
                speed = int(speed)
            except:
                pass
            current_data = {
                'time': time,
                'speed': speed
            }

            data_array.append(current_data)

            lastTime = time
        
        cv2.imshow("video", resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

print(data_array)
pd.read_json(json.dumps(data_array)).to_excel(output_folder_path + file_path[:-4] + ".xlsx")