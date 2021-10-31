# Thanks to https://youtu.be/brwgBf6VB0I

# 適当なビデオのポーズ検出をするための最小限のコード

import cv2
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_draw
from time import time

pose = mp_pose.Pose()

# ここに適当なビデオファイルへのパスを書く
cap = cv2.VideoCapture('/path/to/input.mp4')
p_time = 0

while True:
    success, img = cap.read()

    # 変換
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # モデルに画像を渡す
    results = pose.process(img_rgb)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

    # FPSを表示するための処理
    c_time = time()
    fps = 1/(c_time-p_time)
    p_time = c_time

    cv2.putText(img, f'{int(fps)}', (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)