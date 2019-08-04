#import time

import cv2
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_BUFFERSIZE,1)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    out = None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    roi = gray[int(width/3):int(width * 2/3) ,int(height/3):int(height * 2/3)]
    mean = cv2.mean(roi)

    mask = cv2.inRange(gray, mean, 255)

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours is not None:
        print(len(contours))
        print("\n")
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w < 256 or h < 128:
                continue
            print([x, y, w, h], ",")
            out = frame[x:x+w, y:y+h]
            cnt = np.array(contour).reshape((-1, 1, 2)).astype(np.int32)
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 3)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Crop", out)

    # time.sleep(2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
