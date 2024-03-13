#-------------------------------------------------------------------------------------------------
#------- DuckHunt -----------------------------------------------------------------------------
#------- Coceptos básicos de PDI------------------------------------------------------------------
#------- Por: Carolina jimenes - @udea.edu.co --------------------------------
#-------------Santiago Naranjo Sanchez - santiago.naranjo1@udea.edu.co-----------------------
#------- Presentado a: David Stephen Fernández MC CAN --------------------------------------------
#----------------------Profesor Facultad de Ingenieria BLQ 21-409  -------------------------------
#------- --------------CC 71629489, Tel 2198528,  Wpp 3007106588 ---------------------------------
#------- Curso Básico de Procesamiento de Imágenes y Visión Artificial----------------------------
#------- marzo de 2024-----------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#------------------1. Importación de bibliotecas necesarias --------------------------------------
#-------------------------------------------------------------------------------------------------

import cv2                  # Importa la biblioteca OpenCV para el procesamiento de imágenes.
import mediapipe as mp      # Proporciona herramientas para el seguimiento y detección de puntos clave en imágenes y vídeos.
import numpy as np          # Importa la biblioteca NumPy para operaciones numéricas eficientes.
import pyautogui            # Permite la automatización de tareas en el sistema operativo mediante el control del mouse y teclado.
import pygetwindow as gw    # Proporciona funciones para interactuar con ventanas y gestionar aplicaciones.

#-------------------------------------------------------------------------------------------------
#------------------2.inicialización de módulos de Cámara --------------------------------------
#-------------------------------------------------------------------------------------------------

mp_drawing = mp.solutions.drawing_utils         # Módulo de Mediapipe que proporciona utilidades para dibujar sobre imágenes y vídeos.
mp_hands = mp.solutions.hands                   # Módulo de Mediapipe específicamente diseñado para el seguimiento de manos.
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)        # Inicializa la captura de vídeo desde la cámara web.

color_mouse_pointer = (123, 255, 0)             #se el asigna un color RGB al puntero del mouse

window = gw.getWindowsWithTitle('Duck Hunt')[0] # Obtiene la ventana del juego Duck Hunt.
window.activate()                               # Activa la ventana del juego Duck Hunt y la trae al frente.

#------------------------------------- Puntos de la pantalla-juego------------------------------------------------

SCREEN_GAME_X_INI = 366     # Coordenada x inicial de la pantalla del juego.
SCREEN_GAME_Y_INI = 144     # Coordenada y inicial de la pantalla del juego.
SCREEN_GAME_X_FIN = 1001    # Coordenada x final de la pantalla del juego.
SCREEN_GAME_Y_FIN = 616     # Coordenada y final de la pantalla del juego.

#------------------------------------- Relación de aspecto de la pantalla-juego-----------------------------------

aspect_ratio_screen = (SCREEN_GAME_X_FIN - SCREEN_GAME_X_INI) / (SCREEN_GAME_Y_FIN - SCREEN_GAME_Y_INI)

#print("aspect_ratio_screen:", aspect_ratio_screen) # Relación de aspecto de la pantalla del juego.

X_Y_INI = 50                 # Coordenada x e y inicial del área de control del mouse.

#-----------------------------Funcion para calcular la distancia euclidiana entre dos puntos en un plano bidimensional -------------------

def calculate_distance(x1, y1, x2, y2): 
    p1 = np.array([x1, y1])
    p2 = np.array([x2, y2])
    return np.linalg.norm(p1 - p2)

#-----------------------------Funcion para detectar si el dedo índice está hacia abajo -----------------------------------

def detect_finger_down(hand_landmarks):
    finger_down = False         # Inicializa la variable que indica si el dedo índice está hacia abajo.
    color_base = (0, 255, 0)    # Inicializa el color del punto y la línea que representa la base de la mano.
    color_index = (0, 255, 0)   # Inicializa el color del punto y la línea que representa el dedo índice.


    x_base1 = int(hand_landmarks.landmark[0].x * width)  # Coordenada x de la base de la mano.
    y_base1 = int(hand_landmarks.landmark[0].y * height) # Coordenada y de la base de la mano.

    x_base2 = int(hand_landmarks.landmark[9].x * width)  # Coordenada x de la base de la mano.
    y_base2 = int(hand_landmarks.landmark[9].y * height) # Coordenada y de la base de la mano.

    x_index = int(hand_landmarks.landmark[8].x * width)  # Coordenada x del dedo índice.
    y_index = int(hand_landmarks.landmark[8].y * height) # Coordenada y del dedo índice.

    d_base = calculate_distance(x_base1, y_base1, x_base2, y_base2)       # Distancia entre los puntos que representan la base de la mano.
    d_base_index = calculate_distance(x_base1, y_base1, x_index, y_index) # Distancia entre los puntos que representan la base de la mano y el dedo índice.

    if d_base_index < d_base:                                   # Si la distancia entre la base de la mano y el dedo índice es menor que la distancia entre los puntos que representan la base de la mano.
        finger_down = True                                      # El dedo índice está hacia abajo.
        color_base = (203, 0, 0)                                # Cambia el color de la base de la mano.
        color_index = (203, 0, 0)                               # Cambia el color del dedo índice.

    cv2.circle(output, (x_base1, y_base1), 5, color_base, 2)                # Dibuja un punto en la base de la mano.
    cv2.circle(output, (x_index, y_index), 5, color_index, 2)               # Dibuja un punto en el dedo índice.
    cv2.line(output, (x_base1, y_base1), (x_base2, y_base2), color_base, 3) # Dibuja una línea que representa la base de la mano.
    cv2.line(output, (x_base1, y_base1), (x_index, y_index), color_index, 3)# Dibuja una línea que representa el dedo índice.

    return finger_down                                          # Retorna si el dedo índice está hacia abajo.



#--------------------------------------------------------------------------------------------------------------------------------
#------------------3.Bucle principal para el seguimiento de la mano y el control del mouse --------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

with mp_hands.Hands(                       # Inicializa el módulo de Mediapipe para el seguimiento de manos.
    static_image_mode=False,               # Modo de imagen estática.lo que significa que el modelo espera un video
    max_num_hands=1,                       # Número máximo de manos a detectar.
    min_detection_confidence=0.5) as hands:# Umbral de confianza mínimo para la detección de manos.

    while True:                            # Bucle principal para el seguimiento de la mano y el control del mouse.
        ret, frame = cap.read()            # Captura un fotograma de la cámara.
        if ret == False:                   # Si no se captura un fotograma, termina el bucle.
            break                          # Termina el bucle.

        height, width, _ = frame.shape     # Obtiene el alto y ancho del fotograma.
        frame = cv2.flip(frame, 1)         # Voltea el fotograma horizontalmente.

#-----------------------------Dibuja un rectángulo en el área de control del mouse-----------------------------------
        
        area_width = width - X_Y_INI * 2                    # Ancho del área de control del mouse.
        area_height = int(area_width / aspect_ratio_screen) # Alto del área de control del mouse.
        aux_image = np.zeros(frame.shape, np.uint8)         # Crea una imagen auxiliar con el mismo tamaño que el fotograma.
        aux_image = cv2.rectangle(aux_image, (X_Y_INI, X_Y_INI), (X_Y_INI + area_width, X_Y_INI +area_height), -1)# Dibuja un rectángulo en el área de control del mouse.
        output = cv2.addWeighted(frame, 1, aux_image, 0.7, 0) # Combina el fotograma con la imagen auxiliar.

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convierte el fotograma de BGR a RGB.
        results = hands.process(frame_rgb)                  # Procesa el fotograma para detectar manos.
        
        
        if results.multi_hand_landmarks is not None:            # Si se detecta al menos una mano.
            for hand_landmarks in results.multi_hand_landmarks: # Para cada mano detectada.
                x = int(hand_landmarks.landmark[9].x * width)   # Coordenada x de la punta del dedo índice.
                y = int(hand_landmarks.landmark[9].y * height)  # Coordenada y de la punta del dedo índice.
                xm = np.interp(x, (X_Y_INI, X_Y_INI + area_width), (SCREEN_GAME_X_INI, SCREEN_GAME_X_FIN))# Coordenada x en la pantalla del juego.
                ym = np.interp(y, (X_Y_INI, X_Y_INI + area_height), (SCREEN_GAME_Y_INI, SCREEN_GAME_Y_FIN))# Coordenada y en la pantalla del juego.
               
                pyautogui.moveTo(int(xm), int(ym))                  # Mueve el puntero del mouse a la coordenada (xm, ym) en la pantalla del juego.
                
                if detect_finger_down(hand_landmarks):              # Si el dedo índice está hacia abajo.
                    pyautogui.click()                               # Hace clic con el mouse.
                
                cv2.circle(output, (x, y), 10, color_mouse_pointer, 3) # Dibuja un círculo en la punta del dedo índice.
                cv2.circle(output, (x, y), 5, color_mouse_pointer, -1) # Dibuja un punto en la punta del dedo índice.
                

#-----------------------------Redimensiona la imagen y la muestra en una ventana-----------------------------------      
                            
        nuevo_ancho = 310   # Ancho de la imagen redimensionada.
        nuevo_alto = 310    # Alto de la imagen redimensionada.

        relacion_aspecto_actual = output.shape[1] / output.shape[0] # Relación de aspecto actual de la imagen

        if relacion_aspecto_actual > 1:            # Si la relación de aspecto actual es mayor que 1.
            nuevo_alto = int(nuevo_ancho / relacion_aspecto_actual)# Redimensiona el alto conservando la relación de aspecto.
        else:
            nuevo_ancho = int(nuevo_alto * relacion_aspecto_actual)# Redimensiona el ancho conservando la relación de aspecto.

        imagen_redimensionada = cv2.resize(output, (nuevo_ancho, nuevo_alto))# Redimensiona la imagen.

        cv2.imshow('Control del Mouse con PDI', imagen_redimensionada)# Muestra la imagen redimensionada en una ventana.
       

        if cv2.waitKey(1) & 0xFF == 27:             # Si se presiona la tecla Esc.rompe el ciclo
            break
cap.release()                                       # Libera la captura de la cámara.
cv2.destroyAllWindows()                             # Cierra todas las ventanas.

#----------------------------------------------------------------------------------------------------------
#---------------------------------Fin del programa----------------------------------------------------------
#----------------------------------------------------------------------------------------------------------