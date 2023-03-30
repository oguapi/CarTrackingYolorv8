import os

import cv2
from ultralytics import YOLO
from rastreador import *

videoPath= os.path.join('.', 'data','via.mp4')
videoOutputPath= os.path.join('.','output.mp4')

cap= cv2.VideoCapture(videoPath)
ret, frame= cap.read()

#Save the video
# fourcc	4-character code of codec used to compress the frames.
cap_out= cv2.VideoWriter(videoOutputPath, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS),
                         (frame.shape[1], frame.shape[0])) #Specify the size

model= YOLO('yolov8n.pt')

tracker= Rastreador()  #Objeto de seguimiento

detection_threshold= 0.5
while ret:
    results= model(frame)

    for result in results:
        detections=[]
        for r in result.boxes.data.tolist():
            #print(r)  #One result is [427.0, 174.0, 520.0, 247.0, 0.7521307468414307, 2.0]
            x1, y1, x2, y2, score, class_id= r
            class_id= int(class_id)
            if score > detection_threshold and class_id == 2:
                #cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(225,0,200),2)
                #cv2.putText(frame,None,(x1,y1))
                detections.append([int(x1), int(y1), int(x2), int(y2)])

    #Tracking cars
    info_id= tracker.rastreo(detections)#poner tracker
    for inf in info_id:
        x1, y1, x2, y2, id= inf
        cv2.putText(frame, str(id), (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (25,10,0),2)
        cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(225,0,20),2)
    
    print(info_id)
    cv2.imshow("Video", frame)
    key= cv2.waitKey(15) #Retraso de milisegundos para leer el sgt frame
    #If we want clase the windows, we use Esc
    if (key==27):
        break

    cap_out.write(frame)    #Write the frames of the output video
    ret, frame= cap.read()

cap.release()
cap_out.release()
cv2.destroyAllWindows()