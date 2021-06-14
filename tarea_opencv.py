import cv2 
import sys
import logging as log
import datetime as dt
from time import sleep

print("*"*50)
entrada=input("Seleccione 1 para imagen o 2 para webcam 3 para salir: ")
print("*"*50)

continuar = True
while continuar:
    if entrada == "1":
        # imagePath = sys.argv[1]
        imagePath = input("Introduzca imagen a analizar: ")
        while "." not in imagePath:
            print("Introduzca la imagen con su extension (.jpg, .png)")
            imagePath = input("Introduzca imagen a analizar: ")

        cascPath = "haarcascade_frontalface_default.xml"

        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(cascPath)

        # Read the image
        image = cv2.imread(imagePath)
       
       #Tratando de capturar cuando se introduce una imagen que no existe
        try:
            image is None
        except:
            print("Introduzca la imagen con su extension (.jpg, .png)")
            continuar = False
       
       
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image 
        # The function returns a list of rectangles in which it believes it found a face. 
        # Next, we will loop over where it thinks it found something.
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=4  ,
            minSize=(30, 30)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )

        print("Found {0} faces!".format(len(faces)))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            centro = (x+w//2,y+h//2)
            cv2.circle(image, (centro), (w//2), (0, 0, 255), 2)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Colola un texto en la imagen analizada con el numero de caras detectadas
        font = cv2.FONT_HERSHEY_SIMPLEX
        # fontScale
        fontScale = 1
        color = (0, 255, 255)
        origen = (50,50)
        # Line thickness of 2 px
        thickness = 2
        
        # Using cv2.putText() method
        #Syntax: cv2.putText(image, text, origen, fuente, fontScale, color[, thickness[, tipo de linea ]])
        image = cv2.putText(image, f'{len(faces)} Caras ', origen, font, 
                        fontScale, color, thickness, cv2.LINE_AA)
        image = cv2.putText(image, "Presione 's' para guardar una copia", (50,80), font, 0.7, (255,240,239), thickness, cv2.LINE_AA)
        #mostramos la imagen
        cv2.imshow("Faces found", image)
        #Guardamos una imagen con la informacion detectada
        ret = cv2.waitKey(0)

        if ret == 115:
            cv2.imwrite("detectadas.jpg",image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("*"*50)
        entrada=input("Seleccione 1 para imagen o 2 para webcam 3 para salir: ")
        print("*"*50)


    elif entrada =="2":
        cascPath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        # log.basicConfig(filename='webcam.log',level=log.INFO)

        video_capture = cv2.VideoCapture(0)
        anterior = 0

        while True:
            if not video_capture.isOpened():
                print('Unable to load camera.')
                sleep(5)
                pass

            # Capture frame-by-frame
            ret, frame = video_capture.read()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=4,
                minSize=(20, 20)
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            if anterior != len(faces):
                anterior = len(faces)
                log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


            # Display the resulting frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            # fontScale
            fontScale = 1
            color = (0, 255, 255)
            origen = (50,30)
            # Line thickness of 2 px
            thickness = 2

            frame = cv2.putText(frame, f'Caras detectadas: {len(faces)} ', origen, font, fontScale, color, thickness, cv2.LINE_AA)
            cv2.imshow('Video', frame)
            
            ret = cv2.waitKey(1)

            if ret == 115:
                cv2.imwrite("caras_detectadas.jpg",frame)

            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Display the resulting frame
            cv2.imshow('Video', frame)

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()
        
        print("*"*50)
        entrada=input("Seleccione 1 para imagen o 2 para webcam 3 para salir: ")
        print("*"*50)
    elif entrada =="3":
        salir = input ("Seguro quieres salir (S/N): ")
        if salir == "s" or salir == "S":
            continuar = False
        
        elif salir == "n" or salir =="N":
            print("*"*50)
            entrada=input("Seleccione 1 para imagen o 2 para webcam 3 para salir: ")
            print("*"*50)
    else:
        print("entrada invalida")
        print("*"*50)
        entrada=input("Seleccione 1 para imagen o 2 para webcam 3 para salir: ")
        print("*"*50)
