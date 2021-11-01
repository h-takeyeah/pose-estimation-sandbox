# Thanks to https://youtu.be/brwgBf6VB0I

# 最小限のコードを適当にクラス化したやつ
import cv2
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_draw
from time import time

class PoseDetector():

    def __init__(self, mode=False, model_complexity=1, smooth_landmarks=True,
                enable_seg=False, smooth_seg=True, detection_con=0.5, track_con=0.5):

        self.mode = mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_seg = enable_seg
        self.smooth_seg = smooth_seg
        self.detection_con = detection_con
        self.track_con = track_con
        self.pose = mp_pose.Pose(self.mode, self.model_complexity, self.smooth_landmarks,
            self.enable_seg, self.smooth_seg, self.detection_con, self.track_con)
        
    def find_pose(self, img, draw=True):
        # 変換
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # モデルに画像を渡す
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks:
            if draw:
                mp_draw.draw_landmarks(img, self.results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        return img

    def find_position(self, img, draw=True):
        '''
        検出したポーズの各節点の位置をリストで返す．接点と番号の対応関係はここを参照のこと
        https://google.github.io/mediapipe/solutions/pose#pose-landmark-model-blazepose-ghum-3d
        '''
        lm_list = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return lm_list

def main():
    # VideoCapture()に映像ストリームを渡す．
    # https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html
    device_id = 0
    # 有効なカメラが見つかるまで回す(最大4回)
    while device_id < 4:
        cap = cv2.VideoCapture(device_id) # /dev/video{device_id}
        if cap.isOpened():
            break
        device_id = device_id + 1

    if not cap.isOpened():
        print('Can\'t open a camera')
        return

    # FPS表示用カウンタ
    p_time = 0
    detector = PoseDetector()
    while True:
        # フレーム1枚を読み込む
        success, img = cap.read()

        # フレームにポーズを書き足す
        img = detector.find_pose(img)
        # ポーズの位置をリストで取得
        lm_list = detector.find_position(img)

        # FPSを表示するための処理
        c_time = time()
        fps = 1/(c_time-p_time)
        p_time = c_time

        cv2.putText(img, f'{int(fps)}', (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow('Image', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
