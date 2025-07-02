import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size();

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        h, w, _ = frame.shape

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark

                wrist = landmarks[mp_hands.HandLandmark.WRIST]

                screen_x = int(wrist.x * screen_w)
                screen_y = int(wrist.y * screen_h)

                # pyautogui.moveTo(screen_x, screen_y)

                cv2.circle(frame, (int(wrist.x * w), int(wrist.y * h)), 2, (0, 255, 0), -1)
               
                with open("coords.txt", "w") as f:
                    f.write(f"{wrist.x * w},{wrist.y * h}")

                cv2.putText(frame, "", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
