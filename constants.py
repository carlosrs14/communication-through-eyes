
# Índices de MediaPipe para el ojo derecho
RIGHT_EYE_IDX = [33, 160, 158, 133, 153, 144]

EAR_THRESHOLD = 0.30      # ear por debajo de esto es ojo cerrado
DOUBLE_BLINK_MAX_INTERVAL = 0.40       # parpadeo < 0.3 segundos se considera punto (.) si demora mas el (-)
LETTER_PAUSE = 1.5       # si pasa 1 segundo sin parpadeo es porque es fin de letra