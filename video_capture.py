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

    def is_finger_folded(tip, pip):
        return tip.y > pip.y


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
                index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                screen_x = int(wrist.x * screen_w)
                screen_y = int(wrist.y * screen_h)

                # pyautogui.moveTo(screen_x, screen_y)

                cv2.circle(frame, (int(wrist.x * w), int(wrist.y * h)), 2, (0, 255, 0), -1)
                cv2.circle(frame, (int(index_tip.x * w), int(index_tip.y * h)), 2, (0, 255, 0), -1)

                # Detección de mano cerrada o abierta
                fingers_folded = 0

                # Pulgar (comparación horizontal)
                if landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_IP].x:
                    fingers_folded += 1

                # Índice
                if is_finger_folded(landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                                    landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP]):
                    fingers_folded += 1

                # Medio
                if is_finger_folded(landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                                    landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]):
                    fingers_folded += 1

                # Anular
                if is_finger_folded(landmarks[mp_hands.HandLandmark.RING_FINGER_TIP],
                                    landmarks[mp_hands.HandLandmark.RING_FINGER_PIP]):
                    fingers_folded += 1

                # Meñique
                if is_finger_folded(landmarks[mp_hands.HandLandmark.PINKY_TIP],
                                    landmarks[mp_hands.HandLandmark.PINKY_PIP]):
                    fingers_folded += 1

                # Determinar estado de la mano
                hand_closed = fingers_folded >= 4
                text = "Mano Cerrada" if hand_closed else "Mano Abierta"

                if hand_closed:
                    with open("coords.txt", "w") as f:
                        f.write(f"{0.0},{0.1}")
                else:
                    with open("coords.txt", "w") as f:
                        f.write(f"{wrist.x * w},{wrist.y * h}")

                # Mostrar texto en la imagen
                cv2.putText(frame, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
