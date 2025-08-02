import mediapipe as mp
import time
from morse_code import MORSE_CODE
from constants import *
from utils import *

cap = cv2.VideoCapture(0)

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(min_detection_confidence = 0.5)

def main():
    blink_times = []
    last_processed_time = time.time()
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
            h, w, _ = frame.shape
            ear = calc_ear(landmarks, RIGHT_EYE_IDX)

            draw_face_box(frame, landmarks, w, h)
            draw_eye_box(frame, landmarks, RIGHT_EYE_IDX, w, h)

            # ear por debajo del umbral para ojo cerrado
            eye_closed = ear < EAR_THRESHOLD

            if not eye_closed and getattr(main, 'was_closed', False):
                blink_times.append(now)
            
                if len(blink_times) == 2:
                    dt = blink_times[1] - blink_times[0]
                    if dt <= DOUBLE_BLINK_MAX_INTERVAL:
                        buffer += '-'
                        print('[-]', end='', flush=True)
                    else:
                        buffer += '.'
                        print('[.]', end='', flush=True)
                        blink_times = [blink_times[1]]
                    
                    blink_times.clear()
                setattr(main, 'last_blink', now)
            setattr(main, 'was_closed', eye_closed)
            
        if blink_times and (now - blink_times[0]) > DOUBLE_BLINK_MAX_INTERVAL:
                buffer += '.'
                print('[.]', end='', flush=True)
                blink_times.clear()
                setattr(main, 'last_blink', now)

        # aqui al pasar bastante tiempo suponemos que se ha terminado la letra
        if buffer and (now - getattr(main, 'last_blink', now) > LETTER_PAUSE):
            letra = MORSE_CODE.get(buffer, '?')
            message += letra
            print(f"-> {letra}")
            # despues de reconocer la letra limpiamos el buffer
            buffer = ''

        cv2.putText(frame, f"Message: {message}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow('Blink to Morse', frame)

        # si presionamos q se sale del bucle y se cierra la camara
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main.was_clased = False
    main.last_blink = time.time()
    main()