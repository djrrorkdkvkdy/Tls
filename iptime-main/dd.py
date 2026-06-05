import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 정보 및 경고 로그 숨기기
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # oneDNN 관련 경고 숨기기

import cv2
import mediapipe as mp
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

label = input("동작 이름 입력 (예: 손 펼치기, 주먹): ").strip()
while not label or "pip" in label or "install" in label:
    print("올바른 동작 이름을 입력해주세요. (명령어는 사용할 수 없습니다)")
    label = input("동작 이름 입력 (예: 손 펼치기, 주먹): ").strip()

with open("data.csv", "a", newline="") as f:
    writer = csv.writer(f)

    while True:
        ret, frame = cap.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:

                data = []

                for lm in hand_landmarks.landmark:
                    data.append(lm.x)
                    data.append(lm.y)

                data.append(label)
                writer.writerow(data)

                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Collecting Data", frame)

        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()