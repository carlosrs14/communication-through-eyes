# Blink to Morse
Este proyecto permite convertir parpadeos humanos en texto usando código Morse, empleando visión por computadora con MediaPipe y OpenCV. Está pensado como una forma alternativa de comunicación basada en gestos oculares.

## ¿Cómo funciona?
Se utiliza la cámara para detectar el rostro y los ojos.

Cuando el ojo está cerrado y luego se abre, se interpreta como un parpadeo.

Dos tipos de parpadeos:

Parpadeo corto (.)

Doble parpadeo rápido (-)

Una pausa larga entre parpadeos indica el fin de una letra.

Cada letra es traducida del buffer de Morse a un caracter y se añade al mensaje final.

## Tecnologias usadas
Python3 como lenguaje de programación.

MediaPipe para detectar y rastrear el rostro y los ojos.

OpenCV para la manipulación de imágenes y visualización en tiempo real.
