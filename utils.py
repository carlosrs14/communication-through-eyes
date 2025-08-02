import math
import cv2

def draw_face_box(frame, landmarks, image_w, image_h):
    x_vals = [int(p.x * image_w) for p in landmarks]
    y_vals = [int(p.y * image_h) for p in landmarks]
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

def draw_eye_box(frame, landmarks, eye_idxs, image_w, image_h):
    eye_points = [landmarks[i] for i in eye_idxs]
    x_vals = [int(p.x * image_w) for p in eye_points]
    y_vals = [int(p.y * image_h) for p in eye_points]
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 255), 2)

def calc_ear(landamarks, eye_idxs):

    # para calcular las distancias entre puntos claves
    def dist(p1, p2):
        return math.hypot(p2.x - p1.x, p2.y - p1.y)
    
    # aqui obtenemos los 6 puntos claves del ojo
    p1, p2, p3, p4, p5, p6 = [landamarks[i] for i in eye_idxs]
    
    # aqui aplico la formula del ear: (altura1 + altura2) / (2 * ancho)
    return (dist(p2, p6) + dist(p3, p5)) / (2.0 * dist(p1, p4))
