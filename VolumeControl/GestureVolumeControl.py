import math
import time
import cv2
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm  



from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.SetMasterVolumeLevel(0,None)
minVol = volume.GetVolumeRange()[0]
maxVol = volume.GetVolumeRange()[1]





















wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
vol=0

detector = htm.handDetector(detectionCon=0.8)


pt, ct = 0, 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (int(x1), int(y1)), 10, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (int(x2), int(y2)), 10, (0, 255, 0), cv2.FILLED)
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (int(cx), int(cy)), 8, (0,255, 0), cv2.FILLED)
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if length < 15:
            cv2.circle(img, (int(cx), int(cy)), 8, (0, 0, 255), cv2.FILLED)
        
        
        vol=np.interp(length, (15, 240), (minVol, maxVol))
        volume.SetMasterVolumeLevel(vol, None)
        volBar = np.interp(length, [15, 240], [400, 150])
        volPer = np.interp(length, [15, 240], [0, 100])
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)












    
    ct = time.time()
    fps = 1 / (ct - pt) if ct != pt else 0
    pt = ct

    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 100, 100), 2)

    cv2.imshow('Video', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
