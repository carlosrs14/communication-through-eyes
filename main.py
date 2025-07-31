import cv2
import mediapipe as mp
import time
import math
from morse_code import MORSE_CODE
from constants import *

# Índices de MediaPipe para el ojo derecho
RIGHT_EYE_IDX = [33, 160, 158, 133, 153, 144]

cap = cv2.VideoCapture(0)

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(min_detection_confidence = 0.5)


def calc_ear(landamarks, eye_idxs):

    # para calcular las distancias entre puntos claves
    def dist(p1, p2):
        return math.hypot(p2.x - p1.x, p2.y - p1.y)
    
    # aqui obtenemos los 6 puntos claves del ojo
    p1, p2, p3, p4, p5, p6 = [landamarks[i] for i in eye_idxs]
    
    # aqui aplico la formula del ear: (altura1 + altura2) / (2 * ancho)
    return (dist(p2, p6) + dist(p3, p5)) / (2.0 * dist(p1, p4))

def main():
    blink_start = None
    last_blink_time = 0
    buffer = ''
    message = ''

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # invierto la camara para no verme raro
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        now = time.time()

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            ear = calc_ear(landmarks, RIGHT_EYE_IDX)

            # ear por debajo del umbral para ojo cerrado
            if ear < EAR_THRESHOLD:
                if blink_start is None:
                    blink_start = now
            else:
                if blink_start:
                    duration = now - blink_start

                    #evitar detectar microparpadeos por accidente
                    if duration >= 0.01:
                        symbol = '.' if duration < DOT_DURATION else '-'
                        buffer += symbol
                        print(f"[{symbol}]", end = '', flush = True)

                    last_blink_time = now
                    blink_start = None
            
            # aqui al pasar bastante tiempo suponemos que se ha terminado la letra
            if buffer and (now - last_blink_time > LETTER_PAUSE):
                letra = MORSE_CODE.get(buffer, '?')
                message += letra
                print(f"-> {letra}")
                #despues de reconocer la letra limpiamos el buffer
                buffer = ''

        cv2.putText(frame, f"Message: {message}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Blink to Morse', frame)

        # si presionamos q se sale del bucle y se cierra la camara
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()